import random


class Bio:
    def __init__(self):
        self.energy = 0

    def judge(self, a):
        # 根据指令处理结果
        if a == 0:
            self.energy += 1
        elif a == 2 or a == 4:
            self.energy -= 1
        elif a == 3:
            self.energy -= 3
        elif a == 5:
            self.energy -= 6
        elif a == 6:
            self.energy -= 5
        else:
            pass


class Player(Bio):
    def order_translation(self, oo):
        # 玩家类 需要翻译指令，并判断指令当前能否实现
        o = oo.replace(" ", "")
        if o == Manage.command[0]:
            return 0
        elif o == Manage.command[1]:
            return 1
        elif o == Manage.command[2]:
            if self.energy >= 1:
                return 2
            else:
                return "lack energy for anti order"
        elif o == Manage.command[3]:
            if self.energy >= 3:
                return 3
            else:
                return "lack energy for anti2 order"
        elif o == Manage.command[4]:
            if self.energy >= 1:
                return 4
            else:
                return "lack energy for def2 order"
        elif o == Manage.command[5]:
            if self.energy >= 6:
                return 5
            else:
                return "lack energy for anti3 order"
        elif o == Manage.command[6]:
            if self.energy >= 5:
                return 6
            else:
                return "lack energy for back order"
        else:
            return "wrong order!"


class Enemy(Bio):
    def ai(self, p_energy):
        # 非己方控制单位 用ai处理
        r = int(random.random() * 1000)
        if self.energy == 0:
            if p_energy == 0 or p_energy >= 3:
                enemy_action = 0
            else:
                if (r > 350 and p_energy == 1) or (r > 650 and p_energy == 2):
                    enemy_action = 0
                else:
                    enemy_action = 1
        elif self.energy < 6 and self.energy != 0:
            if (abs(p_energy - self.energy) > 2) or p_energy == self.energy:
                if self.energy == 1 or self.energy == 2:
                    if r > 750:
                        enemy_action = 4
                    else:
                        enemy_action = r % 3
                else:
                    enemy_action = r % 5
            else:
                if self.energy == 1 or self.energy == 2:
                    if r > 890 - 20 * p_energy:
                        enemy_action = 4
                    else:
                        enemy_action = r % 3
                else:
                    if r > 800:
                        enemy_action = 2
                    elif 700 < r < 800:
                        enemy_action = 4
                    else:
                        enemy_action = r % 5
        else:
            if r > 700 - 25 * p_energy:
                enemy_action = 6
            else:
                enemy_action = 5
        if self.energy >= 1 and p_energy == 0:
            enemy_action = 2
        elif p_energy >= 5:
            enemy_action = 0
        return enemy_action


class Manage:
    command = ["gold", "def", "anti", "anti2", "def2", "anti3", "back"]

    def __init__(self):
        self.round = 1
        self.player = Player()
        self.enemy = Enemy()

    def round_calculate(self, u, e):
        if (u == 5 and e != 6) or (u == 2 and e == 0) or (u == 3 and e < u) \
                or (u == 6 and (e == 2 or e == 3 or e == 5)):
            return "win"
            # 表示游戏获胜
        elif (e == 5 and u != 6) or (e == 2 and u == 0) or (e == 3 and u < e) \
                or (e == 6 and (u == 2 or u == 3 or u == 5)):
            return "lose"
        else:
            return 0

    def start(self):
        while True:
            print("-------Round:" + str(self.round) + "----------")
            enemy_action = self.enemy.ai(self.player.energy)
            self.enemy.judge(enemy_action)
            while True:
                # 直到指令正确，才跳出循环
                your_order = input("Please input your order: ")
                your_num = self.player.order_translation(your_order)
                if isinstance(your_num, int) and your_num >= 0:
                    self.player.judge(your_num)
                    break
                else:
                    print(self.player.order_translation(your_order))
            print("Enemy:" + Manage.command[enemy_action])
            # 评价对局结果
            if self.round_calculate(your_num, enemy_action) == "win":
                print("you win!!!")
                break
            elif self.round_calculate(your_num, enemy_action) == "lose":
                print("you lose!")
                break
            else:
                self.round += 1
                # 进入下一回合


if __name__ == "__main__":
    m = Manage()
    m.start()