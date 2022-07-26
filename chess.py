import sys
from PyQt5.QtWidgets import *
from uach import *
from chess_play import *
from plane_fight import *


class My(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(My, self).__init__(parent)
        self.setupUi(self)

    def start1(self):
        a = self.doubleSpinBox.value()
        m = Manager()
        m.main(a)

    def start2(self):
        a = self.comboBox.currentText()
        b = tuple(eval(a))
        m = Man()
        m.main(b)
        #注意：一次只能打开一个游戏窗口.退出游戏即退出程序
        #飞机大战重新开始游戏会出现错误
        #同时玩多个游戏可能需要多线程
        #如果多次按按钮，则会重新开始游戏


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #对象数组
    n = int(input('创建几个窗口：'))
    m = [My() for _ in range(n+1)]
    for i in range(n):
        m[i].show()
    sys.exit(app.exec())