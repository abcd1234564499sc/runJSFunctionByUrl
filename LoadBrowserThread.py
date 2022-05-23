#!/usr/bin/env python
# coding=utf-8
from PyQt5.QtCore import QThread, QUrl


class LoadBrowserThread(QThread):
    def __init__(self,browser=None,url=""):
        super(LoadBrowserThread, self).__init__()
        self.browser = browser
        self.url = url

    def run(self):
        self.browser.load(QUrl(self.url))

