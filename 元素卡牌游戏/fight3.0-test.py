import re
import random
# 4.0或者4.0之后的目标：
# 随意选择玩家数量和敌人数量 以及多少阵营，每个阵营是哪些人，每个人都要起名字/生成名字 也可以生成随机游戏模式
# 可设定攻击目标
# 指令集完善 解析并判断指令的逻辑完善


def order_translation(s, energy=3):
    # 玩家类 需要翻译指令，并判断指令当前能否实现
    letter = re.sub(r'\d+', '', s).replace(" ", "")
    num = re.findall(r'\d+', s)
    if num:
        numm = int(num[0])
    else:
        return "No number in your order!"
    # num不可能含有小数点，也不可能是负数(因为小数点和负数符号会当作字符串处理)
    if len(num) == 0 or numm == 0:
        return "Wrong Number!"
    else:
        all_order = {"gold": ["a", 0, 2 * numm - 1], "def": ["b", 0, 2 * numm - 3],
                     "anti": ["c", 1, 2 * numm - 1], "back": ["d", 1, 2 * numm - 1],
                     "backing": ["e", 1, int((2 * numm - 1) // 3)]}
        for key in all_order.keys():
            if letter == key:
                if numm == 1 and energy >= all_order[key][1]:
                    return all_order[key][0] + "1"
                if energy >= all_order[key][2]:
                    return all_order[key][0] + str(numm)
                else:
                    return "lack energy for " + key + str(numm)
        return "wrong order!"

def round_calculate(u, e):
    if(if_it_win(u, e)) == 1:
        return "win"
    elif(if_it_win(e, u)) == 1:
        return "lose"
    else:
        return "none"

def if_it_win(u,e):
    if (u[0] == "c" and e[0] == "a") \
            or (u[0] == "c" and (e[0] == "b" or e[0] == "c") and int(u[1:]) > int(e[1:])) \
            or (u[0] == "c" and e[0] == "d" and int(u[1:]) > int(e[1:])) \
            or (u[0] == "c" and e[0] == "e" and int(u[1:]) != int(e[1:])) \
            or (u[0] == "d" and e[0] == "c" and int(u[1:]) >= int(e[1:])) \
            or (u[0] == "e" and e[0] == "c" and int(u[1:]) == int(e[1:])):
        return 1 # u win
    else:
        return 0

def ai(energy, p_energy):
        # 非己方控制单位 用ai处理
        r = int(random.random() * 1000)
        if energy <= 0:
            if p_energy == 0 or p_energy >= 3:
                enemy_action = "a1" # 玩家有3个能源可以必杀Ai
            else:
                if (r > 350 and p_energy == 1) or (r > 650 and p_energy == 2):
                    enemy_action = "a1"
                else:
                    enemy_action = "b1"
        elif energy == 1:
            if p_energy >= 7: # 玩家有7个能源才可以必杀Ai
                enemy_action = "a1"
            elif p_energy == 5 or p_energy == 6:
                if r > 450:
                    enemy_action = "c1" # 玩家有6个能源，很可能出gold3，若出gold3则必胜
                else:
                    enemy_action = ["a1", "b1", "d1", "e1", "e2", "e3"][r % 5]
            elif p_energy == 0:
                enemy_action = "c1"
            elif p_energy == 1 or p_energy == 2:
                enemy_action = ["b1", "c1", "e1", "a1"][r % 4]
            else:
                enemy_action = ["b1", "d1", "b2", "c1", "e1", "e2", "a1"][r % 6]
        elif energy == 2:
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
            if p_energy - energy >= 5:
                if r > 250:
                    enemy_action = "a" + str((energy + 1) // 2)
                elif 125 < r < 250:
                    enemy_action = "c" + str((energy + 1) // 2)
                else:
                    enemy_action = "d" + str((energy + 1) // 2)
            elif 2 <= p_energy - energy < 5 or -5 < p_energy - energy < -2:
                if r > 700:
                    enemy_action = "a" + str((energy + 1) // 2)
                elif 620 < r < 700:
                    enemy_action = "b" + str(r % ((energy + 3) // 2) + 1)
                elif 250 < r < 620:
                    enemy_action = "c" + str(r % ((energy + 1) // 2) + 1)
                elif 90 < r < 250:
                    enemy_action = "d" + str(r % ((energy + 1) // 2 + 1) + (energy + 1) // 2 - 3)
                else:
                    enemy_action = "e" + str(r % int(1.5 * energy + 2) + (1.5 * energy + 2) - 3)
            elif -2 <= p_energy - energy <= 2:
                if r > 700:
                    enemy_action = "a" + str((energy + 1) // 2 + 1)
                elif 550 < r < 700:
                    enemy_action = "b" + str(r % ((energy + 3) // 2) + 1)
                elif 250 < r < 550:
                    enemy_action = "c" + str(r % ((energy + 1) // 2) + 1)
                elif 50 < r < 250:
                    enemy_action = "d" + str(r % ((energy + 1) // 2) + 1)
                else:
                    enemy_action = "e" + str(r % int(1.5 * energy + 2) + 1)
            elif p_energy - energy <= -5:
                if r > 600:
                    enemy_action = "a" + str((energy + 1) // 2)
                else:
                    enemy_action = "c" + str(r % int(1.5 * energy + 2) + (1.5 * energy + 2) - 3)
        return enemy_action
