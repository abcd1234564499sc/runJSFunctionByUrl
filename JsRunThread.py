#!/usr/bin/env python
# coding=utf-8
from PyQt5.QtCore import QThread, pyqtSignal


class JsRunThread(QThread):
    signal_info_log = pyqtSignal(str)
    signal_result_log = pyqtSignal(str, str)
    signal_error_log = pyqtSignal(str)

    def __init__(self, browser, nowInput, parent=None):
        super(JsRunThread, self).__init__(parent)
        self.browser = browser
        self.nowInput = nowInput
        nowInputFormat = nowInput.replace("\"", "\\\"")
        self.jsStr = "process(\"{0}\")".format(nowInputFormat)

    def run(self):
        try:
            self.browser.page().runJavaScript(self.jsStr, self.writeLog)
        except Exception as ex:
            errorLogStr = "输入值为 {0} 的线程运行时发生后异常：{1}".format(self.nowInput,str(ex))
            self.signal_error_log.emit(errorLogStr)

    def writeLog(self, result):
        self.signal_result_log.emit(self.nowInput, result)
