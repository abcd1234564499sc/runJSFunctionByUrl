# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainForm.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1096, 780)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.urlLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.urlLineEdit.setObjectName("urlLineEdit")
        self.gridLayout.addWidget(self.urlLineEdit, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)
        self.inputFormatLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.inputFormatLineEdit.setObjectName("inputFormatLineEdit")
        self.gridLayout.addWidget(self.inputFormatLineEdit, 1, 1, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.input1TextEdit = QtWidgets.QTextEdit(self.tab)
        self.input1TextEdit.setObjectName("input1TextEdit")
        self.verticalLayout.addWidget(self.input1TextEdit)
        self.input1CheckBox = QtWidgets.QCheckBox(self.tab)
        self.input1CheckBox.setCheckable(True)
        self.input1CheckBox.setChecked(True)
        self.input1CheckBox.setObjectName("input1CheckBox")
        self.verticalLayout.addWidget(self.input1CheckBox)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.input2TextEdit = QtWidgets.QTextEdit(self.tab)
        self.input2TextEdit.setObjectName("input2TextEdit")
        self.verticalLayout_2.addWidget(self.input2TextEdit)
        self.input2CheckBox = QtWidgets.QCheckBox(self.tab)
        self.input2CheckBox.setChecked(False)
        self.input2CheckBox.setObjectName("input2CheckBox")
        self.verticalLayout_2.addWidget(self.input2CheckBox)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.input3TextEdit = QtWidgets.QTextEdit(self.tab)
        self.input3TextEdit.setObjectName("input3TextEdit")
        self.verticalLayout_3.addWidget(self.input3TextEdit)
        self.input3CheckBox = QtWidgets.QCheckBox(self.tab)
        self.input3CheckBox.setObjectName("input3CheckBox")
        self.verticalLayout_3.addWidget(self.input3CheckBox)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.input4TextEdit = QtWidgets.QTextEdit(self.tab)
        self.input4TextEdit.setObjectName("input4TextEdit")
        self.verticalLayout_4.addWidget(self.input4TextEdit)
        self.input4CheckBox = QtWidgets.QCheckBox(self.tab)
        self.input4CheckBox.setObjectName("input4CheckBox")
        self.verticalLayout_4.addWidget(self.input4CheckBox)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.jsFunTextEdit = QtWidgets.QTextEdit(self.tab_3)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.jsFunTextEdit.setFont(font)
        self.jsFunTextEdit.setObjectName("jsFunTextEdit")
        self.horizontalLayout.addWidget(self.jsFunTextEdit)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.resetButton = QtWidgets.QPushButton(self.tab_3)
        self.resetButton.setObjectName("resetButton")
        self.verticalLayout_6.addWidget(self.resetButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.resultTable = QtWidgets.QTableWidget(self.tab_2)
        self.resultTable.setObjectName("resultTable")
        self.resultTable.setColumnCount(0)
        self.resultTable.setRowCount(0)
        self.horizontalLayout_2.addWidget(self.resultTable)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.exportResultButton = QtWidgets.QPushButton(self.tab_2)
        self.exportResultButton.setObjectName("exportResultButton")
        self.verticalLayout_7.addWidget(self.exportResultButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_7)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_5.addWidget(self.tabWidget)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.helpButton = QtWidgets.QPushButton(self.centralwidget)
        self.helpButton.setObjectName("helpButton")
        self.horizontalLayout_4.addWidget(self.helpButton)
        self.configButton = QtWidgets.QPushButton(self.centralwidget)
        self.configButton.setObjectName("configButton")
        self.horizontalLayout_4.addWidget(self.configButton)
        self.runButton = QtWidgets.QPushButton(self.centralwidget)
        self.runButton.setObjectName("runButton")
        self.horizontalLayout_4.addWidget(self.runButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.tabWidget_2 = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.tab_4)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.normalLogTextEdit = QtWidgets.QTextEdit(self.tab_4)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.normalLogTextEdit.setFont(font)
        self.normalLogTextEdit.setReadOnly(True)
        self.normalLogTextEdit.setObjectName("normalLogTextEdit")
        self.horizontalLayout_8.addWidget(self.normalLogTextEdit)
        self.tabWidget_2.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.tab_5)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.errorLogTextEdit = QtWidgets.QTextEdit(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.errorLogTextEdit.setFont(font)
        self.errorLogTextEdit.setReadOnly(True)
        self.errorLogTextEdit.setObjectName("errorLogTextEdit")
        self.horizontalLayout_9.addWidget(self.errorLogTextEdit)
        self.tabWidget_2.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab_6)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_8.addLayout(self.horizontalLayout_5)
        self.tabWidget_2.addTab(self.tab_6, "")
        self.verticalLayout_5.addWidget(self.tabWidget_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        self.input1CheckBox.stateChanged['int'].connect(MainWindow.updateInputFormat)
        self.input2CheckBox.stateChanged['int'].connect(MainWindow.updateInputFormat)
        self.input3CheckBox.stateChanged['int'].connect(MainWindow.updateInputFormat)
        self.input4CheckBox.stateChanged['int'].connect(MainWindow.updateInputFormat)
        self.runButton.clicked.connect(MainWindow.runJs)
        self.resetButton.clicked.connect(MainWindow.resetJsFunctionITextEdit)
        self.exportResultButton.clicked.connect(MainWindow.exportResult)
        self.helpButton.clicked.connect(MainWindow.openHelpWindow)
        self.configButton.clicked.connect(MainWindow.openConfigWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "JS函数调试工具箱"))
        self.label.setText(_translate("MainWindow", "URL"))
        self.label_6.setText(_translate("MainWindow", "输入格式"))
        self.label_2.setText(_translate("MainWindow", "输入1"))
        self.input1CheckBox.setText(_translate("MainWindow", "启用"))
        self.label_3.setText(_translate("MainWindow", "输入2"))
        self.input2CheckBox.setText(_translate("MainWindow", "启用"))
        self.label_4.setText(_translate("MainWindow", "输入3"))
        self.input3CheckBox.setText(_translate("MainWindow", "启用"))
        self.label_5.setText(_translate("MainWindow", "输入4"))
        self.input4CheckBox.setText(_translate("MainWindow", "启用"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "输入"))
        self.resetButton.setText(_translate("MainWindow", "重置"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "js处理函数"))
        self.exportResultButton.setText(_translate("MainWindow", "导出"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "输出"))
        self.helpButton.setText(_translate("MainWindow", "使用说明"))
        self.configButton.setText(_translate("MainWindow", "设置"))
        self.runButton.setText(_translate("MainWindow", "运行"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("MainWindow", "流程日志"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), _translate("MainWindow", "异常日志"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), _translate("MainWindow", "浏览器"))
