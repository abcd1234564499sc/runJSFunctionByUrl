#!/usr/bin/env python
# coding=utf-8
import traceback

import openpyxl as oxl
from PyQt5.QtCore import QThread, pyqtSignal

import myUtils


class ExportExcellThread(QThread):
    signal_end = pyqtSignal(bool, str)
    signal_log = pyqtSignal(str)

    def __init__(self, resultTable, saveCount=1000, resultHeaderList=[]):
        super(ExportExcellThread, self).__init__()
        self.resultTable = resultTable
        self.saveCount = saveCount
        self.resultHeaderList = resultHeaderList

    def run(self):
        nowTable = self.resultTable
        nowResultCount = nowTable.rowCount()
        filename = "导出文件 " + myUtils.getNowSeconed()
        filename = myUtils.updateFileNameStr(filename)
        resultFlag = False
        logStr = ""
        self.signal_log.emit("导出文件名为：{}".format(filename))
        try:
            # 创建一个excell文件对象
            wb = oxl.Workbook()
            # 创建URL扫描结果子表
            ws = wb.active
            ws.title = "JS函数执行结果"
            # 创建表头
            myUtils.writeExcellHead(ws, self.resultHeaderList)

            # 遍历当前结果
            self.signal_log.emit("开始导出结果")
            for rowIndex in range(nowResultCount):
                if rowIndex % self.saveCount == 0:
                    minIndex = rowIndex + 1
                    maxIndex = rowIndex + self.saveCount if nowResultCount > rowIndex + self.saveCount else nowResultCount
                    tmpLogStr = "正在导出{0}-{1}行数据".format(minIndex, maxIndex)
                    self.signal_log.emit(tmpLogStr)
                else:
                    pass
                # 获取当前行的值
                nowIndex = nowTable.item(rowIndex, 0).text()
                nowInput = nowTable.item(rowIndex, 1).text()
                nowResultStr = nowTable.item(rowIndex, 2).text()

                # 将值写入excell对象
                myUtils.writeExcellCell(ws, rowIndex + 2, 1, nowIndex, 0, True)
                myUtils.writeExcellCell(ws, rowIndex + 2, 2, nowInput, 0, True)
                myUtils.writeExcellCell(ws, rowIndex + 2, 3, nowResultStr, 0, True)
                myUtils.writeExcellSpaceCell(ws, rowIndex + 2, 4)
                # 指定数量行保存一次
                if rowIndex != 0 and rowIndex % self.saveCount == 0:
                    myUtils.saveExcell(wb, saveName=filename)
                    wb = oxl.open(filename)
                    ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
            # 设置列宽
            colWidthArr = [7, 20, 60]
            myUtils.setExcellColWidth(ws, colWidthArr)
            # 保存文件
            myUtils.saveExcell(wb, saveName=filename)
            resultFlag = True
            logStr = "成功保存文件：{0}.xlsx 至当前文件夹".format(filename)
            self.signal_end.emit(resultFlag, logStr)
        except Exception as ex:
            resultFlag = False
            logStr = "保存文件失败，报错信息为：{0}".format(traceback.format_exc())
            self.signal_end.emit(resultFlag, logStr)

