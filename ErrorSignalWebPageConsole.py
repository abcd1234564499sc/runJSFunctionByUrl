import json

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEnginePage


class ErrorSignalWebPageConsole(QWebEnginePage):
    signal_console_error = pyqtSignal(str)

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        if level == QWebEnginePage.ErrorMessageLevel:
            self.signal_console_error.emit(msg)
            
    def certificateError(self, error):
        # If you want to ignore the certificates of certain pages
        # then do something like
        # if error.url() == QUrl("https://www.us.army.mil/"):
        #     error.ignoreCertificateError()
        #     return True
        # return super().certificateError(error)

        error.ignoreCertificateError()
        return True