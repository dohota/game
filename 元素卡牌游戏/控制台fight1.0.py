import random


class Manage:
    energy = energy2 = 0
    # 双方的能源数量
    round = 1
    # 回合数
    command = ["gold", "def", "anti", "anti2", "def2", "anti3"]#指令集合
    # defend-time 可以连续防御的次数

    def __init__(self):
        pass

    def order_translation(self, oo):
        # 指令解释器，把数字指令封装成自然语言的指令，使得玩家易于理解
        # 作为指令解释器的同时，它也检查了指令是否可行
        o = oo.replace(" ", "")
        # 去除字符串的空格
        if o == Manage.command[0]:
            Manage.energy += 1
            return 0
        elif o == Manage.command[1]:
            return 1
        elif o == Manage.command[2]:
            if Manage.energy >= 1:
                Manage.energy -= 1
                return 2
                # 表示成功执行anti
            else:
                return -2
                # -2表示执行anti的能源不足
        elif o == Manage.command[3]:
            if Manage.energy >= 3:
                Manage.energy -= 3
                return 3
            else:
                return -3
        elif o == Manage.command[4]:
            if Manage.energy >= 1:
                Manage.energy -= 1
                return 4
            else:
                return -4
        elif o == Manage.command[5]:
            if Manage.energy >= 6:
                Manage.energy -= 6
                return 5
            else:
                return -5
        else:
            return -1
            # -1表示不存在的指令

    def enemy_ai(self):
        # 敌人的ai行为树
        r = int(random.random() * 1000)
        if Manage.energy2 == 0:
            enemy_action = r % 2
        elif 0 < Manage.energy2 <= 1:
            enemy_action = r % 3
            if (r > 500 and Manage.energy >= 3) or (r > 150 and Manage.energy >= 5):
                enemy_action = 4
        elif 1 < Manage.energy2 <= 3:
            enemy_action = r % 4
        elif Manage.energy2 >= 6:
            enemy_action = 5
        else:
            enemy_action = r % 5
        # 敌人执行指令，也有energy的增减
        if enemy_action == 0:
            Manage.energy2 += 1
        elif enemy_action == 2 or enemy_action == 4:
            Manage.energy2 -= 1
        elif enemy_action == 3:
            Manage.energy2 -= 3
        elif enemy_action == 5:
            Manage.energy -= 6
        return enemy_action

    def battle_calculate(self,u,e):
        if u == 5 or (u == 2 and e == 0) or (u == 3 and e < u):
            return 1
            # 表示游戏获胜
        elif e == 5 or (e == 2 and u == 0) or (e == 3 and u < e):
            return -1
        else:
            return 0

    def start(self):
        while True:
            print("-------Round:"+str(Manage.round)+"----------")
            while True:
                # 直到指令正确，才跳出循环
                your_order = input("Please input your order: ")
                your_num = self.order_translation(your_order)
                if your_num >= 0:
                    break
            enemy_action = self.enemy_ai()
            print("Enemy:"+Manage.command[enemy_action])
            if self.battle_calculate(your_num, enemy_action) == 1:
                # 计算胜利的条件
                print("you win!!!")
                break
            elif self.battle_calculate(your_num, enemy_action) == -1:
                print("you lose!")
                break
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            Manage.round += 1
            # 进入下一回合


if __name__ == "__main__":
    print("-----intro-----")
    # 这里可以写游戏的介绍
    m = Manage()
    m.start()