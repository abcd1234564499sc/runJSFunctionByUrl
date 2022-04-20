#!/usr/bin/env python
# coding=utf-8
from PyQt5.QtWidgets import QDialog

from ui.helpForm import Ui_HelpForm


class HelpWindow(QDialog,Ui_HelpForm):
    def __init__(self, parent=None):
        super(HelpWindow, self).__init__(parent)
        self.setupUi(self)
