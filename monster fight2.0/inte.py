import re


class A:
    def __init__(self):
        self.pos = 0
        self.ran = []
        self.all = ''
        self.c = self.all[self.pos]

    def main(self):
        file = open('E://学习//1.txt', 'r', encoding='utf-8')
        self.all = file.read()  # 读取文件全部
        file.close()
        self.all = ''.join(self.all.split())  # 去除空格
        #self.all.index('Map')
        print(self.all)

    def signal(self):
        while 1:
            if self.c == 'M':
                self.pos += 1
                if self.c == 'a':
                    self.pos += 1
                    if self.c == 'p':
                        self.pos += 1
                        if self.c == '{':
                            self.ran[0] = '10'
                            self.pos += 1
            if self.c == '{':
                self.ran[0] += 1
