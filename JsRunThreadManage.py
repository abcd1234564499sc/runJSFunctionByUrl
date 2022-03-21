#!/usr/bin/env python
# coding=utf-8
from PyQt5.QtCore import QThread, pyqtSignal

from JsRunThread import JsRunThread


class JsRunThreadManage(QThread):
    signal_info_log = pyqtSignal(str)
    signal_result_log = pyqtSignal(str, str)
    signal_error_log = pyqtSignal(str)

    def __init__(self, inputFormattedList=[], browser=None, parent=None):
        super(JsRunThreadManage, self).__init__(parent)
        self.inputFormattedList = inputFormattedList
        self.browser = browser
        self.threadList = []

    def run(self):
        try:
            for tmpIndex, tmpInput in enumerate(self.inputFormattedList):
                logStr = "使用输入值({1}/{2})：{0} 创建线程".format(tmpInput, tmpIndex + 1, len(self.inputFormattedList))
                self.signal_info_log.emit(logStr)
                tmpThread = JsRunThread(self.browser, tmpInput)
                tmpThread.signal_info_log[str].connect(self.writeLog)
                tmpThread.signal_result_log[str, str].connect(self.jsCallBack)
                tmpThread.signal_error_log[str].connect(self.writeErrorLog)
                self.threadList.append(tmpThread)
            # 运行线程
            for nowThread in self.threadList:
                nowThread.start()

            self.signal_info_log.emit("线程创建完成，结果请前往输出tab查看")
        except Exception as ex:
            logStr = "创建运行JS函数的线程发生异常：{0}".format(str(ex))
            self.signal_error_log.emit(logStr)

    def jsCallBack(self, inputStr, result):
        self.signal_result_log.emit(inputStr, result)

    def writeLog(self, logStr):
        self.signal_info_log.emit(logStr)

    def writeErrorLog(self, logStr):
        self.signal_error_log.emit(logStr)
