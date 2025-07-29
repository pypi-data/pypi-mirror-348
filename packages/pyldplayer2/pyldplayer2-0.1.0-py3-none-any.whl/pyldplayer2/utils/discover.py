import os
from warnings import warn

from pyldplayer2.base.objects.appattr import AppAttr


def discover_process():
    import psutil

    for proc in psutil.process_iter():
        try:
            if proc.name() == "dnplayer.exe":
                return os.path.abspath(os.path.dirname(proc.exe()))
            if "dn" in proc.name():
                path = os.path.abspath(os.path.dirname(proc.exe()))
                counter = 0
                while True:
                    contents = os.listdir(path)
                    if "dnplayer.exe" in contents:
                        return path
                    elif "LDPlayer" in contents:
                        path = os.path.join(path, "LDPlayer")
                    else:
                        path = os.path.dirname(path)
                    counter += 1
                    if counter > 5:
                        warn("Failed to find dnplayer.exe")
                        break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def discover_dotenv():
    try:
        from dotenv import load_dotenv

        load_dotenv()
        return os.getenv("LDPATH")
    except Exception:
        return None


def discover():
    path = os.environ.get("LDPATH", None) or discover_dotenv() or discover_process()
    if path:
        AppAttr(path)
