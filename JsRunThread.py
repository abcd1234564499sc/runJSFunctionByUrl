#!/usr/bin/env python
# coding=utf-8
import time
import traceback
from queue import Queue

from PyQt5.QtCore import QThread, pyqtSignal


class JsRunThread(QThread):
    signal_result = pyqtSignal(dict)
    signal_err = pyqtSignal(dict)

    def __init__(self, browser=None):
        super(JsRunThread, self).__init__()
        self.queue = Queue()
        self.ifStopFlag = False
        self.browser = browser
        self.threadStatus = 0  # 代表当前线程的状态，0为创建未运行，1为运行，2为中断(terminate)，3为运行后停止(stop)，-1为异常退出
        self.extraErrorInfo = ""  # 记录线程因异常退出后报错信息，只有当threadStatus为-1时才有值，平常为空字符串

    def run(self):
        self.ifStopFlag = False
        self.runFlag = True
        self.threadStatus = 1
        try:
            while not self.ifStopFlag:
                if self.runFlag and not self.queue.empty():
                    inputDic = self.queue.get()
                    nowInput = inputDic["input"]
                    nowInputFormat = nowInput.replace("\"", "\\\"")
                    jsStr = "process(\"{0}\")".format(nowInputFormat)
                    self.browser.page().runJavaScript(jsStr, self.solveResult)
                else:
                    time.sleep(1)
                    continue
        except:
            self.threadStatus = -1
            self.extraErrorInfo = traceback.format_exc()
            errDic = {"input": inputDic, "errStr": self.extraErrorInfo, "threadObj": self}
            self.signal_err.emit(errDic)

    def addInput(self, nowInput):
        self.queue.put({"input": nowInput})

    def terminateThread(self):
        self.runFlag = False
        self.threadStatus = 2

    def restartThread(self):
        self.runFlag = True
        self.threadStatus = 1

    def stopThread(self):
        self.ifStopFlag = True
        self.threadStatus = 3

    def getQueueLen(self):
        nowQueueLen = self.queue.qsize()
        return nowQueueLen

    def getQueue(self):
        return self.queue

    def setProxyDic(self, proxyDic=None):
        self.proxyDic = proxyDic

    def getThreadStatus(self):
        return self.threadStatus

    def solveResult(self, result):
        try:
            resultDic = {"input": result[0], "result": result[1]}
            self.signal_result.emit(resultDic)
        except:
            pass
