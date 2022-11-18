from tkinter import *
from re import findall, MULTILINE
from sqlite3 import *


class Manager:
    def __init__(self):
        self.window = Tk()
        self.window.title('数据库学习')

    def label(self,txt):
        scroll = Scrollbar(self.window)
        t = Text(self.window, height=1, width=800)
        scroll.pack(side=RIGHT, fill=Y)  # 靠右安置与父对象高度相同
        t.pack(side=LEFT, fill=Y)  # 靠左安置与父对象高度相同
        scroll.config(command=t.yview)
        t.config(yscrollcommand=scroll.set)
        t.insert(END, txt)
        t.pack()

    def find(self,p1,p2):
        db = connect('employees.db')
        view = db.cursor()
        query = "select * from employees where first_name LIKE '{}%' OR last_name LIKE '{}%'".format(p1, p2)
        view.execute(query)
        return view.fetchall()

    def main(self,a,b):
        row = self.find(a,b)
        self.label(row)
        self.window.mainloop()


if __name__ == '__main__':
    m = Manager()
    a = input("please input first name you want find:")
    b = input("please input last name you want to find:")
    m.main(a,b)

