import json

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEnginePage


class ErrorSignalWebPageConsole(QWebEnginePage):
    signal_console_error = pyqtSignal(str)

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        if level == QWebEnginePage.ErrorMessageLevel:
            self.signal_console_error.emit(msg)