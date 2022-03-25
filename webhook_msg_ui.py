# -*- coding:utf-8 -*-
# 从Qt ui文件加载窗口界面
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import  QIcon
import requests
import datetime


class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('wx.ui')
        self.ui.pushButton.clicked.connect(self.handleCalc)

    def handleCalc(self):
        my_url = self.ui.Text_url.toPlainText()
        message = self.ui.Text_message.toPlainText()
        if len(my_url) == 0 or len(message) == 0:
            send_code = "请输入完整的信息"
        else:
            data = {
                "msgtype": "text",
                "text": {
                    "content": str(datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S %p')) + "\n" + message
                }
            }
            respond = requests.post(url=my_url, json=data)
            print(respond.json())
            if respond.json()['errcode'] == 0:
                send_code = "发送成功!"
            elif respond.json()['errcode'] == 93000:
                send_code = "发送失败!"
        QMessageBox.about(self.ui, "发送回执", send_code)


if __name__ == '__main__':

    app = QApplication([])
    app.setWindowIcon(QIcon('bitbug_favicon.ico'))
    stats = Stats()
    stats.ui.show()
    app.exec_()
