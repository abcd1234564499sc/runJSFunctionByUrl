#!/usr/bin/env python
# coding=utf-8
import os
import sys

from PyQt5 import QtNetwork
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView

import myUtils
from ConfigWindow import ConfigWindow
from ErrorSignalWebPageConsole import ErrorSignalWebPageConsole
from ExportExcellThread import ExportExcellThread
from HelpWindow import HelpWindow
from JsRunThreadManage import JsRunThreadManage
from LoadBrowserThread import LoadBrowserThread
from UpdateTableReusltThread import UpdateTableResultThread
from ui.mainForm import Ui_MainWindow


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.checkedList = []
        self.inputFormattedList = []
        self.updateInputFormat()
        self.resetJsFunctionITextEdit()
        userAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        self.browser = QWebEngineView()
        browserPage = ErrorSignalWebPageConsole(self.browser)
        browserPage.signal_console_error.connect(self.jsConsoleErrorSolved)
        self.browser.setPage(browserPage)
        self.browser.page().profile().setHttpUserAgent(userAgent)
        self.browser.loadFinished.connect(self.browserLoaded)
        self.browser.setObjectName("webView")
        self.horizontalLayout_5.addWidget(self.browser)
        self.confFileName = "工具箱配置.conf"
        self.confHeadList = ["是否使用代理", "代理IP", "代理端口"]
        # 初始化线程
        self.browserLoadThread = LoadBrowserThread()
        self.threadManage = JsRunThreadManage(browser=self.browser)
        self.threadManage.signal_thread_result.connect(self.runJsThreadResultSolved)
        self.threadManage.signal_thread_err.connect(self.runJsThreadErrSolved)
        self.updateTableResultThread = UpdateTableResultThread(self.resultTable)
        # 设置结果表头
        self.resultHeaderList = ["序号", "输入", "输出"]
        self.resultTable.setColumnCount(len(self.resultHeaderList))
        self.resultTable.setHorizontalHeaderLabels(self.resultHeaderList)
        self.resultTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.resultTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.resultTable.verticalHeader().setVisible(False)

        self.confDic = self.initConfFile()
        self.confWindow = ConfigWindow(self.confDic)
        self.helpWindow = HelpWindow()
        # 运行线程
        self.threadManage.start()
        self.updateTableResultThread.start()

    # 初始化配置文件，生成配置文件并返回一个配置字典
    # 字典结构为：{
    # "confFileName":配置文件文件名,
    # "ifProxy":是否开启代理，
    # "proxyIp":代理IP,
    # "proxyPort":代理端口
    # }
    def initConfFile(self):
        defaultIfProxy = 0
        defaultProxyIp = ""
        defaultProxyPort = ""
        defaultConfHeaderList = self.confHeadList
        confDic = {defaultConfHeaderList[0]: defaultIfProxy, defaultConfHeaderList[1]: defaultProxyIp,
                   defaultConfHeaderList[2]: defaultProxyPort}

        # 判断是否存在配置文件
        confFilePath = os.path.join(os.getcwd(), self.confFileName)
        if not os.path.exists(confFilePath):
            myUtils.writeToConfFile(confFilePath, confDic)
            confDic["confHeader"] = defaultConfHeaderList
        else:
            confDic = myUtils.readConfFile(confFilePath)
        headerList = confDic["confHeader"]

        reConfDic = {"confFilePath": confFilePath, "confHeaderList": headerList,
                     "ifProxy": True if int(confDic[headerList[0]]) == 1 else False,
                     "proxyIp": confDic[headerList[1]], "proxyPort": confDic[headerList[2]]}

        # 更新代理设置
        self.updateProxy(reConfDic["ifProxy"], reConfDic["proxyIp"], reConfDic["proxyPort"])

        return reConfDic

    def updateInputFormat(self, checkState=0):
        # 遍历4个输入框的复选框，根据选择情况构建inputFormatLineEdit的值
        formatStr = "{"
        checkBoxList = [self.input1CheckBox, self.input2CheckBox, self.input3CheckBox, self.input4CheckBox]
        checkedList = []
        for tmpIndex, nowCheckBox in enumerate(checkBoxList):
            if nowCheckBox.isChecked():
                formatStr = formatStr + "\"输入值{0}\":\"$%$输入值{0}$%$\",".format(tmpIndex + 1)
                checkedList.append(1)
            else:
                checkedList.append(0)
        if formatStr[-1] == ",":
            formatStr = formatStr[:-1]
        else:
            pass
        formatStr = formatStr + "}"
        self.inputFormatLineEdit.setText(formatStr)
        self.checkedList = checkedList

    # 判断是否完成输入
    def checkInput(self):
        checkFlag = True
        checkStr = ""
        nowUrl = self.urlLineEdit.text()
        if nowUrl == "" and checkFlag:
            checkFlag = False
            checkStr = "请输入URL"
        else:
            pass
        if not myUtils.checkIfUrl(nowUrl) and checkFlag:
            checkFlag = False
            checkStr = "输入的URL不符合规范"
        else:
            pass
        if sum(self.checkedList) == 0 and checkFlag:
            checkFlag = False
            checkStr = "请至少启用一个输入"
        else:
            pass
        if self.jsFunTextEdit.toPlainText() == "" and checkFlag:
            checkFlag = False
            checkStr = "js处理函数不能留空"
        else:
            pass
        self.inputFormattedList = self.getInput()
        if len(self.inputFormattedList) == 0 and checkFlag:
            checkFlag = False
            checkStr = "输入为空"
        else:
            pass
        return checkFlag, checkStr

    # 写日志，logType：0代表流程日志，1代表错误日志
    def writeLog(self, logStr, logType=0):
        # 获取当前时间
        nowSeconed = myUtils.getNowSeconed()
        finalLog = "[{0}] {1}".format(nowSeconed, logStr)
        if logType == 0:
            self.normalLogTextEdit.moveCursor(QTextCursor.End)
            self.normalLogTextEdit.append(finalLog)
            self.normalLogTextEdit.moveCursor(QTextCursor.End)
        else:
            self.errorLogTextEdit.moveCursor(QTextCursor.End)
            self.errorLogTextEdit.append(finalLog)
            self.errorLogTextEdit.moveCursor(QTextCursor.End)

    def writeErrorLog(self, logStr):
        self.writeLog("运行发生异常，请确认错误日志")
        self.writeLog(logStr, 1)

    def resetJsFunctionITextEdit(self):
        functionModelStr = ''' function process(nowInputVal){\n    var nowOutputVal = "";\n    nowInputVal=String(nowInputVal);\n    // 逻辑代码\n    nowOutputVal=nowInputVal;\n    \n    return [nowInputVal,nowOutputVal];\n}'''
        self.jsFunTextEdit.setText(functionModelStr)

    def getInput(self):
        # 遍历输入
        inputTextEditList = []
        inputTextEditList.append(self.input1TextEdit)
        inputTextEditList.append(self.input2TextEdit)
        inputTextEditList.append(self.input3TextEdit)
        inputTextEditList.append(self.input4TextEdit)
        inputResultList = []
        for tmpIndex, tmpCheckFlag in enumerate(self.checkedList):
            if tmpCheckFlag == 0:
                nowInputList = [""]
            else:
                nowInputList = inputTextEditList[tmpIndex].toPlainText().replace("\r\n", "\n").split("\n")
            inputResultList.append(nowInputList)
        nowInputFormat = self.inputFormatLineEdit.text()
        nowInputFormat = nowInputFormat.replace("{", "{{")
        nowInputFormat = nowInputFormat.replace("}", "}}")
        for tmpIndex, tmpVal in enumerate(self.checkedList):
            nowInputFormat = nowInputFormat.replace("$%$输入值{0}$%$".format(tmpIndex + 1), "{" + str(tmpIndex) + "}")
        maxCoordinate = [len(a) - 1 for a in inputResultList]
        nowCoordinate = [0 for a in inputResultList]
        resultList = []

        ifAddFlag = True
        while ifAddFlag:
            nowResult = ""
            nowInputItemList = []
            for tmpIndex in range(0, len(inputResultList)):
                nowInputItemList.append(inputResultList[tmpIndex][nowCoordinate[tmpIndex]])
            nowResult = nowInputFormat.format(*nowInputItemList)
            if nowResult != "":
                resultList.append(nowResult)
            else:
                pass
            ifAddFlag, nowCoordinate = self.coordinatePlus(nowCoordinate, maxCoordinate)
        return resultList

    def coordinatePlus(self, nowCoordinate, maxCoordinate):
        ifAddFlag = False
        nowAddIndex = -1
        while not ifAddFlag:
            if len(nowCoordinate) + nowAddIndex == -1:
                ifAddFlag = False
                break
            else:
                nowCoordinateItem = nowCoordinate[nowAddIndex]
                nowMaxCoordinateItem = maxCoordinate[nowAddIndex]
                if nowCoordinateItem == nowMaxCoordinateItem:
                    tmpAddIndex = nowAddIndex
                    while tmpAddIndex != 0:
                        nowCoordinate[tmpAddIndex] = 0
                        tmpAddIndex = tmpAddIndex + 1
                    nowAddIndex = nowAddIndex - 1
                else:
                    nowCoordinate[nowAddIndex] = nowCoordinate[nowAddIndex] + 1
                    ifAddFlag = True
        return ifAddFlag, nowCoordinate

    def runJs(self):
        checkFlag, checkStr = self.checkInput()
        if not checkFlag:
            self.writeErrorLog(checkStr)
        else:
            try:
                url = self.urlLineEdit.text()
                while url[-1] == "/":
                    url = url[:-1]
                logStr = "开始加载URL：{0}".format(url)
                self.writeLog(logStr)
                self.browser.load(QUrl(url))
            except Exception as ex:
                logStr = "加载URL时出现异常：{0}".format(str(ex))
                self.writeErrorLog(logStr)

    def browserLoaded(self, ifSuccessFlag):
        if ifSuccessFlag:
            self.writeLog("URL加载完成")
            try:
                myUtils.clearTalbe(self.resultTable)
                nowJsFunction = self.jsFunTextEdit.toPlainText()
                nowJsFunction = myUtils.changeJsToString(nowJsFunction)
                nowJsStr = '''var script = document.createElement("script");
        script.type = "text/javascript";
        script.text = "{0}";
        document.body.appendChild(script);'''.format(nowJsFunction)
                self.browser.page().runJavaScript(nowJsStr)
                for tmpIndex, tmpInput in enumerate(self.inputFormattedList):
                    logStr = "使用输入值({1}/{2})：{0} 创建线程".format(tmpInput, tmpIndex + 1, len(self.inputFormattedList))
                    self.threadManage.addInput(tmpInput)
                    self.writeLog(logStr)
                logStr = "线程创建完成，结果请前往输出tab查看"
                self.writeLog(logStr)
            except Exception as ex:
                logStr = "启动JS函数执行线程管理线程时出现异常：{0}".format(str(ex))
                self.writeErrorLog(logStr)
        else:
            logStr = "无法加载URL，请检查网络连接"
            self.writeLog(logStr)

        # self.browser.page().runJavaScript(nowJsStr, self.jsCallBack)

    def closeEvent(self, event):
        self.browser.close()
        event.accept()

    def exportResult(self):
        nowTable = self.resultTable
        nowResultCount = nowTable.rowCount()
        if nowResultCount == 0:
            self.writeLog("当前无可导出数据")
            return
        self.exportExcellThread = ExportExcellThread(self.resultTable, 10000, self.resultHeaderList)
        self.exportExcellThread.signal_end.connect(self.exportCompleted)
        self.exportExcellThread.signal_log.connect(self.writeLog)
        self.exportExcellThread.start()
        self.writeLog("开始导出文件")
        self.exportResultButton.setEnabled(False)

    def exportCompleted(self, result, logStr):
        if result:
            self.writeLog(logStr)
        else:
            self.writeErrorLog(logStr)
        self.exportResultButton.setEnabled(True)

    def openConfigWindow(self):
        self.confWindow = ConfigWindow(self.confDic)
        self.confWindow.signal_end.connect(self.confWindowClosed)
        self.confWindow.show()

    def confWindowClosed(self):
        # 更新当前配置
        confFilePath = os.path.join(os.getcwd(), self.confFileName)
        confDic = myUtils.readConfFile(confFilePath)
        headerList = confDic["confHeader"]
        reConfDic = {"confFilePath": confFilePath, "confHeaderList": headerList,
                     "ifProxy": True if int(confDic[headerList[0]]) == 1 else False,
                     "proxyIp": confDic[headerList[1]], "proxyPort": confDic[headerList[2]]}

        # 更新代理设置
        self.updateProxy(reConfDic["ifProxy"], reConfDic["proxyIp"], reConfDic["proxyPort"])

        self.confDic = reConfDic

    def openHelpWindow(self):
        self.helpWindow.show()

    def updateProxy(self, ifUse, ip, port):
        proxy = QtNetwork.QNetworkProxy()
        if ifUse:
            proxy.setType(QtNetwork.QNetworkProxy.ProxyType.HttpProxy)
            proxy.setHostName(ip)
            proxy.setPort(port)
        else:
            proxy.setType(QtNetwork.QNetworkProxy.ProxyType.NoProxy)
        QtNetwork.QNetworkProxy.setApplicationProxy(proxy)

    def runJsThreadResultSolved(self, resultDic):
        nowInput = resultDic["input"]
        nowResult = resultDic["result"]
        self.updateTableResultThread.addResult(nowInput, nowResult)

    def jsConsoleErrorSolved(self,errorStr):
        logStr = "Javascript函数调用发生异常，异常信息为：{}".format(errorStr)
        self.writeLog("Javascript函数调用发生异常，请确认错误日志")
        self.writeLog(logStr, 1)

    def runJsThreadErrSolved(self, errDic):
        nowErrStr = errDic["errStr"]
        nowErrInput = errDic["input"]["input"]
        errLog = "输入值为：{} 的线程运行时发生异常".format(nowErrInput)
        self.writeErrorLog(errLog)
        errLog = "异常日志为：{}".format(nowErrStr)
        self.writeErrorLog(errLog)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainForm = Main()
    mainForm.show()
    sys.exit(app.exec_())
