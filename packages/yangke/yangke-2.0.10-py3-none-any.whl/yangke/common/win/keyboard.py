import time

import win32con
import win32gui
import win32api
from ctypes import windll, byref
from ctypes.wintypes import HWND, POINT
import string
from yangke.common.QtImporter import Qt

dmCharKey = {  # dm插件的键名
    '\x1b': "esc",
    "\x08": "back",
    "\x09": "tab",
    "\x0d": "return",
    "\x10": "shift",
    "\x11": "control",
    "\x12": "menu",
    "\x14": "cap",
}

CodeToKey = {  # dm插件键码
    8: "backspace",
    9: "tab",
    13: "enter",
    16: "shift",
    17: "ctrl",
    18: "alt",
    20: "cap",  # 幽灵键鼠为"capslock"
    27: "esc",
    32: "space",
    33: "1",  # !
    34: "'",  # "
    35: "3",  # #
    36: "4",  # $
    37: "5",  # %
    38: "7",  # &
    39: "'",  # '
    40: "9",  # (
    41: "0",  # )
    42: "8",  # *
    43: "=",  # +
    44: ",",
    45: "-",
    46: ".",
    47: "/",
    48: "0",
    49: "1",
    50: "2",
    51: "3",
    52: "4",
    53: "5",
    54: "6",
    55: "7",
    56: "8",
    57: "9",
    58: ";",  # :
    59: ";",
    60: ",",  # <
    61: "=",
    62: ".",  # >
    63: "/",  # ?
    64: "2",  # 实际是@字符，但按键不考虑shift，一律认为@字符为2
    65: "A",
    66: "B",
    67: "C",
    68: "D",
    69: "E",
    70: "F",
    71: "G",
    72: "H",
    73: "I",
    74: "J",
    75: "K",
    76: "L",
    77: "M",
    78: "N",
    79: "O",
    80: "P",
    81: "Q",
    82: "R",
    83: "S",
    84: "T",
    85: "U",
    86: "V",
    87: "W",
    88: "X",
    89: "Y",
    90: "Z",
    91: "[",
    92: "\\",
    93: "]",  # option
    94: "6",  # ^
    95: "-",  # _
    96: "`",
    97: "a",
    98: "b",
    99: "c",
    100: "d",
    101: "e",
    102: "f",
    103: "g",
    104: "h",
    105: "i",
    106: "j",
    107: "k",
    108: "l",
    109: "m",
    110: "n",
    111: "o",
    112: "p",
    113: "q",
    114: "r",
    115: "s",
    116: "t",
    117: "u",
    118: "v",
    119: "w",
    120: "x",
    121: "y",
    122: "z",
    127: "delete",

}


VkCode = {
    '\x03': 0x03,  # PyQt6界面上按下Ctrl组合键时会产生该键码，意义未知
    "back": 0x08,
    '\x08': 0x08,  # PyQt传递的控制字符过来直接是控制字符的值，不是名称
    "tab": 0x09,
    '\x09': 0x09,
    "return": 0x0D,
    '\x0D': 0x0D,
    "shift": 0x10,
    "control": 0x11,
    "menu": 0x12,
    "pause": 0x13,
    "cap": 0x14,
    '\x14': 0x14,
    "escape": 0x1B,
    "esc": 0x1B,
    '\x1B': 0x1B,
    "space": 0x20,
    '\x20': 0x20,
    "end": 0x23,
    '\x23': 0x23,
    "home": 0x24,
    "\x24": 0x24,
    "left": 0x25,
    "\x25": 0x25,
    "up": 0x26,
    "\x26": 0x26,
    "right": 0x27,
    "\x27": 0x27,
    "down": 0x28,
    "\x28": 0x28,
    "print": 0x2A,
    '\x2A': 0x2A,
    "snapshot": 0x2C,
    "insert": 0x2D,
    '\x2D': 0x2D,
    "delete": 0x2E,
    '\x2E': 0x2E,
    "lwin": 0x5B,
    '\x5B': 0x5B,
    "rwin": 0x5C,
    '\x5C': 0x5C,
    "numpad0": 0x60,
    "numpad1": 0x61,
    "numpad2": 0x62,
    "numpad3": 0x63,
    "numpad4": 0x64,
    "numpad5": 0x65,
    "numpad6": 0x66,
    "numpad7": 0x67,
    "numpad8": 0x68,
    "numpad9": 0x69,
    "multiply": 0x6A,
    "add": 0x6B,
    "separator": 0x6C,
    "subtract": 0x6D,
    "decimal": 0x6E,
    "divide": 0x6F,
    "f1": 0x70,
    "f2": 0x71,
    "f3": 0x72,
    "f4": 0x73,
    "f5": 0x74,
    "f6": 0x75,
    "f7": 0x76,
    "f8": 0x77,
    "f9": 0x78,
    "f10": 0x79,
    "f11": 0x7A,
    "f12": 0x7B,
    "numlock": 0x90,
    "scroll": 0x91,
    "lshift": 0xA0,
    "rshift": 0xA1,
    "lcontrol": 0xA2,
    "rcontrol": 0xA3,
    "lmenu": 0xA4,
    "rmenu": 0XA5
}
PostMessageW = windll.user32.PostMessageW
MapVirtualKeyW = windll.user32.MapVirtualKeyW
VkKeyScanA = windll.user32.VkKeyScanA
ClientToScreen = windll.user32.ClientToScreen
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x202
WM_MOUSEWHEEL = 0x020A
WHEEL_DELTA = 120
WM_KEYDOWN = 0x100
WM_KEYUP = 0x101


def click_key(handle: HWND, key: str):
    """
    按下指定按键，测试成功

    Args:
        handle (HWND): 窗口句柄
        key (str): 按键名
    """
    vk_code = get_virtual_keycode(key)
    scan_code = MapVirtualKeyW(vk_code, 0)
    # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keydown
    wparam = vk_code
    lparam = (scan_code << 16) | 1
    PostMessageW(handle, WM_KEYDOWN, wparam, lparam)
    time.sleep(0.5)
    lparam = (scan_code << 16) | 0XC0000001
    PostMessageW(handle, WM_KEYUP, wparam, lparam)


def get_virtual_keycode(key: str):
    """根据按键名获取虚拟按键码

    Args:
        key (str): 按键名

    Returns:
        int: 虚拟按键码
    """
    if len(key) == 1 and key in string.printable:
        # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-vkkeyscana
        return VkKeyScanA(ord(key)) & 0xff  # ==ord(key)
    else:
        return VkCode[key]


import sys

if not windll.shell32.IsUserAnAdmin():
    # 不是管理员就提权
    windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, __file__, None, 1)
