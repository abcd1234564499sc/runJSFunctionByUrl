#!/usr/bin/env python
# coding=utf-8
import math
from queue import Queue

from PyQt5.QtCore import QThread, QMutex, pyqtSignal

from JsRunThread import JsRunThread


class JsRunThreadManage(QThread):
    signal_thread_result = pyqtSignal(dict)
    signal_thread_err = pyqtSignal(dict)

    def __init__(self, maxThreadCount=1, browser=None):
        super(JsRunThreadManage, self).__init__()
        self.maxThreadCount = maxThreadCount
        self.browser = browser
        self.threadList = [self.createThread(browser=self.browser) for i in range(maxThreadCount)]
        self.nextAddThreadIndex = 0
        self.taskCount = 0
        self.taskCountLock = QMutex()

    def run(self):
        for nowThread in self.threadList:
            nowThread.start()

    def createThread(self, browser=None):
        nowThread = JsRunThread(browser=browser)
        nowThread.signal_result.connect(self.managerSolvedThreadResultFunction)
        nowThread.signal_err.connect(self.threadErrSolvedFunction)
        return nowThread

    def terminateAllThread(self):
        for nowThread in self.threadList:
            if nowThread.getThreadStatus() == 1:
                nowThread.terminateThread()
            else:
                pass

    def restartAllThread(self):
        for nowThread in self.threadList:
            if nowThread.getThreadStatus() == 2:
                nowThread.restartThread()
            elif nowThread.getThreadStatus() == 0:
                nowThread.start()
            else:
                pass

    def stopAllThread(self):
        for nowThread in self.threadList:
            if nowThread.getThreadStatus() == 1:
                nowThread.terminateThread()
                nowThread.stopThread()
            elif nowThread.getThreadStatus() == 2:
                nowThread.stopThread()
            else:
                pass

    def addInput(self, input, ifAddCount=True):
        nowUseThread = self.threadList[self.nextAddThreadIndex]
        nowUseThread.addInput(input)
        self.nextAddThreadIndex = (self.nextAddThreadIndex + 1) % self.maxThreadCount
        # ????????????+1
        if ifAddCount:
            self.taskCountLock.lock()
            self.taskCount = self.taskCount + 1
            self.taskCountLock.unlock()

    def changeMaxThreadCount(self, maxThreadCount):
        if maxThreadCount == self.maxThreadCount:
            return

        # ????????????????????????
        self.terminateAllThread()

        # ??????????????????????????????????????????
        if maxThreadCount > self.maxThreadCount:
            for tmpIndex in range(maxThreadCount - self.maxThreadCount):
                self.threadList.append(self.createThread())
            self.maxThreadCount = maxThreadCount
            # ??????????????????
            # ??????????????????????????????????????????????????????
            nowMaxTaskCount = math.ceil(self.taskCount / self.maxThreadCount)
            tmpTaskQueue = Queue()
            for tmpThread in self.threadList:
                tmpQueueLength = tmpThread.getQueueLen()
                while tmpQueueLength > nowMaxTaskCount:
                    tmpTaskQueue.put(tmpThread.getQueue().get())
                    tmpQueueLength = tmpThread.getQueueLen()
                while tmpQueueLength < nowMaxTaskCount:
                    if tmpTaskQueue.empty():
                        break
                    else:
                        tmpThread.getQueue().put(tmpTaskQueue.get())
                        tmpQueueLength = tmpThread.getQueueLen()
        else:
            solvedThreadList = []
            for tmpItem in self.threadList[maxThreadCount:]:
                solvedThreadList.append(tmpItem)
            self.threadList = self.threadList[:maxThreadCount]
            beforeNextAddThreadIndex = self.nextAddThreadIndex
            # ???????????????????????????????????????
            dataList = []
            for tmpThread in solvedThreadList:
                tmpQueue = tmpThread.getQueue()
                if tmpQueue.qsize() == 0:
                    continue
                else:
                    while not tmpQueue.empty():
                        nowInputDic = tmpQueue.get()
                        dataList.append(nowInputDic)
            # ????????????????????????????????????????????????
            self.nextAddThreadIndex = 0
            self.maxThreadCount = maxThreadCount
            for nowData in dataList:
                nowInput = nowData["input"]
                self.addInput(nowInput, ifAddCount=False)
            # ???????????????????????????IP PORT???????????????
            if beforeNextAddThreadIndex >= maxThreadCount:
                self.nextAddThreadIndex = 0
            else:
                self.nextAddThreadIndex = beforeNextAddThreadIndex

        # ??????????????????
        self.restartAllThread()

    def managerSolvedThreadResultFunction(self, resultDic):
        # ????????????-1
        self.taskCountLock.lock()
        self.taskCount = self.taskCount - 1
        self.taskCountLock.unlock()
        # ??????????????????????????????
        self.signal_thread_result.emit(resultDic)

    def getTaskCount(self):
        return self.taskCount

    def threadErrSolvedFunction(self, errDic):
        nowThreadObj = errDic["threadObj"]
        threadIndex = self.threadList.index(nowThreadObj)
        errDic["threadIndex"] = threadIndex
        self.signal_thread_err.emit(errDic)
        # ???????????????
        nowThreadObj.start()

    def getThreadsStatus(self):
        statusList = []
        for tmpThread in self.threadList:
            statusList.append(tmpThread.getThreadStatus())
        return statusList

    def getThreadQueueLen(self):
        lenList = []
        for tmpThread in self.threadList:
            lenList.append(tmpThread.getQueueLen())
        return lenList
