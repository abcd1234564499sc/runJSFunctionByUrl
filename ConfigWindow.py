#!/usr/bin/env python
# coding=utf-8
import os.path

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QFileDialog

import myUtils
from ConnectProxy import ConnectProxy
from ui.configForm import Ui_ConfigForm


class ConfigWindow(QWidget, Ui_ConfigForm):
    signal_end = pyqtSignal()

    def __init__(self, confDic={}, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # 初始化后台任务对象
        self.connectProxyThread = ConnectProxy()
        # 根据传入的参数初始化数据
        self.confFilePath = confDic["confFilePath"]
        self.confHeadList = confDic["confHeaderList"]
        self.ifProxy = confDic["ifProxy"]
        self.proxyIp = confDic["proxyIp"]
        self.proxyPort = confDic["proxyPort"]
        self.ifExternalJS = confDic["ifExternalJS"]
        self.externalJSFolderPath = confDic["externalJSFolderPath"]
        # 初始化代理
        self.ifProxyCheckBox.setChecked(self.ifProxy)
        self.proxyIpLineEdit.setText(str(self.proxyIp))
        self.proxyPortLineEdit.setText(str(self.proxyPort))
        self.ifExternalJSCheckBox.setChecked(self.ifExternalJS)
        self.externalJSFolderPathLineEdit.setText(str(self.externalJSFolderPath))

    def saveConf(self):
        # 读取当前代理配置值
        nowProxyCheckStatus = False if int(self.ifProxyCheckBox.checkState()) == 0 else True
        nowProxyIp = self.proxyIpLineEdit.text().strip()
        nowProxyPort = self.proxyPortLineEdit.text().strip()
        nowExternalJSCheckStatus = False if int(self.ifExternalJSCheckBox.checkState()) == 0 else True
        nowExternalJSFolderPath = self.externalJSFolderPathLineEdit.text().strip()
        if not nowProxyCheckStatus:
            pass
        else:
            # 验证输入值是否符合规则
            if not myUtils.ifIp(nowProxyIp):
                warningStr = "输入的代理IP不符合IP规范"
                self.writeWarning(warningStr)
                return
            elif not nowProxyPort.isdigit():
                warningStr = "输入的代理端口必须是一个正整数"
                self.writeWarning(warningStr)
                return

        if not nowExternalJSCheckStatus:
            pass
        else:
            # 验证文件夹是否存在
            if not os.path.exists(nowExternalJSFolderPath):
                warningStr = "引用JS文件夹不存在"
                self.writeWarning(warningStr)
                return

        # 生成字典
        confDic = {self.confHeadList[0]: 1 if nowProxyCheckStatus else 0, self.confHeadList[1]: nowProxyIp,
                   self.confHeadList[2]: nowProxyPort, self.confHeadList[3]: 1 if nowExternalJSCheckStatus else 0,
                   self.confHeadList[4]: nowExternalJSFolderPath}

        # 保存到配置文件
        myUtils.writeToConfFile(self.confFilePath, confDic)

        self.writeWarning("保存成功")
        self.signal_end.emit()
        self.close()

    def writeWarning(self, warningStr):
        self.label_4.setText(warningStr)

    def updateConnectButtonStatus(self, status):
        if status == 0:
            self.testProxyButton.setEnabled(False)
            self.proxyIpLineEdit.setEnabled(False)
            self.proxyPortLineEdit.setEnabled(False)
        else:
            self.testProxyButton.setEnabled(True)
            self.proxyIpLineEdit.setEnabled(True)
            self.proxyPortLineEdit.setEnabled(True)

    def connectProxy(self):
        self.testProxyButton.setEnabled(False)
        nowProxyIp = self.proxyIpLineEdit.text().strip()
        nowProxyPort = self.proxyPortLineEdit.text().strip()
        # 验证输入值是否符合规则
        if not myUtils.ifIp(nowProxyIp):
            warningStr = "输入的代理IP不符合IP规范"
            self.writeWarning(warningStr)
            self.testProxyButton.setEnabled(True)
            return
        elif not nowProxyPort.isdigit():
            warningStr = "输入的代理端口必须是一个正整数"
            self.writeWarning(warningStr)
            self.testProxyButton.setEnabled(True)
            return
        # 测试连接
        warningStr = "正在连接代理服务器..."
        self.writeWarning(warningStr)
        self.connectProxyThread = ConnectProxy(nowProxyIp, nowProxyPort)
        self.connectProxyThread.signal_result.connect(self.proxyConnectResult)
        self.connectProxyThread.start()

    def proxyConnectResult(self, result):
        if result:
            warningStr = "连接成功"
            self.writeWarning(warningStr)
        else:
            warningStr = "连接失败"
            self.writeWarning(warningStr)
        self.testProxyButton.setEnabled(True)

    def updateExternalJSStatus(self, status):
        if status == 0:
            self.selectExternalJSFolderButton.setEnabled(False)
            self.externalJSFolderPathLineEdit.setEnabled(False)
        else:
            self.selectExternalJSFolderButton.setEnabled(True)
            self.externalJSFolderPathLineEdit.setEnabled(True)

    def selectExternalJSFolder(self):
        directory = QFileDialog.getExistingDirectory(self, "选择文件夹", "/")
        if directory:
            # 将结果写入显示输入框
            self.externalJSFolderPathLineEdit.setText(directory)
        else:
            pass
