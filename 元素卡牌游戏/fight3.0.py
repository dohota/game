import random
import re
# legal orders:
#
# gold1  0   | gold2   -3+5 | -5+8
# def1   0   | def2    -1   | -3   -5   -7  -9
# anti1  -1  |  anti2  -3   | -5
# back1  -1  |  back2  -3   | -5
# backing1 -1|  backing2 -1 | -1  -2

# 指令的传递还是有些问题，比如说函数调用指令等的问题，最好要写成一个统一的接口

class Bio:
    def __init__(self):
        self.energy = 0

    def judge(self, s):
        # 根据指令处理结果
        if s[0] == "a":
            if s[1] == "1":
                self.energy += 1
            else:
                self.energy += int(s[1])
                # 总共增加了n个能源
        elif s[0] == "b":
            if s[1] != "1":
                self.energy -= 2*int(s[1])-3
        elif s[0] == "c" or s[0] == "d":
            # back/backing 若不能成功抵挡，则游戏结束
            if s[1] == "1":
                self.energy -= 1
            else:
                self.energy -= 2*int(s[1])-1
        elif s[0] == "e":
            # backingN 只能抵挡 antiN
            if s[1] == "1":
                self.energy -= 1
            else:
                self.energy -= int((2*int(s[1])-1) // 3)


class Player(Bio):
    def order_translation(self, s):
        # 玩家类 需要翻译指令，并判断指令当前能否实现
        letter = re.sub(r'\d+', '', s).replace(" ", "")
        num = re.findall(r'\d+', s)
        if num:
            # 防止列表为空
            numm = int(num[0])
        else:
            return "No number in your order!"
        # num不可能含有小数点，也不可能是负数(因为小数点和负数符号会当作字符串处理)
        if len(num) == 0 or numm == 0:
            return "Wrong Number!"
        else:
            all_order = {"gold": ["a", 0, 2*numm-1], "def": ["b", 0, 2 * numm-3],
            "anti": ["c", 1, 2*numm-1], "back": ["d", 1, 2*numm-1], "backing": ["e", 1, int((2*numm-1) // 3)]}
            for key in all_order.keys():
                if letter == key:
                    if numm == 1 and self.energy >= all_order[key][1]:
                        return all_order[key][0]+"1"
                    if self.energy >= all_order[key][2]:
                        return all_order[key][0]+str(numm)
                    else:
                        return "lack energy for "+key+str(numm)
            return "wrong order!"
            # 不用字典的写法：要写好长一串
            # if letter == "gold":
            #     if numm == 1:
            #         return "a1"
            #     if self.energy >= 2*numm-1:
            #         return "a"+str(numm)
            #     else:
            #         return "lack energy for gold"+str(numm)
            # elif letter == "def":
            #     if numm == 1:
            #         return "b1"
            #     if self.energy >= 2 * numm - 3:
            #         return "b" + str(numm)
            #     else:
            #         return "lack energy for def" + str(numm)
            # elif letter == "anti":
            #     if numm == 1 and self.energy >= 1:
            #         return "c1"
            #     if self.energy >= 2 * numm - 1:
            #         return "c"+str(numm)
            #     else:
            #         return "lack energy for anti" + str(numm)
            # elif letter == "back":
            #     if numm == 1 and self.energy >= 1:
            #         return "d1"
            #     if self.energy >= 2 * numm - 1:
            #         return "d"+str(numm)
            #     else:
            #         return "lack energy for back" + str(numm)
            # elif letter == "backing":
            #     if numm == 1 and self.energy >= 1:
            #         return "e1"
            #     if self.energy >= int((2*numm-1) // 3):
            #         return "e"+str(numm)
            #     else:
            #         return "lack energy for backing" + str(numm)
            # else:
            #     return "wrong order!"


class Enemy(Bio):
    def ai(self, p_energy):
        # 非己方控制单位 用ai处理
        # 这个AI有点问题，但我打算下个版本再改
        r = int(random.random() * 1000)
        if self.energy <= 0:
            if p_energy == 0 or p_energy >= 3:
                enemy_action = "a1" # 玩家有3个能源可以必杀Ai
            else:
                if (r > 350 and p_energy == 1) or (r > 650 and p_energy == 2):
                    enemy_action = "a1"
                else:
                    enemy_action = "b1"
        elif self.energy == 1:
            if p_energy >= 7: # 玩家有7个能源才可以必杀Ai
                enemy_action = "a1"
            elif p_energy == 5 or p_energy == 6:
                if r > 450:
                    enemy_action = "c1" # 玩家有6个能源，很可能出gold3，若出gold3则必胜
                else:
                    enemy_action = ["a1", "b1", "d1", "e1", "e2", "e3"][r % 5]
            elif p_energy == 1 or p_energy == 2:
                enemy_action = ["b1", "c1", "e1", "a1"][r % 4]
            elif p_energy == 0:
                enemy_action = "c1"
            else:
                enemy_action = ["b1", "d1", "b2", "c1", "e1", "e2","a1"][r % 6]
        elif self.energy == 2:
            if p_energy >= 9:  # 玩家有9个能源才可以必杀Ai
                enemy_action = "a1"
            elif 5 <= p_energy < 9:
                if r > 250:
                    enemy_action = "a1"
                elif 50 < r < 250:
                    enemy_action = ["b1","b2","c1","d1"][r % 4]
                else:
                    enemy_action = "e" + str(r % 4 + 1)
            elif p_energy == 0:
                enemy_action = "c1"
            else:
                enemy_action = ["b1", "d1", "b2", "c1", "e1", "e2", "a1"][r % 6]
        else:
            if p_energy - self.energy >= 5:
                if r > 250:
                    enemy_action = "a" + str((self.energy + 1) // 2)
                elif 125 < r < 250:
                    enemy_action = "c" + str((self.energy + 1) // 2)
                else:
                    enemy_action = "d" + str((self.energy + 1) // 2)
            elif 2 <= p_energy - self.energy < 5 or -5 < p_energy - self.energy < -2:
                if r > 700:
                    enemy_action = "a" + str((self.energy + 1) // 2)
                elif 620 < r < 700:
                    enemy_action = "b" + str(r % ((self.energy + 3) // 2) + 1)
                elif 250 < r < 620:
                    enemy_action = "c" + str(r % ((self.energy + 1) // 2) + 1)
                elif 90 < r < 250:
                    enemy_action = "d" + str(r % ((self.energy + 1) // 2 + 1) + (self.energy + 1) // 2 - 3)
                else:
                    enemy_action = "e" + str(r % int(1.5 * self.energy + 2) + (1.5 * self.energy + 2) - 3)
            elif -2 <= p_energy - self.energy <= 2:
                if r > 700:
                    enemy_action = "a" + str((self.energy + 1) // 2)
                elif 550 < r < 700:
                    enemy_action = "b" + str(r % ((self.energy + 3) // 2) + 1)
                elif 250 < r < 550:
                    enemy_action = "c" + str(r % ((self.energy + 1) // 2) + 1)
                elif 50 < r < 250:
                    enemy_action = "d" + str(r % ((self.energy + 1) // 2) + 1)
                else:
                    enemy_action = "e" + str(r % int(1.5 * self.energy + 2) + 1)
            elif p_energy - self.energy <= -5:
                if r > 600:
                    enemy_action = "a" + str((self.energy + 1) // 2)
                else:
                    enemy_action = "c" + str(r % int(1.5 * self.energy + 2) + (1.5 * self.energy + 2) - 3)
        return enemy_action
        # 这里Pycharm给我发出了一个警告：enemy_action可能在赋值之前就引用

class Manage:
    def __init__(self):
        self.round = 1
        self.player = Player()
        self.enemy = Enemy()

    def round_calculate(self,u, e):
        if (self.if_it_win(u, e)) == 1:
            return "win"
        elif (self.if_it_win(e, u)) == 1:
            return "lose"
        else:
            return "none"

    def if_it_win(self,u, e):
        if (u[0] == "c" and e[0] == "a") \
                or (u[0] == "c" and (e[0] == "b" or e[0] == "c") and int(u[1:]) > int(e[1:])) \
                or (u[0] == "c" and e[0] == "d" and int(u[1:]) > int(e[1:])) \
                or (u[0] == "c" and e[0] == "e" and int(u[1:]) != int(e[1:])) \
                or (u[0] == "d" and e[0] == "c" and int(u[1:]) >= int(e[1:])) \
                or (u[0] == "e" and e[0] == "c" and int(u[1:]) == int(e[1:])):
            return 1  # u win
        else:
            return 0 # u not win

    def start(self):
        while True:
            print("-------Round:" + str(self.round) + "----------")
            enemy_action = self.enemy.ai(self.player.energy)
            self.enemy.judge(enemy_action)
            while True:
                # 直到指令正确，才跳出循环
                your_order = input("Please input your order: ")
                your_num = self.player.order_translation(your_order)
                if (your_num[0] == "a" or your_num[0] == "b" or your_num[0] == "c"
                    or your_num[0] == "d" or your_num[0] == "e"): # and isinstance(your_num[1:],int)
                    self.player.judge(your_num)
                    break
                else:
                    print(self.player.order_translation(your_order))
            print("Enemy:" + enemy_action) # 这里暂时就展示简单指令了
            # 评价对局结果
            if self.round_calculate(your_num, enemy_action) == "win":
                print("you win!!!")
                break
            elif self.round_calculate(your_num, enemy_action) == "lose":
                print("you lose!")
                break
            else:
                self.round += 1


if __name__ == "__main__":
    m = Manage()
    m.start()