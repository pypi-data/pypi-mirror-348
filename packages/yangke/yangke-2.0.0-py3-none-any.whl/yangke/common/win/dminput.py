# dm_ret = dm.BindWindowEx(hwnd,"dx.graphic.opengl","dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.clip.lock.api|dx.mouse.input.lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor","windows","dx.public.active.api|dx.public.active.message|dx.public.hide.dll|dx.public.active.api2|dx.public.anti.api|dx.public.km.protect|dx.public.inject.super|dx.public.memory|dx.public.inject.c",11)
# 本模块只能使用32位python调用
import time

import requests

from yangke.common.config import logger
from yangke.core import runCMD
import win32com.client
import ctypes
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn

dm = None


# http://localhost:8888/SetKey/mmdlljafd8c5cbf193e99306e9eb61ceb5bd44/ewdSEKFZP

# http://localhost:8888/Bind/
class DMRemote:
    def __init__(self, key="mmdlljafd8c5cbf193e99306e9eb61ceb5bd44", add_key="ewdSEKFZP", port=8765):
        if add_key is None:
            add_key = ""
        try:
            # res = runCMD(
            #     f'C:\\Users\\54067\\PycharmProjects\\RestDmMouseKey\\dist\\RestDM.exe "{key}" "{add_key}" {port}',
            #     wait_for_result=False)
            # # logger.debug(res)
            ...
        except:
            logger.warning(f"自动启动RestDM.exe失败，请确保该应用正常运行！")
        self.port = port
        self.success = False
        self.error_info = ""
        res = self.Reg()
        if res.startswith("success"):
            logger.debug("ykdamo加载成功！")
            self.success = True
        else:
            self.error_info = res

    def Reg(self, key=None, add_key=None):
        if key is None:
            key = "null"
            add_key = "null"
        try:
            res = requests.get(url=f"http://localhost:{self.port}/Reg/{key}/{add_key}")
        except requests.exceptions.ConnectionError:
            return "error: 请求无响应，请检查端口号是否正确"
        return res.text

    def DmGuard(self, enable, type_="memory4"):
        """
        开启打磨防护盾
        """
        res = requests.get(url=f"http://localhost:{self.port}/DmGuard/{type_}")
        return res.text

    def bind_window(self,
                    hwnd,
                    display="gdi2",
                    mouse="dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.clip.lock.api|dx.mouse.input.lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor",
                    keypad="windows",
                    public="",
                    mode=11):
        """
        设置大漠的窗口绑定方式，参考BindWindow参数说明
        dm_ret = dm.BindWindowEx(hwnd,"gdi2","dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.clip.lock.api|dx.mouse.input.lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor","windows","",11)

        """
        if isinstance(mode, str) and ":" in mode:
            mode = int(mode.split(":")[0])
        params = {
            "hwnd": hwnd,
            "display": display,
            "mouse": mouse,
            "keypad": keypad,
            "public": public,
            "mode": mode
        }
        # res = requests.post(url=f"http://localhost:{self.port}/BindWindow/", params=params)
        res = requests.get(url=f"http://localhost:{self.port}/BindWindow/", params=params)
        return res.text

    def unbind_window(self):
        _ = requests.get(url=f"http://localhost:{self.port}/UnBindWindow/")
        return _.text

    def get_bind_window(self):
        _ = requests.get(url=f"http://localhost:{self.port}/GetBindWindow/")
        return _.text

    def press_key(self, key):
        """
        按键
        """
        if "+" in key and len(key) >= 3:  # ctrl+c
            keys = key.split("+")
            if len(keys) == 2 and keys[0].lower() in ["ctrl", "alt", "shift"] and keys[1].lower() not in ["ctrl", "alt",
                                                                                                          "shift"]:
                requests.get(url=f"http://localhost:{self.port}/KeyDownChar/{keys[0].lower()}")
                requests.get(url=f"http://localhost:{self.port}/KeyDownChar/{keys[1].lower()}")
                time.sleep(0.02)
                requests.get(url=f"http://localhost:{self.port}/KeyUpChar/{keys[1].lower()}")
                res = requests.get(url=f"http://localhost:{self.port}/KeyUpChar/{keys[0].lower()}")
                return res.text
            else:
                logger.warning(f"暂不支持三个键的组合键，当前按键为{key}，已忽略")
        else:
            params = {
                "key": key
            }
            return requests.get(url=f"http://localhost:{self.port}/KeyPressChar/", params=params).text

    def key_down(self, key):
        """
        按下键盘按键
        """
        return requests.get(url=f"http://localhost:{self.port}/KeyDownChar/{key.lower()}")

    def key_up(self, key):
        """
        按下键盘按键
        """
        return requests.get(url=f"http://localhost:{self.port}/KeyUpChar/{key.lower()}")

    def left_click(self, x, y):
        params = {
            "x": x,
            "y": y,
        }
        res = requests.get(url=f"http://localhost:{self.port}/MoveTo", params=params)
        res = requests.get(url=f"http://localhost:{self.port}/LeftClick/")
        return res.text

    def left_down(self, x, y):
        params = {
            "x": x,
            "y": y,
        }
        res = requests.get(url=f"http://localhost:{self.port}/MoveTo", params=params)
        res = requests.get(url=f"http://localhost:{self.port}/LeftDown/")
        return res.text

    def left_up(self, x, y):
        params = {
            "x": x,
            "y": y,
        }
        res = requests.get(url=f"http://localhost:{self.port}/MoveTo", params=params)
        res = requests.get(url=f"http://localhost:{self.port}/LeftUp/")
        return res.text

    def right_click(self, x, y):
        params = {
            "x": x,
            "y": y,
        }
        res = requests.get(url=f"http://localhost:{self.port}/MoveTo", params=params)
        res = requests.get(url=f"http://localhost:{self.port}/RightClick/", params=params)
        return res.text

    def right_down(self, x, y):
        params = {
            "x": x,
            "y": y,
        }
        res = requests.get(url=f"http://localhost:{self.port}/MoveTo", params=params)
        res = requests.get(url=f"http://localhost:{self.port}/RightDown/", params=params)
        return res.text

    def right_up(self, x, y):
        params = {
            "x": x,
            "y": y,
        }
        res = requests.get(url=f"http://localhost:{self.port}/MoveTo", params=params)
        res = requests.get(url=f"http://localhost:{self.port}/RightUp/", params=params)
        return res.text

    def move_to(self, x, y):
        res = requests.get(url=f"http://localhost:{self.port}/MoveTo/{x}/{y}")
        return res.text

    def get_cursor_pos(self):
        res = requests.get(url=f"http://localhost:{self.port}/GetCursorPos")
        x, y = eval(res.text)
        return x, y

    def drag_to(self, from_point, to_point, button="left"):
        params = {
            "x1": from_point[0],
            "y1": from_point[1],
            "x2": to_point[0],
            "y2": to_point[1],
            "button": button
        }
        res = requests.post(url=f"http://localhost:{self.port}/Drag/", params=params)
        print(res)

    def capture(self, x1, y1, x2, y2, save_file):
        """
        截图
        """
        try:
            return requests.get(url=f"http://localhost:{self.port}/Capture/{save_file}/{x1}/{y1}/{x2}/{y2}")
        except Exception as e:
            logger.debug(f"连接断开，请检查WebDM.exe是否运行")
            logger.error(e)


class DM:
    def __init__(self, key="mmdlljafd8c5cbf193e99306e9eb61ceb5bd44", add_key="ewdSEKFZP"):
        self.dm = None
        self.key = key
        self.add_key = add_key
        self.bind_mode: list | None = None
        self.load_dm()
        self.is_bind = False

    def load_dm(self):
        try:
            self.dm = win32com.client.Dispatch('dm.dmsoft')
            print('本机系统中已经安装大漠插件，版本为:', self.dm.ver())
        except:
            print('本机并未安装大漠，正在免注册调用')
            dms = ctypes.windll.LoadLibrary(r'E:\安装文件\dm\dm\7.2336/DmReg.dll')
            location_dmreg = r'E:\安装文件\dm\dm\7.2336/dm.dll'
            dms.SetDllPathW(location_dmreg, 0)
            self.dm = win32com.client.Dispatch('dm.dmsoft')

            # dm = CreateObject('dm.dmsoft')
            print('免注册调用成功 版本号为:', self.dm.Ver())

            res = self.dm.Reg(self.key, self.add_key)
            if res == 1:
                print('大漠注册成功！')
            elif res == -1:
                logger.error("大漠插件无法连接网络")
            elif res == -2:
                logger.error("进程没有以管理员方式运行. (出现在win7 win8 vista 2008.建议关闭uac)")
            elif res == 2:
                logger.error("大漠余额不足")
            elif res == 3:
                logger.error("绑定了本机器，但是账户余额不足50元.")
            elif res == 4:
                logger.error("注册码错误")
            elif res == 5:
                logger.error("你的机器或者IP在黑名单列表中或者不在白名单列表中")
            elif res == 6:
                logger.error(
                    "非法使用插件. 一般出现在定制插件时，使用了和绑定的用户名不同的注册码.  也有可能是系统的语言设置不是中文简体,也可能有这个错误.")
            elif res == 7:
                logger.error(
                    "你的帐号因为非法使用被封禁. （如果是在虚拟机中使用插件，必须使用Reg或者RegEx，不能使用RegNoMac或者RegExNoMac,否则可能会造成封号，或者封禁机器）")
            elif res == 8:
                logger.error("ver_info不在你设置的附加白名单中.")

    def DmGuard(self, enable, type_="memory4"):
        res = self.dm.DmGuard(1, "memory4")
        if res == 1:
            print("大漠防护盾开启成功")
        else:
            logger.warning(f"大漠防护盾开启失败，错误码：{res}")

    def set_bindmode(self, display="dx.graphic.opengl",
                     mouse="dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.clip.lock.api|"
                           "dx.mouse.input.lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor",
                     keypad="windows",
                     public="dx.public.active.api|dx.public.active.message|dx.public.hide.dll|dx.public.active.api2|dx."
                            "public.anti.api|dx.public.km.protect|dx.public.inject.super|dx.public.memory|"
                            "dx.public.inject.c",
                     mode=11):
        """
        设置大漠的窗口绑定方式，参考BindWindow参数说明
        """
        self.bind_mode = [display, mouse, keypad, public, mode]

    def bind_window(self, hwnd):
        if self.dm is None:
            self.load_dm()
        res = self.dm.BindWindowEx(hwnd, self.bind_mode[0], self.bind_mode[1], self.bind_mode[2], self.bind_mode[3],
                                   self.bind_mode[4])
        if res == 1:
            self.is_bind = True
        else:
            code = self.dm.GetLastError()
            logger.error(f"大漠绑定窗口失败，错误码：{code}")

    def press_key(self, key):
        """
        按键
        """
        self.dm.KeyPress(key)

    def left_click(self, x, y):
        self.dm.LeftClick(x, y)

    def right_click(self, x, y):
        self.dm.RightClick(x, y)


class ThreadXMLRpcServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


def click(x, y, right=False):
    if right:
        dm.right_click(x, y)
    else:
        dm.left_click(x, y)


def start_rpc_server():
    server = ThreadXMLRpcServer(("localhost", 8888))
    server.register_function(click, "click")
    server.serve_forever()


def start_dm_server(window_hwnd, display, mouse, keypad, public, mode):
    global dm
    dm = DM()
    dm.set_bindmode(display, mouse, keypad, public, mode)
    dm.bind_window(window_hwnd)
    start_rpc_server()


if __name__ == "__main__":
    start_dm_server()
