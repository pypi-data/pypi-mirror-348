import asyncio
import math
import mimetypes
import os
import shutil
import tempfile
import time
import subprocess
import signal
from enum import Enum
from pathlib import Path
from typing import Dict, List, Callable
import httpx
from fastapi import Body, FastAPI, HTTPException, Query, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.helpers.utils import upload_to_presigned_url, upload_parts_to_presigned_url
from app.logger import logger
from app.models import DownloadRequest, DownloadResult, MultipartUploadRequest, MultipartUploadResponse, ZipAndUploadRequest, ZipAndUploadResponse
from app.router import TimedRoute
from app.terminal_socket_server import terminal_socket_server
from app.tools.base import DEFAULT_WORKING_DIR
from app.tools.browser.browser_manager import BrowserDeadError, BrowserManager, PageDeadError
from app.tools.system_process import SystemProcessManager
from app.tools.terminal import terminal_manager
from app.tools.text_editor import text_editor, handle_text_editor_errors
from app.types.messages import BrowserActionRequest, BrowserActionResponse, TerminalApiResponse, TerminalWriteApiRequest, TextEditorActionResult, TextEditorCreateRequest, TextEditorDeleteRequest, TextEditorDirRequest, TextEditorFindContentRequest, TextEditorFindFileRequest, TextEditorMoveRequest, TextEditorStrReplaceRequest, TextEditorViewRequest, TextEditorWriteRequest
from contextlib import asynccontextmanager

system_process_manager = SystemProcessManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    system_process_manager.start_all()
    yield
    system_process_manager.cleanup()

app = FastAPI(lifespan=lifespan)
app.router.route_class = TimedRoute
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FileUploadRequest(BaseModel):
    file_path: str
    presigned_url: str

MULTIPART_THRESHOLD = 10485760  # 10MB

@app.post("/file/upload")
async def upload_file(request: FileUploadRequest = Body()):
    """
    Upload a file to presigned_url. If file size exceeds threshold, return size information instead.

    Request body:
    {
        "file_path": str,         # The local file path to upload
        "presigned_url": str      # The presigned URL to upload to
    }

    Returns:
    - For small files: Uploads the file and returns success response
    - For large files: Returns file information for multipart upload
    """
    try:
        path = Path(request.file_path).resolve()
        file_path = Path(DEFAULT_WORKING_DIR) / path.relative_to('/')
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        if not file_path.is_file():
            raise HTTPException(status_code=400, detail="Path is not a file")
        
        file_size = file_path.stat().st_size
        content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
        file_name = file_path.name
        
        if file_size > MULTIPART_THRESHOLD:
            return {
                "status": "need_multipart",
                "message": "File size exceeds single upload limit",
                "file_name": file_name,
                "content_type": content_type,
                "file_size": file_size,
                "need_multipart": True,
                "recommended_part_size": MULTIPART_THRESHOLD,
                "estimated_parts": file_size // MULTIPART_THRESHOLD + 1
            }
        
        with open(file_path, 'rb') as f:
            content = f.read()
            
        upload_result = await upload_to_presigned_url(
            data=content, 
            presigned_url=request.presigned_url, 
            content_type=content_type, 
            filename=file_name
        )
        
        if not upload_result:
            raise HTTPException(status_code=500, detail="Failed to upload file")
        
        return {
            "status": "success",
            "message": "File uploaded successfully",
            "file_name": file_name,
            "content_type": content_type,
            "file_size": file_size,
            "need_multipart": False,
            "upload_result": {"success": True, "uploaded": True}
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error handling file upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/file/multipart_upload")
async def multipart_upload_file(request: MultipartUploadRequest = Body(...)):
    """
    使用预签名URLs上传文件分片  # Upload file chunks using presigned URLs
    
    Request body:
    {
        "file_path": str,              # 要上传的文件路径  # File path to upload
        "presigned_urls": [            # 预签名URL列表  # List of presigned URLs
            {
                "part_number": int,    # 分片编号（从1开始）  # Part number (starting from 1)
                "url": str             # 该分片的预签名URL  # Presigned URL for this part
            },
            ...
        ],
        "part_size": int              # 每个分片的大小（字节）  # Size of each part in bytes
    }
    """
    try:
        path = Path(request.file_path).resolve()
        file_path = Path(DEFAULT_WORKING_DIR) / path.relative_to('/')
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        if not file_path.is_file():
            raise HTTPException(status_code=400, detail="Path is not a file")
        
        file_size = file_path.stat().st_size
        expected_parts = math.ceil(file_size / request.part_size)
        
        if len(request.presigned_urls) != expected_parts:
            raise HTTPException(
                status_code=400,
                detail=f"Number of presigned URLs ({len(request.presigned_urls)}) does not match expected parts ({expected_parts})"
            )
        
        results = await upload_parts_to_presigned_url(str(file_path), request.presigned_urls, request.part_size)
        
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful
        
        response = MultipartUploadResponse(
            status="success" if failed == 0 else "partial_success",
            message="All parts uploaded successfully" if failed == 0 else f"Uploaded {successful}/{len(results)} parts successfully",
            file_name=file_path.name,
            parts_results=results,
            successful_parts=successful,
            failed_parts=failed
        )
        
        if failed > 0:
            return response, 206
            
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in multipart upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/file/download")
async def download_files(request: DownloadRequest):
    """
    Batch download files endpoint
    Request body:
    {
        "files": [
            {
                "url": "https://example.com/file1.pdf",
                "filename": "file1.pdf"
            },
            ...
        ],
        "folder_path": "download/path"
    }
    """
    try:
        results = []
        
        async def download_file(client, item):
            file_name = os.path.basename(item.filename)
            base_path = Path(DEFAULT_WORKING_DIR) / 'download'
            target_path = base_path
            
            if hasattr(request, "folder_path") and request.folder_path:
                subfolder = request.folder_path.strip('/')
                target_path = os.path.join(base_path, subfolder)
            
            os.makedirs(target_path, exist_ok=True)
            file_path = os.path.join(target_path, file_name)
            
            try:
                response = await client.get(item.url)
                if response.status_code != 200:
                    return DownloadResult(
                        filename=file_name, 
                        success=False,
                        error=f"HTTP {response.status_code}"
                    )
                
                content = response.read()
                with open(file_path, 'wb') as f:
                    f.write(content)
                
                return DownloadResult(filename=file_name, file_path=file_path, success=True)
            except Exception as e:
                return DownloadResult(
                    filename=file_name, 
                    success=False, 
                    error=str(e)
                )
        
        async with httpx.AsyncClient() as client:
            tasks = [download_file(client, item) for item in request.files]
            results = await asyncio.gather(*tasks)
        
        success_count = sum(1 for r in results if r.success)
        fail_count = len(results) - success_count
        
        return {
            "status": "completed",
            "total": len(results),
            "success_count": success_count,
            "fail_count": fail_count,
            "results": results
        }
    except Exception as e:
        logger.error(f"Error in batch download: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/file")
async def get_file(path: str):
    """
    Download file endpoint
    Query params:
        path: str - The file path to download
    """
    try:
        path = Path(path).resolve()
        file_path = Path(DEFAULT_WORKING_DIR) / path.relative_to('/')
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        if not file_path.is_file():
            raise HTTPException(status_code=400, detail="Path is not a file")
        
        return FileResponse(
            path=str(file_path),
            filename=file_path.name,
            media_type="application/octet-stream"
        )
    except Exception as e:
        logger.error(f"Error serving file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/dir/upload")
async def zip_dir(request: ZipAndUploadRequest):
    """
    Zip a directory (excluding node_modules) and upload to presigned_url
    Request body:
    {
        "directory": "/path/to/directory",
        "presigned_url": string
    }
    """
    try:
        # Check if directory exists
        if not os.path.exists(request.directory):
            return ZipAndUploadResponse(
                status="error",
                message="Directory not found",
                error=f"Directory {request.directory} does not exist"
            ).model_dump()
        
        # Get the project name from the directory
        project_name = os.path.basename(request.directory.rstrip('/'))
        
        # Path for the output zip file
        output_zip = f"/tmp/{project_name}.zip"
        
        # Create the zip archive
        success, message = create_zip_archive(request.directory, output_zip)
        
        if not success:
            return ZipAndUploadResponse(
                status="error",
                message="Failed to create zip file",
                error=message
            ).model_dump()
        
        if not os.path.exists(output_zip):
            return ZipAndUploadResponse(
                status="error",
                message="Zip file was not created",
                error="Zip operation failed"
            ).model_dump()
        
        # Upload the zip to presigned_url
        async with httpx.AsyncClient() as client:
            with open(output_zip, 'rb') as f:
                response = await client.put(
                    request.presigned_url,
                    content=f.read(),
                    headers={'Content-Type': 'application/zip'}
                )
                
            if response.status_code not in (200, 201):
                return ZipAndUploadResponse(
                    status="error",
                    message="Failed to upload to presigned_url",
                    error=f"Upload failed with status {response.status_code}: {response.text}"
                ).model_dump()
        
        # Clean up
        os.remove(output_zip)
        
        return ZipAndUploadResponse(
            status="success",
            message=f"Successfully processed {request.project_type} project and uploaded to presigned_url"
        ).model_dump()
    except Exception as e:
        logger.error(f"Error in zip-and-upload: {str(e)}")
        
        return ZipAndUploadResponse(
            status="error",
            message="Internal server error",
            error=str(e)
        ).model_dump()

# Initialize browser manager
browser_manager = BrowserManager(headless=False)

@app.get("/browser/status")
async def browser_status():
    """Endpoint for browser status"""
    try:
        tabs = await browser_manager.health_check()
        return {"healthy": True, "tabs": tabs}
    except BrowserDeadError as e:
        logger.error(f"Browser Error: {e}")
        return {"healthy": False, "tabs": []}

@app.post("/browser/action")
async def browser_action(cmd: BrowserActionRequest = Body()):
    """Endpoint for browser action"""
    async def execute_with_retry():
        timeout = 60
        try:
            return await asyncio.wait_for(
                browser_manager.execute_action(cmd),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            error_msg = f"Browser action timed out after {timeout}s, new tab created and opened target:blank."
            logger.error(error_msg)
            await browser_manager.recreate_page()
            raise PageDeadError(error_msg)
    
    try:
        logger.info(f"start handling browser action {repr(cmd)}")
        result = await execute_with_retry()
        
        logger.info("\n".join([
            "Browser action result:",
            "title: " + result.title,
            "url: " + result.url,
            "result: " + result.result
        ]))
        
        return BrowserActionResponse(
            status="success",
            result=result,
            error=None
        ).model_dump()
    except PageDeadError as e:
        await browser_manager.recreate_page()
        logger.error(e)
        return BrowserActionResponse(
            status="error",
            result=None,
            error=str(e)
        ).model_dump()
    except Exception as e:
        logger.error(f"Browser Error: {e}")
        return BrowserActionResponse(
            status="error",
            result=None,
            error=str(e)
        ).model_dump()

@app.post("/text_editor/dir")
@handle_text_editor_errors
async def text_editor_dir(cmd: TextEditorDirRequest):
    return await text_editor.dir(cmd.path)

@app.post("/text_editor/view")
@handle_text_editor_errors
async def text_editor_view(cmd: TextEditorViewRequest):
    return await text_editor.view(cmd.path, cmd.view_range, cmd.sudo)

@app.post("/text_editor/create")
@handle_text_editor_errors
async def text_editor_create(cmd: TextEditorCreateRequest):
    return await text_editor.create(cmd.path, cmd.file_text, cmd.sudo)

@app.post("/text_editor/write")
@handle_text_editor_errors
async def text_editor_write(cmd: TextEditorWriteRequest):
    return await text_editor.write(cmd.path, cmd.file_text, cmd.sudo, cmd.append, cmd.trailing_newline, cmd.leading_newline)

@app.post("/text_editor/replace")
@handle_text_editor_errors
async def text_editor_replace(cmd: TextEditorStrReplaceRequest):
    return await text_editor.replace(cmd.path, cmd.old_str, cmd.new_str, cmd.sudo)

@app.post("/text_editor/find_content")
@handle_text_editor_errors
async def text_editor_find_content(cmd: TextEditorFindContentRequest):
    return await text_editor.find_content(cmd.path, cmd.regex, cmd.sudo)

@app.post("/text_editor/find_file")
@handle_text_editor_errors
async def text_editor_find_file(cmd: TextEditorFindFileRequest):
    return await text_editor.find_file(cmd.path, cmd.glob)

@app.post("/text_editor/move")
@handle_text_editor_errors
async def text_editor_move(cmd: TextEditorMoveRequest):
    return await text_editor.move(cmd.path, cmd.new_path, cmd.sudo)

@app.post("/text_editor/delete")
@handle_text_editor_errors
async def text_editor_delete(cmd: TextEditorDeleteRequest):
    return await text_editor.delete(cmd.path, cmd.sudo)

@app.websocket("/terminal")
async def websocket_endpoint(ws: WebSocket):
    await terminal_socket_server.handle_connection(ws)

@app.websocket("/vnc")
async def vnc_websocket_endpoint(ws: WebSocket):
    """WebSocket endpoint for VNC connections"""
    await ws.accept()
    logger.info("New VNC WebSocket connection established")
    
    try:
        # Connect to the VNC server
        reader, writer = await asyncio.open_connection('localhost', 5900)
        
        async def forward_to_vnc():
            try:
                while True:
                    data = await ws.receive_bytes()
                    writer.write(data)
                    await writer.drain()
            except Exception as e:
                logger.error(f"Error forwarding to VNC: {e}")
                writer.close()
                await writer.wait_closed()
        
        async def forward_from_vnc():
            try:
                while True:
                    data = await reader.read(65536)  # 64KB buffer for VNC data
                    if not data:
                        break
                    await ws.send_bytes(data)
            except Exception as e:
                logger.error(f"Error forwarding from VNC: {e}")
                writer.close()
                await writer.wait_closed()
        
        # Start forwarding tasks
        to_vnc = asyncio.create_task(forward_to_vnc())
        from_vnc = asyncio.create_task(forward_from_vnc())
        
        # Wait for either task to complete
        done, pending = await asyncio.wait(
            [to_vnc, from_vnc],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        # Cancel pending tasks
        for task in pending:
            task.cancel()
        
        # Wait for tasks to be cancelled
        await asyncio.gather(*pending, return_exceptions=True)
        
    except Exception as e:
        logger.error(f"VNC WebSocket error: {e}")
    finally:
        await ws.close()
        logger.info("VNC WebSocket connection closed")

@app.post("/terminal/{terminal_id}/reset")
async def reset_terminal(terminal_id: str):
    try:
        terminal = await terminal_manager.create_or_get_terminal(terminal_id)
        await terminal.reset()
        return TerminalApiResponse(
            status="success",
            result="terminal reset success",
            terminal_id=terminal_id,
            output=[]
        ).model_dump()
    except Exception as e:
        logger.error(f"Error resetting terminal: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/terminal/reset-all")
async def reset_all_terminals():
    try:
        for terminal in terminal_manager.terminals.values():
            await terminal.reset()
        
        return TerminalApiResponse(
            status="success",
            result="all terminals reset success",
            terminal_id="",
            output=[]
        ).model_dump()
    except Exception as e:
        logger.error(f"Error resetting all terminals: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/terminal/{terminal_id}/view")
async def view_terminal(terminal_id: str, full: bool = Query(True)):
    try:
        terminal = await terminal_manager.create_or_get_terminal(terminal_id)
        history = terminal.get_history(True, full)
        
        return TerminalApiResponse(
            status="success",
            result="terminal view success",
            terminal_id=terminal_id,
            output=history
        ).model_dump()
    except Exception as e:
        logger.error(f"Error viewing terminal: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/terminal/{terminal_id}/kill")
async def kill_terminal_process(terminal_id: str):
    try:
        terminal = await terminal_manager.create_or_get_terminal(terminal_id)
        await terminal.kill_process()
        
        history = terminal.get_history(True, False)
        
        return TerminalApiResponse(
            status="success",
            result="terminal process killed",
            terminal_id=terminal_id,
            output=history
        ).model_dump()
    except Exception as e:
        logger.error(f"Error killing terminal process: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/terminal/{terminal_id}/write")
async def write_terminal_process(terminal_id: str, cmd: TerminalWriteApiRequest):
    try:
        terminal = await terminal_manager.create_or_get_terminal(terminal_id)
        await terminal.write_to_process(cmd.text, cmd.enter if cmd.enter is not None else False)
        
        # Allow time for the process to respond
        await asyncio.sleep(1)
        
        history = terminal.get_history(True, False)
        
        return TerminalApiResponse(
            status="success",
            result="write terminal process success",
            terminal_id=terminal_id,
            output=history
        ).model_dump()
    except Exception as e:
        logger.error(f"Error killing terminal process: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class InitSandboxRequest(BaseModel):
    secrets: Dict[str, str]

@app.post("/init-sandbox")
async def init_sandbox(request: InitSandboxRequest):
    """初始化沙箱环境  # Initialize sandbox environment

    接收 secrets 并写入到用户的 .secrets 目录下，每个 secret 作为单独的文件  # Receive secrets and write them to the user's .secrets directory, each secret as a separate file
    - secrets 目录会在 $HOME/.secrets 下创建  # The secrets directory will be created under $HOME/.secrets
    - 每个 secret 的 key 作为文件名  # Each secret's key is used as the filename
    - 如果文件已存在且内容不同，会将原文件备份（添加时间戳后缀）  # If the file already exists with different content, the original file will be backed up (with a timestamp suffix)

    Args:
        request: InitSandboxRequest containing secrets dictionary

    Returns:
        Dict with status and processed files info

    Raises:
        HTTPException: If HOME environment variable is not set or other errors
    """
    try:
        home_dir = os.getenv('WORKDIR')
        if not home_dir:
            raise HTTPException(status_code=500, detail="HOME environment variable is not set")
            
        secrets_dir = os.path.join(home_dir, '.secrets')
        
        # Create secrets directory if it doesn't exist
        os.makedirs(secrets_dir, exist_ok=True)
        os.chmod(secrets_dir, 0o700)  # rwx------
        
        processed_files = []
        
        for key, value in request.secrets.items():
            secret_file = os.path.join(secrets_dir, key)
            
            if os.path.exists(secret_file):
                try:
                    with open(secret_file, 'r') as f:
                        current_content = f.read()
                    
                    if current_content == value:
                        processed_files.append({
                            'key': key,
                            'action': 'skipped',
                            'reason': 'content unchanged'
                        })
                        continue
                    
                    if current_content != value:
                        # Backup the existing file with timestamp
                        timestamp = time.strftime('%Y%m%d_%H%M%S')
                        backup_file = f"{secret_file}.{timestamp}"
                        os.rename(secret_file, backup_file)
                        processed_files.append({
                            'key': key,
                            'action': 'backed_up',
                            'backup_file': backup_file
                        })
                except Exception as e:
                    logger.error(f"Error reading existing secret file {key}: {e}")
                    raise HTTPException(status_code=500, detail=f"Failed to process existing secret file {key}: {str(e)}")
            
            try:
                with open(secret_file, 'w') as f:
                    f.write(value)
                
                os.chmod(secret_file, 0o600)  # rw-------
                
                processed_files.append({
                    'key': key,
                    'action': 'updated' if os.path.exists(secret_file) else 'created'
                })
            except Exception as e:
                logger.error(f"Error writing secret file {key}: {e}")
                raise HTTPException(status_code=500, detail=f"Failed to write secret file {key}: {str(e)}")
        
        return {
            'status': 'ok',
            'secrets_dir': secrets_dir,
            'processed_files': processed_files
        }
    except Exception as e:
        logger.error(f"Error processing secrets: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process secrets: {str(e)}")

@app.get("/healthz")
async def healthz():
    """Health check endpoint."""
    # If browser is set to start automatically, create the task but don't await it
    if browser_manager.status == "started":
        asyncio.create_task(browser_manager.initialize())
    
    return {"status": "ok"}

def create_zip_archive(source_dir: str, output_zip: str) -> tuple[bool, str]:
    '''
    Create a zip archive of a directory, excluding node_modules and .next

    Args:
        source_dir: Path to the directory to zip
        output_zip: Path for the output zip file

    Returns:
        tuple[bool, str]: (success, error_message)
    '''
    try:
        source_path = Path(source_dir).resolve()
        if not source_path.is_dir():
            return (False, f"Directory '{source_dir}' does not exist")
        
        if not output_zip.endswith('.zip'):
            output_zip += '.zip'
            
        exclude_patterns = [
            'node_modules',
            '.next',
            '.open-next',
            '.turbo',
            '.wrangler',
            '.git',
            '.vnc'
        ]
        
        def copy_files(src, dst, ignores=exclude_patterns):
            for item in os.listdir(src):
                if item in ignores:
                    continue
                    
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                
                if os.path.isdir(s):
                    shutil.copytree(s, d, ignore=lambda x, y: ignores)
                else:
                    shutil.copy2(s, d)
        
        # Create a temporary directory for the archive
        with tempfile.TemporaryDirectory() as temp_dir:
            source_copy = os.path.join(temp_dir, 'source')
            os.makedirs(source_copy)
            
            # Copy files to the temporary directory, excluding patterns
            copy_files(str(source_path), source_copy)
            
            # Create the zip archive
            shutil.make_archive(output_zip[:-4], 'zip', source_copy)
        
        return (True, '')
    except Exception as e:
        return (False, f"Failed to create zip archive: {str(e)}")