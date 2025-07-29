import pygetwindow as gw


def activate_wnd(wnd: gw.Win32Window):
    try:
        wnd.activate()
    except gw.PyGetWindowException as e:
        if e.args[0].startswith("Error code from Windows: 0"):
            return

        raise e
