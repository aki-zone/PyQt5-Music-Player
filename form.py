from functools import partial
from typing import List

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QImage, QPixmap
from audio import Config


class Ui_Form(QtWidgets.QWidget):
    """
    播放列表的ui
    """
    def __init__(self, Main_Window: object, music_list: List[Config] = None):

        super().__init__()

        self.Main_Window = Main_Window

        self.music_list = music_list

        self.setWindowTitle("播放列表")
        self.setStyleSheet("background:rgb(27, 27, 27)")

        self.setMinimumSize(QtCore.QSize(480, 150))

        self.icon1 = QtGui.QIcon()
        self.icon1.addPixmap(QtGui.QPixmap("resources/list.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(self.icon1)

        # 创建垂直布局
        self.vertical_layout = QtWidgets.QVBoxLayout(self)

        # 创建滚动区域
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # 创建列表窗口
        self.list_widget = QtWidgets.QWidget(self.scroll_area)
        self.list_layout = QtWidgets.QVBoxLayout(self.list_widget)

        if music_list is not None:
            for bean in music_list:
                # 读取播放列表里每一个播放配置单元，并赋值给每一个音乐选择按钮button/QPushButton，装进滚动容器scroll_area/QScrollArea

                button = QtWidgets.QPushButton(self.list_widget)

                button.setMinimumSize(QtCore.QSize(380, 80))
                button.setMaximumSize(QtCore.QSize(9990, 80))

                button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

                # 需要判定音乐标题是否为可读模式
                if bean.music_info.title:
                    button.setText(bean.music_info.title)
                else:
                    button.setText("暂无音乐 - 空白")

                # 判定音乐文件封面，装载进音乐选择按钮作为图标
                icon = QtGui.QIcon()
                if bean.music_info.album_cover:
                    icon.addPixmap(QtGui.QPixmap(bit_to_map(bean.music_info.album_cover)), QtGui.QIcon.Normal,
                                   QtGui.QIcon.Off)
                else:
                    icon.addPixmap(QtGui.QPixmap("resources/default.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

                button.setIcon(icon)
                button.setIconSize(QtCore.QSize(90, 90))

                bean.music_dir = self.Main_Window.get_dir()
                button.clicked.connect(partial(self.chooce, value=bean))  # 连接按钮点击事件

                button.setStyleSheet("background:rgb(37, 37, 37);"
                                     "text-align: left; "
                                     "padding-left: -2px;"
                                     "color: white;  /* 文本颜色，这里是红色 */"
                                     "font-family: Microsoft YaHei, sans-serif;  /* 字体族 */"
                                     "font-size: 28px;  /* 字体大小 */"
                                     "font-weight: bold;  /* 字体粗细 */")
                self.list_layout.addWidget(button)

        else:
            # 音乐列表为空，则加载默认播放选择按钮
            button = QtWidgets.QPushButton(self.list_widget)

            button.setMinimumSize(QtCore.QSize(380, 80))
            button.setMaximumSize(QtCore.QSize(9990, 80))

            button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            button.setText("暂无音乐 - 空白")

            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("resources/default.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            button.setIcon(icon)
            button.setIconSize(QtCore.QSize(90, 90))

            button.clicked.connect(self.show_void)  # 连接按钮点击事件

            button.setStyleSheet("background:rgb(37, 37, 37);"
                                 "text-align: left; "
                                 "padding-left: -2px;"
                                 "color: white;  /* 文本颜色，这里是红色 */"
                                 "font-family: Microsoft YaHei, sans-serif;  /* 字体族 */"
                                 "font-size: 28px;  /* 字体大小 */"
                                 "font-weight: bold;  /* 字体粗细 */")
            self.list_layout.addWidget(button)

        self.scroll_area.setWidget(self.list_widget)
        self.vertical_layout.addWidget(self.scroll_area)

    def show_void(self):
        # 在这里添加显示图片和文字的逻辑，可以使用QMessageBox、QDialog等
        # 可以考虑创建一个新的窗口来显示详细信息

        # 以一个警告窗QMessageBox/QMessageBox() 作为空白列表提示窗口
        QMessageBox = QtWidgets.QMessageBox()
        QMessageBox.setWindowIcon(self.icon1)
        QMessageBox.setWindowTitle("提示")
        QMessageBox.setInformativeText("请返回主菜单\n选择音乐文件目录~ Tv T")
        QMessageBox.exec_()

    def chooce(self, value: Config):
        """
        选择一个音乐进行播放，并从00：00时刻开始播放
        """
        if value:
            if value.music_url is not self.Main_Window.config.music_url:
                self.Main_Window.music_stop()
                self.Main_Window.set_config(value)
                self.Main_Window.bean.start_time = 0
                self.Main_Window.music_play()


def bit_to_map(binary_data):
    image = QImage.fromData(binary_data)
    pixmap = QPixmap.fromImage(image)
    return pixmap
