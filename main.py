#!/usr/bin/env python
# coding=utf-8
import sys

import openpyxl as oxl
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView

import myUtils
from JsRunThreadManage import JsRunThreadManage
from ui.mainForm import Ui_MainWindow


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.checkedList = []
        self.inputFormattedList = []
        self.updateInputFormat()
        self.resetJsFunctionITextEdit()
        self.browser = QWebEngineView()
        self.browser.loadFinished.connect(self.browserLoaded)
        self.threadManage = JsRunThreadManage()
        # 设置结果表头
        self.resultHeaderList = ["序号", "输入", "输出"]
        self.resultTable.setColumnCount(len(self.resultHeaderList))
        self.resultTable.setHorizontalHeaderLabels(self.resultHeaderList)
        self.resultTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.resultTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.resultTable.verticalHeader().setVisible(False)

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
        functionModelStr = ''' function process(nowInputVal){\n    var nowOutputVal = "";\n    nowInputVal=String(nowInputVal);\n    // 逻辑代码\n    nowOutputVal=nowInputVal;\n    \n    return nowOutputVal;\n}'''
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
                self.threadManage = JsRunThreadManage(self.inputFormattedList, self.browser)
                self.threadManage.signal_result_log.connect(self.jsCallBack)
                self.threadManage.signal_info_log.connect(self.writeLog)
                self.threadManage.start()
            except Exception as ex:
                logStr = "启动JS函数执行线程管理线程时出现异常：{0}".format(str(ex))
                self.writeErrorLog(logStr)
        else:
            logStr = "无法加载URL，请检查网络连接"
            self.writeLog(logStr)

        # self.browser.page().runJavaScript(nowJsStr, self.jsCallBack)

    def jsCallBack(self, inputStr, result):
        nowTableRowCount = self.resultTable.rowCount()
        self.resultTable.insertRow(nowTableRowCount)
        self.resultTable.setItem(nowTableRowCount, 0, myUtils.createTableItem(str(nowTableRowCount + 1)))
        # self.resultTable.setItem(nowTableRowCount, 1,
        #                          myUtils.createTableItem(self.inputFormattedList[nowTableRowCount]))
        self.resultTable.setItem(nowTableRowCount, 1, myUtils.createTableItem(inputStr))
        self.resultTable.setItem(nowTableRowCount, 2, myUtils.createTableItem(result))

    def closeEvent(self, event):
        self.browser.close()
        event.accept()

    def exportResult(self):
        nowTable = self.resultTable
        nowResultCount = nowTable.rowCount()
        if nowResultCount == 0:
            self.writeLog("当前无可导出数据")
            return
        filename = "导出文件 " + myUtils.getNowSeconed()
        filename = myUtils.updateFileNameStr(filename)
        # 创建一个excell文件对象
        wb = oxl.Workbook()
        # 创建URL扫描结果子表
        ws = wb.active
        ws.title = "JS函数执行结果"
        # 创建表头
        myUtils.writeExcellHead(ws, self.resultHeaderList)

        # 遍历当前结果
        for rowIndex in range(nowResultCount):
            # 获取当前行的值
            nowIndex = nowTable.item(rowIndex, 0).text()
            nowInput = nowTable.item(rowIndex, 1).text()
            nowResultStr = nowTable.item(rowIndex, 2).text()

            # 将值写入excell对象
            myUtils.writeExcellCell(ws, rowIndex + 2, 1, nowIndex, 0, True)
            myUtils.writeExcellCell(ws, rowIndex + 2, 2, nowInput, 0, True)
            myUtils.writeExcellCell(ws, rowIndex + 2, 3, nowResultStr, 0, True)
            myUtils.writeExcellSpaceCell(ws, rowIndex + 2, 4)

        # 设置列宽
        colWidthArr = [7, 20, 60]
        myUtils.setExcellColWidth(ws, colWidthArr)
        # 保存文件
        myUtils.saveExcell(wb, saveName=filename)
        self.writeLog("成功保存文件：{0}.xlsx 至当前文件夹".format(filename))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainForm = Main()
    mainForm.show()
    sys.exit(app.exec_())
