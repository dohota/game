import sys
from PyQt5.QtWidgets import *
from uach import *


class My(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(My, self).__init__(parent)
        self.setupUi(self)

    def add(self):
        a1 = self.lineEdit.text()
        a2 = self.lineEdit_2.text()
        a3 = self.lineEdit_3.text()
        x = self.comboBox.currentText()
        y = self.textEdit.toPlainText()
        pp = [a1,x,a3,a2,y]
        if not a1.isalpha():
            QMessageBox.about(self, '输入姓名警告', '只能有字母（包括汉字）')
        elif not a2.isdigit():
            QMessageBox.about(self,'注意身份证号','只能输入数字')
        elif not 5 < len(a2) <= 18:
            QMessageBox.about(self,'注意身份证号','需要6~18位')
        elif len(a3) > 5:
            QMessageBox.about(self,'输入专业警告','不能超过5字符')
        elif not a3.isalpha():
            QMessageBox.about(self,'输入专业警告','只能有字母（包括汉字）')
        else:
            for i in range(0,5):
                self.tableWidget.setItem(self.tableWidget.rowCount()-1, i,
                                     QTableWidgetItem(pp[i]))
            self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)

    def dell(self):
        x = self.lineEdit_4.text()
        # if (not x.isdigit()) or (x % 1 != 0):
        #     QMessageBox.about(self, '要求', '只能输入整数')
        if not (0 < int(x) <= self.tableWidget.rowCount()):
            # 把不是整数或数字的转换成int
            QMessageBox.about(self, '要求!', '不能超出范围')
        else:
            #把那一行的值都设为空
            # for i in range(0,5):
            #     self.tableWidget.setItem(,i,QTableWidgetItem(' '))
            self.tableWidget.removeRow(int(x)-1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #学习对象数组
    n = int(input('创建几个窗口：'))
    m = [My() for _ in range(n+1)]
    for i in range(1,n+1):
        m[i].show()
    sys.exit(app.exec())








