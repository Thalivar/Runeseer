import os, platform, psutil
from datetime import datetime

def getOsName():
    uname = platform.uname()
    # Checks if the user is on windows
    if os.name == "nt":
        return f"{uname.system} {uname.release}"
    
    try:
        data = {}
        with open("/etc/os-release") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    data[k] = v.strip('"')
        
        return data.get("PRETTY_NAME", f"{uname.system} {uname.release}")    
    except (FileNotFoundError, PermissionError, OSError):
        return f"{uname.system} {uname.release}"
    
def uptimeSTR():
    bootTS = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()
    delta = now - bootTS
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    mins, _ = divmod(rem, 60)
    return f"{days} Days {hours}:{mins:02d} Hours"

def getSystemInfo():
    uname = platform.uname()
    osName = getOsName()

    mem = psutil.virtual_memory()
    diskRoot = "C:\\" if os.name == "nt" else "/"
    disk = psutil.disk_usage(diskRoot)

    cpuName = uname.processor or "CPU"
    cpuCores = psutil.cpu_count(logical = False) or "?"
    cpuThreads = psutil.cpu_count(logical = True) or "?"

    shell = (os.environ.get("SHELL") or os.environ.get("COMSPEC") or "unknown")
    shellName = shell.split("/")[-1].split("\\")[-1]

    batt = psutil.sensors_battery()
    if batt:
        battSTR = f"{batt.percent:.0f}% ({"AC" if batt.power_plugged else "battery"})"
    else:
        battSTR = "N/A"
    
    return {
        "userHost": f"{os.environ.get('USER') or os.environ.get('USERNAME') or 'unknown'}@{uname.node}", 
        "os": osName,
        "kernel": uname.release,
        "shell": shellName,
        "uptime": uptimeSTR(),
        "cpu": f"{cpuName} ({cpuCores}C/{cpuThreads}T)",
        "memoryUsed": mem.used,
        "memoryTotal": mem.total,
        "diskUsed": disk.used,
        "diskTotal": disk.total,
        "battery": battSTR,
    }