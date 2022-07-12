import win32gui
from time import sleep

_id_ = None

"""
获取所有窗口
"""
def get_all_windows():
    hWnd_list = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWnd_list)
    return hWnd_list

"""获取所有标题"""
def get_title(hwnd):
    title = win32gui.GetWindowText(hwnd)
    return title

"""窗口名获取到句柄"""
def get_hwnd_from_name(name):
    hWnd_list = get_all_windows()
    for hwd in hWnd_list:
        title = get_title(hwd)
        if title == name:
            return hwd

# hwnd = win32gui.FindWindow("Progman", "Program Manager")
"""窗口发信息"""
def pretreatmentHandle():
    hwnd = win32gui.FindWindow("Progman", "Program Manager")
    win32gui.SendMessageTimeout(hwnd, 0x052C, 0, None, 0, 0x03E8)
    hwnd_WorkW = None
    while 1:
        hwnd_WorkW = win32gui.FindWindowEx(None, hwnd_WorkW, "WorkerW", None)
        # print('hwmd_workw: ', hwnd_WorkW)
        if not hwnd_WorkW:
            continue
        hView = win32gui.FindWindowEx(hwnd_WorkW, None, "SHELLDLL_DefView", None)
        # print('hwmd_hView: ', hView)
        if not hView:
            continue
        h = win32gui.FindWindowEx(None, hwnd_WorkW, "WorkerW", None)
        # print('h_1: ',h)
        while h:
            win32gui.SendMessage(h, 0x0010, 0, 0)  # WM_CLOSE
            h = win32gui.FindWindowEx(None, hwnd_WorkW, "WorkerW", None)
            # print(h)
        break
    return hwnd

def FindIS(HWND):
    for hwdn in get_all_windows():
        if HWND == hwdn:
            return True
            break
        else:
            return False
            continue


"""窗口创建子窗口"""
def main(WINDOWS, SleepTime):
    global _id_
    while True:
        HWND = get_hwnd_from_name(WINDOWS)
        if HWND:
            _id_ = HWND
            sleep(SleepTime)
            win32gui.SetParent(HWND, pretreatmentHandle())
            break
        else:
            continue