import threading
import tkinter
from tkinter import messagebox
import random
import time
import sys


class Game(tkinter.Frame):
    energy1 = energy2 = 0
    defend_time1 = defend_time2 = 3
    round = 1
    a = -1
    enemy_action = -1

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Fighting Game")
        self.master.geometry("500x200")
        # 绑定关闭窗口的方法
        self.master.bind("<Destroy>", self.on_window_close)
        #self.v = self.master.StringVar()
        self.aa = ["energy", "defend", "attack"]
        self.pack()
        # 删除旧的部件
        while self.winfo_children():
            self.winfo_children()[0].destroy()
        self.create()

    def on_window_close(self,event):
        # event这个参数不能丢
        # 如果选择关闭窗口 ，不管是哪一个窗口，都会结束所有线程，结束整个程序
        print("窗口关闭")
        self.master.quit()
        del self
        sys.exit()

    @staticmethod
    def showing(a, b):
        messagebox.showinfo(a, b)

    def create(self):
        if Game.energy2 == 0:
            Game.enemy_action = int(random.random()*1000) % 2
        else:
            Game.enemy_action = int(random.random() * 1000) % 3
        if Game.defend_time2 == 0:
            Game.enemy_action = 0
        if Game.enemy_action == 0:
            Game.energy2 += 1
        elif Game.enemy_action == 1:
            Game.defend_time2 -= 1
        elif Game.enemy_action == 2:
            Game.energy2 -= 1
        l1 = tkinter.Label(self.master, text="Round"+str(Game.round))
        l1.pack()
        # 把Radiobutton放置在frame之中
        frame = tkinter.Frame(self.master)
        frame.pack()
        self.v = tkinter.StringVar()
        self.v.set("energy")  # 默认值
        r1 = tkinter.Radiobutton(self.master, text="Energy", value="energy", variable=self.v)
        # 不要写variable= tkinter.StringVar()，因为那样会导致Radiobutton选项不互斥
        r1.pack()
        r2 = tkinter.Radiobutton(self.master, text="Defend", value="defend", variable=self.v)
        r2.pack()
        r3 = tkinter.Radiobutton(self.master, text="Attack", value="attack", variable=self.v)
        r3.pack()
        b1 = tkinter.Button(self.master, text="Start the round", command=self.check_option())
        b1.pack()

    def check_option(self):
        if self.v.get() == "energy":
            Game.a = 0
            self.energy()
        elif self.v.get() == "defend":
            Game.a = 1
            self.defend()
        elif self.v.get() == "attack":
            Game.a = 2
            self.attack()

    def loop(self):
        print("adsdsdsdsdsdsd")
        if Game.enemy_action == 0 and Game.a == 2:
            Game.showing("you lose", "What a pity!")
            self.master.quit()
        if Game.enemy_action == 2 and Game.a == 0:
            Game.showing("you win", "Good job!")
            self.master.quit()
        if Game.a != -1:
            p1 = tkinter.Label(self.master, text="Your turn:"+self.aa[Game.a])
            p1.pack()
            p2 = tkinter.Label(self.master, text="Enemy turn:"+self.aa[Game.enemy_action])
            p2.pack()
            time.sleep(1)
            self.clear_screen()

    def clear_screen(self):
        # 游戏进入下一回合
        Game.round += 1
        # 重置这些参数，给下一回合使用
        Game.enemy_action = -1
        # 删除当前的Frame (清空屏幕)
        while self.winfo_children():
            self.winfo_children()[0].destroy()
        # 创建并添加一个新的Frame来替换旧的Frame
        new_frame = tkinter.Frame(self)
        new_frame.pack(fill="both", expand=True)

    def energy(self):
        Game.energy1 += 1

    def defend(self):
        if Game.defend_time1 <= 0:
            Game.showing("Warn!", "not allowed")
            return
        Game.defend_time1 -= 1

    def attack(self):
        if Game.energy1 <= 0:
            Game.showing("Warn!", "lack energy")
            return
        Game.energy1 -= 1

    def t(self):
        while True:
            self.loop()
            time.sleep(1)


if __name__ == "__main__":
    # 设置最大递归深度
    sys.setrecursionlimit(900)
    # window是其父窗口
    window = tkinter.Tk()
    app = Game(master=window)
    # 创建线程并启动
    thread = threading.Thread(target=app.t)
    thread.start()
    app.mainloop()
