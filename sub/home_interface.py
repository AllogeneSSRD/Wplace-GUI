# coding:utf-8
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect
from qfluentwidgets import FluentIcon, setFont, InfoBarIcon

from sub.home_ui import Ui_Form


class HomeInterface(Ui_Form, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
