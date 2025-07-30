from yangke.common.qt import YkWindow, run_app
from yangke.common.config import logger
from yangke.common.QtImporter import QPushButton


class MainWindow(YkWindow):
    def __init__(self):
        super().__init__()
        self.enable_input_panel(panel_ui_file=None)
        self.setWindowTitle("中转服务器连接工具", with_project_name=False)

    def button_clicked(self):
        sender = self.sender()  # 发送事件的组件，可能是button、YkDialog等任何拥有signal的类
        if isinstance(sender, QPushButton):
            self.statusBar().showMessage(sender.text() + ' was pressed')
        if sender.text() == "测试连接":
            # 。。
            ...


run_app(MainWindow)
