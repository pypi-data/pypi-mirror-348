# 用于测量屏幕上鼠标点击位置的距离

import pyWinhook  # pip install pywinhook
from pyWinhook.HookManager import MouseEvent, KeyboardEvent
import pythoncom

from yangke.common.KeysTransfer import KeysTransfer
from yangke.common.config import logger


# collapse
def shield_hot_key():
    import PyHook3  # 先安装swig.exe，配置环境变量后，再安装pip install PyHook3

    hm = PyHook3.HookManager()

    # 鼠标事件处理函数
    def OnMouseEvent(event):
        print('MessageName:', event.MessageName)  # 事件名称
        print('Message:', event.Message)  # windows消息常量
        print('Time:', event.Time)  # 事件发生的时间戳
        print('Window:', event.Window)  # 窗口句柄
        print('WindowName:', event.WindowName)  # 窗口标题
        print('Position:', event.Position)  # 事件发生时相对于整个屏幕的坐标
        print('Wheel:', event.Wheel)  # 鼠标滚轮
        print('Injected:', event.Injected)  # 判断这个事件是否由程序方式生成，而不是正常的人为触发。
        print('---')

        # 返回True代表将事件继续传给其他句柄，为False则停止传递，即被拦截
        return True

    # 键盘事件处理函数
    def OnKeyboardEvent(event):
        print('MessageName:', event.MessageName)  # 同上，共同属性不再赘述
        print('Message:', event.Message)
        print('Time:', event.Time)
        print('Window:', event.Window)
        print('WindowName:', event.WindowName)
        print('Ascii:', event.Ascii, chr(event.Ascii))  # 按键的ASCII码
        print('Key:', event.Key)  # 按键的名称
        print('KeyID:', event.KeyID)  # 按键的虚拟键值
        print('ScanCode:', event.ScanCode)  # 按键扫描码
        print('Extended:', event.Extended)  # 判断是否为增强键盘的扩展键
        print('Injected:', event.Injected)
        print('Alt', event.Alt)  # 是某同时按下Alt
        print('Transition', event.Transition)  # 判断转换状态
        print('---')

        # 同上
        return False

    # 绑定事件处理函数
    # hm.MouseAllButtonsDown = OnMouseEvent  # 将OnMouseEvent函数绑定到MouseAllButtonsDown事件上
    hm.KeyDown = OnKeyboardEvent  # 将OnKeyboardEvent函数绑定到KeyDown事件上
    hm.KeyUp = OnKeyboardEvent

    # hm.HookMouse()  # 设置鼠标钩子
    hm.HookKeyboard()  # 设置键盘钩子

    # 循环获取消息
    pythoncom.PumpMessages()


class MouseKeyManager:
    keyIsPressed = False

    def __init__(self):
        """
        全局鼠标键盘响应事件
        """
        self.hm = pyWinhook.HookManager()
        self.on_key_event = None
        self.start_pos = None
        self.end_pos = None
        self.pressed_key = None
        self.dragging = False
        self.ignore_keys = set()

    def onKeyDown(self, event):
        print(f"按下键盘：{event.Key}")
        if self.keyIsPressed:
            return True
        self.keyIsPressed = True
        return True

    def onKeyUp(self, event):
        self.keyIsPressed = False
        print(str(event.Key) + ' is released')
        return True

    def mouseup(self, event: MouseEvent):
        self.end_pos = event.Position
        dx, dy = self.end_pos[0] - self.start_pos[0], self.end_pos[1] - self.start_pos[1]
        if dx > 1 or dy > 1:
            print(f"按下鼠标：{self.start_pos}")
            print(f"弹起鼠标：{event.Position}")
            # if self.dragging:
            print(f"dx, dy = {(self.end_pos[0] - self.start_pos[0], self.end_pos[1] - self.start_pos[1])}")
            self.dragging = False
        return True

    def mousedown(self, event: MouseEvent):
        self.start_pos = event.Position
        return True

    def _ignore_key(self, key_event: KeyboardEvent):
        """
        拦截系统按键，拦截self.ignore_keys中的按键，并调用self.on_key_event回调函数，如果没有回调函数，则只是屏蔽相应按键
        """
        if key_event.Key and key_event.Key.lower() in self.ignore_keys:
            if self.on_key_event:
                return self.on_key_event(key_event)
            else:
                return False
        else:
            return True

    def shield_hot_keys(self, keys, on_key_event=None):
        """
        屏蔽系统热键，当系统热键触发时，调用on_key_event方法
        键名参考KeysTransfer中的default键名
        只能调用一次
        """
        if isinstance(keys, str):
            key = KeysTransfer(source="default", destination="pywinhook_name").transfer(keys)
            self.ignore_keys.append(key.lower())
        elif isinstance(keys, list):
            for key in keys:
                key = KeysTransfer(source="default", destination="pywinhook_name").transfer(key) or ""
                self.ignore_keys.add(key.lower())

        self.on_key_event = on_key_event
        self.hm.KeyUp = self._ignore_key
        self.hm.KeyDown = self._ignore_key
        self.hm.HookKeyboard()
        self.daemon()

    def stop_shield_keyboard(self):
        self.hm.UnhookKeyboard()

    def stop_shield_mouse(self):
        self.hm.UnhookMouse()

    @staticmethod
    def daemon():
        pythoncom.PumpMessages()


if __name__ == '__main__':
    mkm = MouseKeyManager()
    mkm.shield_hot_keys(["win", "PrintScreen"])
    mkm.daemon()
