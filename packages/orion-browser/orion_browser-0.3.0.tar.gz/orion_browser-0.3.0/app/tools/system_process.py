import os
import subprocess
import time
import platform
from pathlib import Path
from app.logger import logger

class SystemProcessManager:
    def __init__(self):
        self.processes = []
        self.display = ":199"  # Use virtual display
        self.is_linux = platform.system().lower() == "linux"
        if self.is_linux:
            os.environ["DISPLAY"] = self.display
        
    def setup_fcitx_config(self):
        """Setup fcitx configuration"""
        if not self.is_linux:
            return
            
        config_dir = Path.home() / ".config" / "fcitx"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_content = "[Profile]\nIMName=googlepinyin\nEnabledIMList=fcitx-keyboard-us:True,googlepinyin:True"
        
        try:
            with open(config_dir / "profile", "w") as f:
                f.write(config_content)
            logger.info("Fcitx configuration written successfully")
        except Exception as e:
            logger.error(f"Failed to write fcitx configuration: {e}")
        
    def start_xvfb(self):
        """Start Xvfb virtual display server"""
        cmd = ["Xvfb", self.display, "-screen", "0", "1600x900x24", "-ac", "-noreset"]
        process = subprocess.Popen(cmd)
        self.processes.append(process)
        time.sleep(2)  # Wait for Xvfb to start
        
    def start_x11vnc(self):
        """Start x11vnc server"""
        cmd = [
            "x11vnc",
            "-display", self.display,
            "-forever",
            "-shared",
            "-noxkb",
            "-noxdamage",
            "-rfbport", "5900",
            "-rfbauth", os.path.expanduser("~/.vnc/passwd")
        ]
        process = subprocess.Popen(cmd)
        self.processes.append(process)
        time.sleep(2)  # Wait for x11vnc to start
        
    def start_fcitx(self):
        """Start fcitx input method"""
        self.setup_fcitx_config()
        process = subprocess.Popen(["fcitx"])
        self.processes.append(process)
        
    def start_all(self):
        """Start all required system processes"""
        if not self.is_linux:
            logger.info("Not running on Linux, skipping system processes")
            return
            
        self.start_xvfb()
        self.start_x11vnc()
        self.start_fcitx()
        
    def cleanup(self):
        """Cleanup all processes"""
        if not self.is_linux:
            return
            
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                logger.error(f"Error cleaning up process: {e}") 