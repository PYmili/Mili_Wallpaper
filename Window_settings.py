import win32gui
import win32con
from time import sleep

_id_ = None

"""窗口名获取到句柄"""
def get_hwnd_from_name(name):
    hWnd_list = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWnd_list)

    for hwnd in hWnd_list:
        title = win32gui.GetWindowText(hwnd)
        if title == name:
            return hwnd
        else:
            continue


"""
FindWindow Porgman Program Manager
SendMessageTimeout 0x052C Message
向桌面窗口WorkerW下的 Porman Program Manager窗口发送 0x052C信息，分裂出新的WorkerW
"""
def pretreatmentHandle() -> int:
    # hwnd = win32gui.FindWindow("Progman", "Program Manager")
    Progman = win32gui.FindWindow("Progman", "Program Manager") # 查找PM窗口
    win32gui.SendMessageTimeout(
        Progman,
        0x052C,
        None,
        None,
        win32con.SMTO_NORMAL,
        1000
    ) # 发送0x052c信息
    WorkerW = None
    Workerw_WorkerW = 0
    while True:
        # 查找PM的主窗口 WorkerW
        WorkerW = win32gui.FindWindowEx(
            None,
            WorkerW,
            "WorkerW",
            None
        )
        print('WorkerW: ', WorkerW)
        if WorkerW == 0:
            continue

        # 确认WorkerW下有SHELLDLL_DefView窗口
        WorkerWhView = win32gui.FindWindowEx(
            WorkerW,
            None,
            "SHELLDLL_DefView",
            None
        )
        print('SHELLDLL_DefView: ', WorkerWhView)
        if WorkerWhView == 0:
            continue
        else:
            # 成功查找到WorkerW下的WorkerW窗口
            Workerw_WorkerW = win32gui.FindWindowEx(
                None,
                WorkerW,
                "WorkerW",
                None
            )
            print('WorkerW -> WorkerW: ', Workerw_WorkerW)
            break
        # while h:
            # win32gui.SendMessage(h, 0x0010, 0, 0)  # WM_CLOSE
    return Workerw_WorkerW

def FindIS(HWND) -> bool:
    hWnd_list = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWnd_list)

    for hwdn in hWnd_list:
        if HWND == int(hwdn):
            return True
        else:
            return False

"""
查看视频窗口是否存在
"""
def Isffmpeg(hwnd) -> bool:
    hWnd_list = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWnd_list)
    try:
        if hwnd in hWnd_list:
            return True
        else:
            return False
    except TypeError:
        return False
"""
设置视频窗口至WorkerW窗口子窗口
"""
def main(WindowsTitle: str, SleepTime) -> None:
    global _id_
    while True:
        _HWND = get_hwnd_from_name(WindowsTitle) # 获取视频窗口hwnd
        if _HWND:
            _id_ = _HWND
            sleep(SleepTime)
            win32gui.SetParent(_HWND, pretreatmentHandle()) # 设置子窗口
            break
        else:
            continue