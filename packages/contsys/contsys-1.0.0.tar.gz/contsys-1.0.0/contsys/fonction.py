import subprocess
import os
import sys

class fonction:
    #CMD
    @staticmethod
    def clear():
        if sys.platform=='win32':
            subprocess.run('cls', shell=True)
        elif sys.platform=='linux':
            subprocess.run('clear', shell=True)

    @staticmethod
    def title(title):
        if sys.platform=='win32':
            subprocess.run(f'title {title}', shell=True)
        if sys.platform=='linux':
            subprocess.run(f'echo -ne "\033]0;{title}\007"', shell=True)
    
    #SYSTEM
    @staticmethod
    def iswin32():
        if sys.platform == 'win32':
            return True
        else:
            return False
    
    @staticmethod
    def islinux():
        if sys.platform == 'linux':
            return True
        else:
            return False
    
    @staticmethod
    def isdarwin():
        if sys.platform == 'darwin':
            return True
        else:
            return False

    @staticmethod
    def recupmode():
        if sys.platform=='win32':
            subprocess.run('shutdown.exe /r /o /f /t 0', shell=True)
        else:
            print('Only work on windows.')
    
    @staticmethod
    def reboot():
        if sys.platform=='win32':
            subprocess.run('shutdown /r /t 0', shell=True)
        elif sys.platform=='linux' or sys.platform=='darwin':
            subprocess.run('shutdown -r now', shell=True)