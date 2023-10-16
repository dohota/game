from manage4 import *
import sys


class Manage:
    def __init__(self):
        self.round = 1
        self.player1 = Bio()
        self.player2 = Bio()

    def win_calculate(self, u, e):

        if self.player1.blood == 0:
            print("you lose")
            sys.exit()
        elif self.player1.blood == 0:
            print("you win")
            sys.exit()

    def round_calculate(self):
        pass

    def start(self):
        while True:
            print("-------Round:" + str(self.round) + "----------")
            while True:
                your_order = Order.order_translation(input("Please input your order: "))
                if self.player1.is_order_legal(your_order) == 1:
                    self.player1.judge(your_order)
                    break
                else:
                    print(self.player1.is_order_legal(your_order))
            while True:
                your_order2 = Order.order_translation(input("Please input your order: "))
                if self.player2.is_order_legal(your_order2) == 1:
                    self.player2.judge(your_order2)
                    break
                else:
                    print(self.player2.is_order_legal(your_order2))
            self.round_calculate(your_order, your_order2)
            self.round += 1


if __name__ == "__main__":
    m = Manage()
    m.start()