#!/usr/bin/env python
# coding=utf-8
import time
import traceback
from queue import Queue

from PyQt5.QtCore import QThread, pyqtSignal

import myUtils


class UpdateTableResultThread(QThread):
    signal_err = pyqtSignal(dict)

    def __init__(self, tableWidget=None):
        super(UpdateTableResultThread, self).__init__()
        self.queue = Queue()
        self.ifStopFlag = False
        self.tableWidget = tableWidget
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
                    nowInputStr = inputDic["inputStr"]
                    nowResult = inputDic["result"]

                    nowTableRowCount = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(nowTableRowCount)
                    self.tableWidget.setItem(nowTableRowCount, 0, myUtils.createTableItem(str(nowTableRowCount + 1)))
                    self.tableWidget.setItem(nowTableRowCount, 1, myUtils.createTableItem(nowInputStr))
                    self.tableWidget.setItem(nowTableRowCount, 2, myUtils.createTableItem(nowResult))
                else:
                    time.sleep(1)
                    continue
        except:
            self.threadStatus = -1
            self.extraErrorInfo = traceback.format_exc()
            errDic = {"input": inputDic, "errStr": self.extraErrorInfo, "threadObj": self}
            self.signal_err.emit(errDic)

    def addResult(self, inputStr, result):
        self.queue.put({"inputStr": inputStr, "result": result})

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

    def setTableWidget(self, tableWidget=None):
        self.tableWidget = tableWidget

    def getThreadStatus(self):
        return self.threadStatus
