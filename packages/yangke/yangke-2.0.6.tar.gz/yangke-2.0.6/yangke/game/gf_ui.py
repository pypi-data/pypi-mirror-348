import os
import time
import traceback

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog

from yangke.common.QtImporter import (QKeyEvent, QAction, Qt, QHBoxLayout, QMessageBox, QKeyEvent, QVBoxLayout,
                                      QPushButton)

from yangke.common.qt import (YkWindow, run_app, logger, QApplication, QWidget, QLabel, QComboBox,
                              QLineEdit, YkItem, YkInputPanel, YkScrollArea, YkImageWidget, YkDialog, layout_to_widget)
from yangke.common.win.dminput import DMRemote
from yangke.common.win.keyboard import VkCode, CodeToKey
from yangke.common.win.win_x64 import get_all_window
from yangke.game.gf import Step, Steps, Frame, NotExist, Exist, Region, AnchorRegion, RectRegion, Position, Offset, \
    RequestWeb
from yangke.base import start_threads, stop_threads, show_pic, pic2qlabel, pic2qpixmap
import pyautogui
from PIL import Image, ImageGrab
import yangke.game.ghost.ghostbox as gb
import win32con


class StepWidget(YkItem):
    def __init__(self, idx, op, target, judge, condition, name, root_window):
        self.name = name
        self.step = Step(op, target, judge, condition)
        self.first_item = YkItem(f"步骤{idx}", f"<button on-click='btn_clicked'>删除步骤{idx}</button>",
                                 f"<button on-click='btn_clicked'>运行步骤{idx}</button>",
                                 size=[50, 20, 20])
        self.first_item.value.clicked.connect(root_window.btn_clicked)
        self.first_item.unit.clicked.connect(root_window.btn_clicked)
        self.op_data = {
            "click key": ["键位描述"],
            "press key": ["键位描述"],
            "release key": ["键位描述"],
            "left click": ["画面中的文字", "画面中的图片", "相对偏移", "自定义对象"],
            "right click": ["画面中的文字", "画面中的图片", "相对偏移", "自定义对象"],
            "double click": ["画面中的文字", "画面中的图片", "相对偏移", "自定义对象"],
        }

        self.item11 = QComboBox()
        self.item11.addItems(self.op_data.keys())
        # noinspection all
        self.item11.currentTextChanged.connect(self.change_op)
        self.item12 = QComboBox()
        self.item12.addItems(self.op_data["click key"])
        self.item12.currentTextChanged.connect(self.change_op_dest)
        self.item13_1: QLabel | None = None
        self.item13_2 = QLineEdit("")
        self.item13 = YkItem(None, self.item13_2, None, margins=[0, 0, 0, 0], size=[0, 50, 0], struct=0)

        self.item1 = YkItem(self.item11, self.item12, unit=self.item13,
                            size=[20, 20, 50])
        self.item21 = QComboBox()
        self.item21.addItems(["重复", "等待", "无"])
        self.item22 = QComboBox()
        self.item22.addItems(["直到"])
        self.item23 = QComboBox()
        self.item23.addItems(["无", "存在文字", "存在图片", "不存在文字", "不存在图片", "自定义条件"])
        self.item23.currentTextChanged.connect(self.change_condition)
        self.condition_item = YkItem(label=self.item21,
                                     value=self.item22,
                                     unit=self.item23,
                                     size=[20, 20, 50],
                                     margins=(10, 0, 10, 0))
        self.item31 = None
        self.item31_1: QLabel = QLabel("预览图")
        self.item31_2: QLineEdit = QLineEdit()
        self.prefer_obj_line: QLineEdit = None
        self.range_line = None
        self.bak_item = None
        super().__init__(label=self.first_item, value=self.item1, unit=self.condition_item, bak=self.bak_item,
                         direction="v", bgcolor="green")
        self.set_step(self.step)

    def set_step(self, step):
        try:
            self.item11.setCurrentText(step.op)
            if step.op in ["click key", "press key", "release key"]:
                self.item12.setCurrentText("键位描述")
                if isinstance(step.target, dict):
                    self.item13_2.setText(step.target.get("value"))
                else:
                    self.item13_2.setText(step.target)
            else:
                if isinstance(step.target, Offset):
                    self.item12.setCurrentText("相对偏移")
                    self.item13_1.setText(step.target.anchor_obj)
                    self.item13_2.setText(f"{step.target.dx},{step.target.dy}")
                elif step.target.get("__cls__") == "Offset":
                    ...
                elif step.target.get("__cls__") == "Picture":
                    self.item12.setCurrentText("画面中的图片")
                    self.item13_2.setText(step.target["path"])
                    self.item13_1.setPixmap(QPixmap(step.target["path"]))
                elif step.target.get("__cls__") == "Text":
                    self.item12.setCurrentText("画面中的文字")
                    self.item13_2.setText(step.target["text"])
            if step.judge == "wait":
                self.item22.setCurrentText("等待")
            elif step.judge == "repeat":
                self.item22.setCurrentText("重复")
            else:
                self.item22.setCurrentText("无")
            if step.condition is None:
                self.item23.setCurrentText("无")
            elif isinstance(step.condition, Exist):
                if step.condition.type_ == "text":
                    self.item23.setCurrentText("存在文字")
                    if isinstance(step.condition.value, list) and len(step.condition.value) == 1:
                        text = step.condition.value[0]
                        self.item31.setText(text)
                elif step.condition.type_ == "pic":
                    self.item23.setCurrentText("存在图片")
                    if isinstance(step.condition.value, list) and len(step.condition.value) == 1:
                        path = step.condition.value[0]
                        self.item31_2.setText(path)
                        self.item31_1.setPixmap(QPixmap(path))
            elif isinstance(step.condition, NotExist):
                if step.condition.type_ == "text":
                    self.item23.setCurrentText("不存在文字")
                    if isinstance(step.condition.value, list) and len(step.condition.value) == 1:
                        text = step.condition.value[0]
                        self.item31.setText(text)
                elif step.condition.type_ == "pic":
                    self.item23.setCurrentText("不存在图片")
                    if isinstance(step.condition.value, list) and len(step.condition.value) == 1:
                        path = step.condition.value[0]
                        self.item31_2.setText(path)
                        self.item31_1.setPixmap(QPixmap(path))
            else:
                self.item23.setCurrentText("自定义条件")
                self.prefer_obj_line.setText(step.condition.value)

            if isinstance(step.condition, Exist) or isinstance(step.condition, NotExist):
                if step.condition.anchor_name is not None:
                    self.prefer_obj_line.setText(step.condition.anchor_name)
                if step.condition.region is not None:
                    if isinstance(step.condition.region, list):
                        _ = [str(__) for __ in step.condition.region]
                        self.range_line.setText(",".join(_))


        except:
            logger.warning(f"StepWidget加载出错")

    def form_bak_item(self):
        condition = self.condition_item.get_value_and_unit()[1]
        if condition == "无":
            self.bak_item = None
            return self.bak_item
        elif condition == "存在文字" or condition == "不存在文字":
            self.item31 = QLineEdit()
            self.item31.setPlaceholderText("输入条件判断的文字")
        elif condition == "自定义条件":
            self.item31 = None
            self.prefer_obj_line = QLineEdit()
            self.prefer_obj_line.setPlaceholderText("输入自定义条件")
            self.range_line = None
            self.bak_item = YkItem(label=self.item31, value=self.prefer_obj_line, unit=self.range_line,
                                   size=[0, 90, 0], margins=[1, 10, 0, 10])
            return self.bak_item
        else:
            self.item31_1 = QLabel("预览图")
            self.item31_2 = QLineEdit("")
            self.item31_2.setPlaceholderText("图片路径")
            self.item31 = YkItem(self.item31_1, self.item31_2, f"<button on-click='capture_mini_pic'>截图</button>",
                                 size=[16, 22, 12], margins=[0, 0, 0, 0], struct=2, parent=self)
            self.item31.unit.clicked.connect(self.capture_mini_pic)
        self.prefer_obj_line = QLineEdit()
        self.prefer_obj_line.setPlaceholderText("输入参考点定义")
        self.range_line = QLineEdit()
        self.range_line.setPlaceholderText("输入查找区域定义")
        self.bak_item = YkItem(label=self.item31, value=self.prefer_obj_line, unit=self.range_line,
                               size=[50, 20, 20])

        return self.bak_item

    def get_step(self):
        op = self.item11.currentText()
        if self.item12.currentText() == "相对偏移":
            target = {
                "__cls__": "Offset",
                "value": self.item13.get_value(),
                "anchor": self.item13.get_label_text()
            }
        elif self.item12.currentText() == "画面中的图片":
            target = {
                "__cls__": "Pic",
                "value": self.item13.get_value(),
                "anchor": self.item13.get_label_text()
            }
        elif self.item12.currentText() == "画面中的文字":
            target = {
                "__cls__": "Text",
                "value": self.item13.get_value(),
            }
        elif self.item12.currentText() == "键位描述":
            target = {
                "__cls__": "Key",
                "value": self.item13.get_value(),
            }
        else:  # "自定义对象"
            target = {
                "__cls__": "UserDefObj",
                "value": self.item13.get_value(),
            }
        judge = self.item21.currentText()
        cond = self.item23.currentText()
        if self.item31 is not None:
            if isinstance(self.item31, QLineEdit):
                dest_obj = self.item31.text()
            elif isinstance(self.item31, YkItem):
                dest_obj = self.item31.get_value()
            else:
                dest_obj = None
        else:
            dest_obj = None
        judge = {"重复": "repeat", "等待": "wait", "无": None}.get(judge)
        anchor_name = None
        dest_range = None
        if self.prefer_obj_line is not None and self.prefer_obj_line.text() is not None:
            anchor_name = self.prefer_obj_line.text()
        if self.range_line is None:
            _ = None
        else:
            _ = self.range_line.text()
        if _ is not None and _.strip() != "":
            dest_range = _.strip().split(",")
            try:
                dest_range = [int(_) for _ in dest_range]
            except:
                logger.error(f"目标区域中存在非数值类型字符{dest_range=}")

        if cond == "无":
            condition = None
        elif cond == "存在文字":
            condition = Exist(dest_obj, type_="text", region=dest_range, anchor_name=anchor_name)
        elif cond == "不存在文字":
            condition = NotExist(dest_obj, type_="text", region=dest_range, anchor_name=anchor_name)
        elif cond == "存在图片":
            condition = Exist(dest_obj, type_="pic", region=dest_range, anchor_name=anchor_name)
        elif cond == "不存在图片":
            condition = NotExist(dest_obj, type_="pic", region=dest_range, anchor_name=anchor_name)
        else:  # cond == "自定义条件"
            condition = self.item31.get_value()
        return Step(op=op, target=target, judge=judge, condition=condition)

    def change_op(self):
        op_name = self.item11.currentText()
        self.item12.clear()
        self.item12.addItems(self.op_data[op_name])

    def change_op_dest(self):
        op_type = self.item12.currentText()
        if op_type == "画面中的文字":
            self.item13.clear_all()
            self.item13.add_item(0, "")
            self.item13_2 = QLineEdit("")
            self.item13.add_item(1, self.item13_2)
            self.item13_2.setPlaceholderText("输入点击的文字")
            self.item13.set_size({"width": [0, 50, 0]})
        elif op_type == "键位描述":
            self.item13.clear_all()
            self.item13.add_item(0, "")
            self.item13_2 = QLineEdit("")
            self.item13.add_item(1, self.item13_2)
            self.item13_2.setPlaceholderText("输入键盘按键或组合键描述")
            self.item13.set_size({"width": [0, 50, 0]})
        elif op_type == "画面中的图片":
            self.item13.clear_all()
            self.item13_1 = QLabel("预览图")
            self.item13.add_item(0, self.item13_1)
            self.item13_2 = QLineEdit("")
            self.item13_2.setPlaceholderText("图片路径")
            self.item13.add_item(1, self.item13_2)
            self.item13.add_item(2, f"<button on-click='capture_mini_pic'>截图</button>")
            self.item13.set_size({"width": [16, 22, 12]})
            self.item13.unit.clicked.connect(self.capture_mini_pic)
        elif op_type == "相对偏移":
            self.item13.clear_all()
            self.item13_1 = QLineEdit("")
            self.item13_1.setPlaceholderText("输入偏移对象")
            self.item13_1.setToolTip("例如：step1.target/step1.condition")
            self.item13.add_item(0, self.item13_1)
            self.item13_2 = QLineEdit("")
            self.item13.add_item(1, self.item13_2)
            self.item13_2.setPlaceholderText("输入偏移参数")
            self.item13_2.setToolTip("例如：300, 100表示偏移dx=300, dy=200")
            self.item13.set_size({"width": [25, 25, 0]})
        elif op_type == "自定义对象":
            self.item13.clear_all()
            self.item13.add_item(0, "")
            self.item13_2 = QLineEdit("")
            self.item13.add_item(1, self.item13_2)
            self.item13_2.setPlaceholderText("")
            self.item13.set_size({"width": [0, 50, 0]})

    def change_condition(self):
        self.remove_item(3)
        self.add_item(3, self.form_bak_item())

    def capture_mini_pic(self):
        sender = self.sender()
        if isinstance(sender, QPushButton):
            text = sender.text()
            if text == "截图":
                pyautogui.hotkey("win", "shift", "s")
                sender.setText("粘贴")
            elif text == "粘贴":
                parent = sender.parent().parent()
                if isinstance(parent, YkItem) and parent.get_value() == "画面中的图片":
                    # 说明是鼠标点击的图片
                    step_name = sender.parent().parent().parent().label.label.text()  # 步骤1
                    file_name = f"{self.name}_{step_name}_click_obj.png"
                else:
                    # 说明是条件判断的图片
                    step_name = sender.parent().parent().parent().label.label.text()  # 步骤1
                    file_name = f"{self.name}_{step_name}_condition_obj.png"
                im = ImageGrab.grabclipboard()
                if isinstance(im, Image.Image):
                    im.save(file_name)
                    sender.parent().value.setText(file_name)
                    label: QLabel = sender.parent().label
                    label.setPixmap(QPixmap(file_name))
                    label.setScaledContents(True)
                elif im:
                    for filename in im:
                        print("filename:%s" % filename)
                        im = Image.open(filename)
                else:
                    print("clipboard is empty")

                sender.setText("截图")


class ChooseWindow(QDialog):

    def __init__(self, parent=None, windows: dict = {}):
        """
        选择要操作的窗口，从当前所有窗口中
        :param windows: 格式为{hwnd: title}的窗口信息字典
        """
        super().__init__(parent)
        self.setFixedWidth(600)
        self.setFixedHeight(600)
        self.setWindowTitle("选择值")
        self.layout = QVBoxLayout(self)

        self.combo_box = QComboBox(self)

        self.combo_box.addItems(list(windows.values()))  # 注意这里我们添加的是字符串，但你可以根据需要处理它们

        self.layout.addWidget(self.combo_box)

        self.ok_button = QPushButton("确定", self)
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

    def get_selected_value(self):
        # 返回选中的值（作为字符串）
        return self.combo_box.currentText()


class MainWindow(YkWindow):

    def __init__(self):
        super().__init__()
        self.temp_ = None
        self.add_input_panel("ui/ui_panel.yaml", domain="综合")
        _ = self.proj.get("综合")
        if isinstance(_, dict):
            for k, v in _.items():
                self._input_panel.set_value(k, v)
        self.thread = None
        self.running = False
        # self.set_status_bar_label("天谕")
        self.frame: Frame | None = None
        self.add_input_panel("ui/ui_panel.yaml", domain="自定义步骤")
        panel: YkInputPanel = self.panels.get("自定义步骤")
        step_name = panel.get_values_and_units(need_unit=False)[0].strip()
        if step_name is None or step_name == "":
            panel.set_value("步骤序列名称", "自定义任务1")
            step_name = "自定义任务1"
        else:
            panel.set_value("步骤序列名称", step_name)
        if self.proj.get("temp_steps") is None or self.proj.get("temp_steps") == []:
            item = StepWidget(1, "press", "R", None, None, step_name, self)
            if panel is not None:
                panel.insert_item(1, item)
        else:
            for idx, step in enumerate(self.proj.get("temp_steps")):
                item = StepWidget(idx=idx + 1, root_window=self, name=step_name, **step)
                panel.insert_item(idx + 1, item)
            # self.add_content_tab(YkItem(), "存在条件设置")
        self.add_content_tab(QLabel("."), "欢迎")
        self.capture_ykimagewidget = YkImageWidget([], True, self.do_action)
        scroll = YkScrollArea()
        scroll.setWidget(self.capture_ykimagewidget)
        self.add_content_tab(widget=scroll, tab_name="CT截图")

        # self.statusBar1.addPermanentWidget()

        # self.add_content_tab(widget=self.capture_ykimagewidget, tab_name="CT截图") # 直接使用该widget会导致每次截图，画面高度增加，貌似是QT的bug
        self._keyboard = False  # 模拟键盘功能是否开启
        self._mouse = False  # 模拟鼠标功能是否开启
        if self.proj.get("dm_sim_info") is None:
            self.proj.update({"dm_sim_info": {"key": "null",
                                              "add_key": "",
                                              "display": "gid2",
                                              "mouse": "dx.mouse.position.lock.api",
                                              "keypad": "windows",
                                              "public": "",
                                              "mode": "101:超级绑定模式.可隐藏目标进程中的dll，推荐使用",
                                              "port": 8765},
                              "sim_mode": "DM-remote"},
                             )
        if self.proj.get("temp_steps") is None:
            self.proj.update({
                "temp_steps": []
            })
        if self.proj.get("steps_repos") is None:
            self.proj.update({
                "steps_repos": {}
            })

        if self.proj.get("RequestWebPort") is not None:
            self.request_web = RequestWeb(self.proj.get("RequestWebPort"))
        else:
            self.request_web = RequestWeb(port=8765)

        self.mode_repos = {
            "天谕": {
                "display": "dx.graphic.3d.10plus",
                "mouse": "dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor",
                "keypad": "dx.keypad.state.api|dx.keypad.api",
                "public": "dx.public.graphic.protect|dx.public.anti.api|dx.public.km.protect|dx.public.prevent.block",
                "mode": "101:超级绑定模式.可隐藏目标进程中的dll，推荐使用",
            },
            "天谕1": {
                "display": "dx.graphic.3d.10plus",
                "mouse": "dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.clip.lock.api|dx.mouse.input.lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor|dx.mouse.raw.input",
                "keypad": "dx.keypad.input.lock.api|dx.keypad.state.api|dx.keypad.api",
                "public": "",
                "mode": "0:推荐模式此模式比较通用，而且后台效果是最好的",
            },
            "笑傲江湖": {

            },
            "剑叁": {
                "display": "dx.graphic.3d.10plus",
                "mouse": "dx.mouse.api|dx.mouse.raw.input",
                "keypad": "dx.keypad.input.lock.api|dx.keypad.state.api|dx.keypad.api",
                "public": "",
                "mode": "0:推荐模式此模式比较通用，而且后台效果是最好的",
            },
            "逆水寒": {
                "display": "dx.graphic.3d.10plus",
                "mouse": "dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor",
                "keypad": "dx.keypad.state.api|dx.keypad.api",
                "public": "dx.public.graphic.protect|dx.public.anti.api|dx.public.km.protect|dx.public.prevent.block",
                "mode": "101:超级绑定模式.可隐藏目标进程中的dll，推荐使用",
            },
            "魔兽世界": {
                "display": "dx.graphic.3d.10plus",
                "mouse": "dx.mouse.clip.lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor",
                "keypad": "dx.keypad.input.lock.api|dx.keypad.state.api|dx.keypad.api",
                "public": "dx.public.hide.dll|dx.public.anti.api|dx.public.km.protect",
                "mode": "101:超级绑定模式.可隐藏目标进程中的dll，推荐使用",
            }
        }

    def show_dialog(self):
        dialog = ChooseWindow(self, get_all_window())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_value = dialog.get_selected_value()
            self.panels.get("综合").set_value("游戏ID", selected_value)
            self.init_frame(force_update=True)
            self.capture_window()

    def yk_signal_received(self, msg: dict):
        if msg.get("action") == "capture_window":
            self.capture_window()

    def set_sim_mode(self):
        _ = os.path.abspath(os.path.join(os.path.dirname(__file__), "ui", "ui_panel.yaml"))
        input_panel = YkInputPanel(from_file=_, domain="设置键鼠模拟方式", parent=self)

        dialog = YkDialog(self, widget=input_panel, modality=False)
        dialog.set_size(600, 500)
        input_panel.apply_btn_connect()
        self.temp_ = {"input_panel": input_panel, "dialog": dialog}

        dm_sim_info = self.proj.get("dm_sim_info")
        input_panel.set_value("注册码", value=dm_sim_info.get("key") or "null")
        input_panel.set_value("附加码", value=dm_sim_info.get("add_key") or "")
        input_panel.set_value("显示", value=dm_sim_info.get("display") or "gdi2")
        input_panel.set_value("鼠标", value=dm_sim_info.get("mouse") or "dx.mouse.position.lock.api")
        input_panel.set_value("键盘", value=dm_sim_info.get("keypad") or "windows")
        input_panel.set_value("公共参数", value=dm_sim_info.get("public") or "")
        input_panel.set_value("模式", value=dm_sim_info.get("mode"))
        try:
            input_panel.set_value("端口", value=int(dm_sim_info.get("port")) or 8765)
        except:
            QMessageBox.warning(None, "错误提示", f"端口号必须是整数，当前为({dm_sim_info.get('port')})")
            input_panel.set_value("端口", value=8765)

        input_panel.set_value("模拟方式", self.proj.get("sim_mode"))


    def _change_sim_mode(self):
        input_panel: YkInputPanel = self.temp_.get("input_panel")
        type_ = input_panel.get_item("模拟方式").get_value()
        input_panel.remove_item(index=list(range(1, input_panel.get_items_count() - 2)))
        tails = -2  # 面板尾部的固定YkItem数量
        if type_ == "DM-remote" or type_.startswith("DM-local"):
            input_panel.get_item("模拟方式").unit.setHidden(False)
            input_panel.get_item("模拟方式").unit.setText("加载DM")
            dm_sim_info = self.proj.get("dm_sim_info")
            input_panel.insert_item(tails, YkItem("注册码", "", "", size=[30, 130, 0]))  # 在倒数第三个位置插入YkItem
            input_panel.set_value("注册码", value=dm_sim_info.get("key") or "null")
            input_panel.insert_item(tails, YkItem("附加码", "", "", size=[30, 130, 0]))
            input_panel.set_value("附加码", value=dm_sim_info.get("add_key") or "")
            input_panel.insert_item(tails, YkItem("显示", "", "", size=[30, 130, 0]))
            input_panel.set_value("显示", value=dm_sim_info.get("display") or "gdi2")
            input_panel.insert_item(tails, YkItem("鼠标", "", "", size=[30, 130, 0]), )
            input_panel.set_value("鼠标", value=dm_sim_info.get("mouse") or "dx.mouse.position.lock.api")
            input_panel.insert_item(tails, YkItem("键盘", "", "", size=[30, 130, 0]), )
            input_panel.set_value("键盘", value=dm_sim_info.get("keypad") or "windows")
            input_panel.insert_item(tails, YkItem("公共参数", "", "", size=[30, 130, 0]), )
            input_panel.set_value("公共参数", value=dm_sim_info.get("public") or "")
            input_panel.insert_item(tails, YkItem("模式", "", "", size=[30, 130, 0]), )
            input_panel.set_value("模式",
                                  value=dm_sim_info.get("mode") or "101:超级绑定模式.可隐藏目标进程中的dll，推荐使用")
            input_panel.insert_item(tails, YkItem("端口", "", "", size=[30, 130, 0]), )
            input_panel.set_value("端口", value=dm_sim_info.get("port") or 8765)
            item: YkItem = self.panels["综合"].get_item("游戏ID")
            item.value.setEnabled(True)
            item.unit.setHidden(False)
        elif type_ == "Normal":
            input_panel.get_item("模拟方式").unit.setHidden(True)
            item: YkItem = self.panels["综合"].get_item("游戏ID")

            item.value.setEnabled(True)
            item.unit.setHidden(False)

        elif type_ == "幽灵键鼠":
            input_panel.get_item("模拟方式").unit.setHidden(False)
            input_panel.get_item("模拟方式").unit.setText("测试幽灵键鼠")

            item: YkItem = self.panels["综合"].get_item("游戏ID")
            item.value.setEnabled(True)
            item.unit.setHidden(False)
        elif type_ == "易键鼠":
            input_panel.get_item("模拟方式").unit.setHidden(True)

            item: YkItem = self.panels["综合"].get_item("游戏ID")
            item.value.setEnabled(True)
            item.unit.setHidden(False)
        elif type_ == "易键鼠-双头远程":
            input_panel.get_item("模拟方式").unit.setHidden(True)
            item: YkItem = self.panels["综合"].get_item("游戏ID")
            item.set_value("USB视频流-易键鼠-远程操作")
            item.value.setEnabled(False)
            item.unit.setHidden(True)
        elif type_ == "幽灵键鼠-双头远程":
            input_panel.get_item("模拟方式").unit.setHidden(True)
            item: YkItem = self.panels["综合"].get_item("游戏ID")
            item.set_value("USB视频流-幽灵键鼠-远程操作")
            item.value.setEnabled(False)
            item.unit.setHidden(True)

    def add_step(self):
        panel: YkInputPanel = self.panels.get("自定义步骤")
        idx = panel.get_items_count()
        name = panel.get_item("步骤序列名称").value.text()
        panel.insert_item(idx, StepWidget(idx, "press", "R", None, None, name, self))

    def init(self):
        self.init_frame()

        self.frame.init_chat(anchor="ui/ZhaoMu.png", anchor_region=AnchorRegion(0, "anchor.y1", "anchor.x1", -10),
                             channels=["世界", "团队", "队伍", "附近", "阵营", "地区"])
        suc = self.frame.init_task(anchor="任务", find_region=RectRegion(left=-350, top=300, right=-1, bottom=-500),
                                   anchor_region=AnchorRegion("anchor.x1", "anchor.y1", -10, "anchor.y1+400"))
        if not suc:
            self.frame.init_task(anchor="驻地", find_region=RectRegion(left=-350, top=300, right=-1, bottom=-500),
                                 anchor_region=AnchorRegion("anchor.x1-100", "anchor.y1", -10, "anchor.y1+400"))

        # self.frame.init_time(region=(-170, 0, -2, 30))
        self.frame.init_time(region=(-25, 5, -2, 25))
        # self.frame.turn_direction_to("青蛙", region=Region(width_child=1000, height_child=800))

    def run(self):
        # self.init()
        # settings = self.get_value_of_panel(need_dict=True, need_unit=False)
        # key = settings.get("打怪技能按键")
        # role = settings.get("游戏ID").strip()
        # mode = settings.get("打怪模式")
        # freq = float(settings.get("按键频率"))
        # # self.frame = Frame(role)
        # # link_pos = self.frame.task.get_text_link_pos_global("打开公会")
        # # self.frame.show_region(link_pos)
        # #
        # # self.frame.left_click(*link_pos.get_center(), offset=(16, 0))
        # # self.frame.dm.unbind_window()
        # if mode == "无脑打怪":
        #     steps_重复按键 = Steps(
        #         steps=[
        #             Step("press", key, None, None),
        #         ]
        #     )
        # else:
        #     steps_重复按键 = Steps(
        #         steps=[
        #             Step("press", key, "until",
        #                  NotExist("竹林偷伐者", last_time=20, region=Region(align="center", width_child=600)),
        #                  wait_method="repeat"),
        #             Step("double-press", "space", "until",
        #                  Exist("竹林偷伐者", last_time=60, interval=10, region=Region(align="center", width_child=600)),
        #                  wait_method="repeat"),
        #         ]
        #     )
        # self.thread = start_threads(self.frame.run_steps_forever, args_list=[steps_重复按键, freq])
        self._input_panel.get_button("运行").setDisabled(True)
        self._input_panel.get_button("停止").setDisabled(False)

    def stop(self):
        stop_threads(self.thread)
        self.running = False
        logger.debug(f"停止任务")
        self._input_panel.get_button("停止").setDisabled(True)
        self._input_panel.get_button("运行").setDisabled(False)
        if self.proj.get("sim_mode") == "DM-remote":
            self.frame.dm.unbind_window()
            if self._mouse:
                self._mouse = False
            if self._keyboard:
                self._keyboard = False

    def save(self):
        settings = self.get_value_of_panel(need_dict=True, need_unit=False, domain="综合")
        self.proj.update({"综合": settings})
        super().save()

    def init_frame(self, force_update=False):
        """
        绑定需要操作的窗口界面

        :params force_update： 已有绑定窗口时是否强制更新绑定的窗口
        """
        if self.frame is None or self.frame.window is None or force_update or not self.frame.bind_success:
            settings = self.get_value_of_panel(need_dict=True, need_unit=False, domain="综合")
            role = settings.get("游戏ID").strip()
            if self.frame is not None:
                if hasattr(self.frame, "dm") and self.frame.bind_success:
                    self.frame.dm.unbind_window()
            self.frame = Frame(role,
                               sim_mode=self.proj.get("sim_mode"),
                               sim_info=self.proj.get("dm_sim_info"))
            if self.frame.window is None:
                self.statusBar1.showMessage("未找到游戏窗口")
                return None
        return self.frame

    def capture_window(self):

        self.init_frame()
        if self.frame.window is None:
            return
        if not self.frame.bind_success:
            QMessageBox.information(self, "提示", "使用DM-remote插件，但窗口绑定失败")
        snapshot = self.frame.capture_window_xywh()
        # screen = QApplication.primaryScreen()
        # snapshot = screen.grabWindow(self.frame.window).toImage()
        # show_pic(snapshot)
        if len(snapshot) == 0:  # snapshot == []
            return
        if self.capture_ykimagewidget is None:
            self.capture_ykimagewidget = YkImageWidget(snapshot, True, self.do_action)
            scroll = YkScrollArea()
            scroll.setWidget(self.capture_ykimagewidget)
            self.add_content_tab(widget=scroll, tab_name="CT截图")
            # self.add_content_tab(widget=self.capture_ykimagewidget, tab_name="CT截图")
        else:
            self.capture_ykimagewidget.replace_image(snapshot)

        if "CT截图" in self._content_tab.labels and self._content_tab.get_current_tab_name() != "CT截图":
            self._content_tab.activate_tab("CT截图")
        pos = self.frame.get_cursor_pos()
        if pos is not None:
            self.set_status_bar_label(str(pos))
        self.statusBar1.showMessage("就绪")

    def real_time_capture(self):
        logger.info("开始实时截图")
        while self._mouse or self._keyboard:
            self.yk_signal.emit({"action": "capture_window"})
            time.sleep(0.1)
        logger.info("实时截图结束")
        self.statusBar1.showMessage("就绪")

    def btn_clicked(self, anything=None, anything2=None, **kwargs):
        """
        在截图区域上点击时的响应时间
        """
        sender = self.sender()
        text = sender.text()
        if text == "截图":
            self.capture_window()
            self.statusBar1.showMessage("就绪")

        if text == "加载DM":
            sim_info = self.proj.get("dm_sim_info")
            dm_remote = DMRemote(key=sim_info.get("key"), add_key=sim_info.get("add_key"), port=sim_info.get("port"))
            if dm_remote.success:
                QMessageBox.information(None, "提示", "DM-remote加载成功")
            else:
                QMessageBox.information(None, "提示", f"DM-remote加载失败，{dm_remote.error_info}")
        elif text == "测试幽灵键鼠":
            res = gb.opendevice(0)
            if gb.isconnected():
                QMessageBox.information(self, "提示", "幽灵键鼠设备正常")
            else:
                QMessageBox.information(self, "提示", "幽灵键鼠设备打开失败，请检查硬件是否存在")
        elif text == "保存键鼠模拟方式":
            input_panel: YkInputPanel = self.temp_.get("input_panel")
            values = input_panel.get_values_and_units(need_unit=False, need_dict=True, need_label=True)
            if self.proj.get("sim_mode") != values.get("模拟方式"):  # 更改模拟方式后，重新绑定窗口
                self.proj.update({"sim_mode": values.get("模拟方式")})
                self.init_frame(force_update=True)
            if values.get("模拟方式") == "DM-remote" or values.get("模拟方式") == "DM-local":
                try:
                    port = values.get("端口")
                except:
                    QMessageBox(None, "错误提示", f"端口号必须是整数，当前为({values.get('端口')})")
                    port = self.proj.get("dm_sim_info").get("port") or 8765
                self.proj.get("dm_sim_info").update({"key": values.get("注册码"),
                                                     "add_key": values.get("附加码"),
                                                     "display": values.get("显示"),
                                                     "mouse": values.get("鼠标"),
                                                     "keypad": values.get("键盘"),
                                                     "public": values.get("公共参数"),
                                                     "mode": values.get("模式"),
                                                     "port": port,
                                                     })
            else:
                pass
            # self.temp_: YkDialog
            if isinstance(self.temp_.get("dialog"), YkDialog):
                self.temp_.get("dialog").close()
            self.statusBar1.showMessage("就绪")

        elif text == "绑定窗口":
            if self.init_frame() is None:
                QMessageBox.information(self, "提示", "绑定失败，详细信息请检查日志输出")
            else:
                QMessageBox.information(self, "提示", "窗口绑定成功")
            self.statusBar1.showMessage("就绪")
        elif text == "移动鼠标":
            # 测试移动鼠标功能
            self.init_frame()
            _x, _y = self.frame.window_pos
            w, h = self.frame.window_size
            x1 = int(_x + w / 2)
            y1 = int(_y + h / 2)
            # x1, y1 = 963, 102
            x2, y2 = x1 + 100, y1 + 11
            interval = int((x2 - x1) / 10)
            self.frame.left_press(x1, y1)
            QApplication.processEvents()
            for i in range(10):
                self.frame.move_to(x1 + i * interval, y1 + i)
                logger.debug(f"dest pos: {x1 + i * interval}, {y1}  cursor pos: {self.frame.get_cursor_pos()}")
                QApplication.processEvents()
            self.frame.left_release(x1 + 21, y1)

        elif text.startswith("运行步骤"):
            self.statusBar1.showMessage("开始执行步骤")
            panel: YkInputPanel = self.panels.get("自定义步骤")
            idx = int(text.replace("运行步骤", ""))
            step_widget: StepWidget = panel.get_item(f"步骤{idx}")
            step: Step = step_widget.get_step()
            self.frame.run_steps(Steps([step]))
            self.statusBar1.showMessage("步骤执行完毕")
        elif text.startswith("删除步骤"):
            panel: YkInputPanel = self.panels.get("自定义步骤")
            panel.remove_item(-1)
        elif text.startswith("测试键盘"):
            # 测试键盘事件
            input_panel: YkInputPanel = self.temp_.get("input_panel")
            cmd = input_panel.get_item("测试键盘").get_value()  # click_key('A')
            cmd = f"self.frame.{cmd}"
            try:
                exec(cmd)
            except Exception as e:
                traceback.print_exc()
            self.capture_window()
        elif text.startswith("测试鼠标"):
            # 测试鼠标模拟是否正常
            input_panel: YkInputPanel = self.temp_.get("input_panel")
            cmd = input_panel.get_item("测试鼠标").get_value()  # left_click(10,10)
            cmd = f"self.frame.{cmd}"
            try:
                exec(cmd)
            except Exception as e:
                traceback.print_exc()
            self.capture_window()

    def load_steps(self, combox: QComboBox | str, dialog: YkDialog):
        """
        加载指定名称的步骤序列
        """
        if isinstance(combox, QComboBox):
            steps_name = combox.currentText()
        else:
            steps_name = combox
        steps = self.proj.get("steps_repos").get(steps_name)

        dialog.close()

    def close_load_steps_repos(self, dialog: YkDialog):
        self.statusBar1.showMessage("就绪")
        dialog.close()

    def steps_clicked(self):
        sender = self.sender()
        text = sender.text()
        if text == "加载":
            steps_repos = self.proj.get("steps_repos")
            if steps_repos is not None and len(steps_repos) > 0:
                steps_name = list(steps_repos.keys())
                button1 = QPushButton("确定")
                button2 = QPushButton("取消")

                choose_steps = QComboBox()
                choose_steps.addItems(steps_name)

                vbox = QVBoxLayout()
                vbox.addWidget(choose_steps)
                vbox.addWidget(button1)
                vbox.addWidget(button2)
                dialog = YkDialog(self, "加载步骤序列", layout_to_widget(vbox))
                dialog.set_size(300, 300)

                button1.clicked.connect(lambda: self.load_steps(choose_steps, dialog))
                button2.clicked.connect(lambda: self.close_load_steps_repos(dialog))
        elif text == "运行":
            if self.running:
                QMessageBox.warning(self, "警告", "已经有任务在运行了！")
                return
            self.init_frame()
            panel: YkInputPanel = self.panels.get("自定义步骤")
            steps = []
            for i in range(1, panel.get_items_count()):
                _step = panel.get_item(f"步骤{i}")
                self.statusBar1.showMessage(f"执行步骤{i}")
                step = _step.get_step()
                steps.append(step)

            # self.frame.run_steps(Steps(steps))
            self.thread = start_threads(self.frame.run_steps, (Steps(steps),))  # 新线程中运行步骤序列，否则界面卡死
            self.running = True
        elif text == "保存":
            panel: YkInputPanel = self.panels.get("自定义步骤")
            steps_name = panel.get_item("步骤序列名称").get_value()
            steps_json = []
            for i in range(1, panel.get_items_count()):
                _step = panel.get_item(f"步骤{i}")
                step = _step.get_step()
                steps_json.append(step.to_json())
            self.proj["temp_steps"] = steps_json
            self.proj["steps_repos"].update({steps_name: steps_json})
            self.statusBar1.showMessage(f"步骤序列 [{steps_name}] 保存成功")

    def do_action(self, x, y, op):
        """
        执行操作，然后等待1s，截图显示
        """
        if self._mouse:  # 如果开启了鼠标模拟测试，则转发鼠标操作至绑定的窗口
            if self.frame is not None and self.frame.window is not None:
                x_inner = int(self.capture_ykimagewidget.x_scale * x)
                y_inner = int(self.capture_ykimagewidget.y_scale * y)
                if op == "left_click":
                    self.frame.left_click(x_inner, y_inner)
                elif op == "right_click":
                    self.frame.right_click(x_inner, y_inner)
                elif op == "left_press":
                    logger.debug(f"left_press {x_inner}, {y_inner}")
                    self.frame.left_press(x_inner, y_inner)
                elif op == "right_press":
                    logger.debug(f"right_press {x_inner}, {y_inner}")
                    self.frame.right_press(x_inner, y_inner)
                elif op == "left_release":
                    logger.debug(f"left_release {x_inner}, {y_inner}")
                    self.frame.left_release(x_inner, y_inner)
                elif op == "right_release":
                    logger.debug(f"right_up {x_inner}, {y_inner}")
                    self.frame.right_release(x_inner, y_inner)
                elif op == "move":
                    logger.debug(f"move {x_inner}, {y_inner}")
                    self.frame.move_to(x_inner, y_inner)
        else:
            if self.frame is not None and self.frame.window is not None:
                x_inner = int(self.capture_ykimagewidget.x_scale * x)
                y_inner = int(self.capture_ykimagewidget.y_scale * y)
                self.set_status_bar_label(f"{x_inner}, {y_inner}")

    def event(self, event):
        if isinstance(event, QKeyEvent):
            key = event.nativeVirtualKey()
            if self._keyboard:
                if key in [win32con.VK_TAB, win32con.VK_F5]:  # and event.type() == QKeyEvent.Type.KeyRelease):
                    self.keyPressEvent(event)  # Qt默认Tab键会被窗口处理，不会传递给KeyPressEvent事件
                    return True  # 该事件已被处理
            else:
                return super().event(event)

        return super().event(event)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        """
        键盘按键-按下某键
        测试方法只支持短按，不支持按键不放，但按键不放可以在内部实现
        20240702:支持长按
        """
        key_code = a0.nativeVirtualKey()  # 获取按键的标准键码，a0.key()是Qt的特有键码，不通用
        if self._keyboard:  # 如果模拟键盘开启，则拦截所有键盘按键至绑定的窗口
            self.init_frame()
            if key_code == win32con.VK_ESCAPE:
                if self.capture_ykimagewidget.region_show:
                    return  # 释放按键时响应
            key = CodeToKey[key_code]
            self.frame.press_key(key=key)
        else:
            if self.capture_ykimagewidget.region_show:
                if key_code == win32con.VK_ESCAPE:
                    return  # 释放时响应
            super().keyPressEvent(a0)

    def keyReleaseEvent(self, a0: QKeyEvent):
        key_code = a0.nativeVirtualKey()
        if self._keyboard:
            if key_code == win32con.VK_ESCAPE:
                if self.capture_ykimagewidget.region_show:
                    self.capture_ykimagewidget.region_show = False
                    self.capture_window()
                    return  # 按下按键时已经响应
            key = CodeToKey[key_code]
            self.frame.release_key(key=key)
        else:
            if self.capture_ykimagewidget.region_show:
                if key_code == win32con.VK_ESCAPE:
                    self.capture_ykimagewidget.region_show = False
                    self.capture_window()
                    return  # 释放时响应
            super().keyReleaseEvent(a0)

    def show_new_region(self):
        if self.capture_ykimagewidget is None:
            return
        geo = self.capture_ykimagewidget.geometry()
        self.capture_ykimagewidget.region_show = True

    def tool_click(self, k1):
        # 工具栏点击事件
        sender: QAction = self.sender()
        text: str = self.sender().text()
        if text == "模拟键盘":
            if self._keyboard:
                sender.setChecked(False)
                self._keyboard = False
            else:
                sender.setChecked(True)
                self._keyboard = True
                self.panels.get("综合").get_button("停止").setDisabled(False)
                if self._mouse is False:
                    start_threads(self.real_time_capture)
        elif text == "模拟鼠标":
            if self._mouse:
                sender.setChecked(False)
                self._mouse = False
            else:
                sender.setChecked(True)
                self._mouse = True
                self.panels.get("综合").get_button("停止").setDisabled(False)
                if self._keyboard is False:
                    start_threads(self.real_time_capture)

        elif text == "新建区域":
            self.show_new_region()
            self.capture_window()

    def refresh(self):
        self.frame.dm.unbind_window()  # 解绑窗口，重新绑定
        self.init_frame()
        if "CT截图" in self._content_tab.labels:
            self._content_tab.remove_tab("CT截图")
        self.capture_ykimagewidget = YkImageWidget([], True, self.do_action)
        scroll = YkScrollArea()
        scroll.setWidget(self.capture_ykimagewidget)
        self.add_content_tab(widget=scroll, tab_name="CT截图")


run_app(MainWindow)
