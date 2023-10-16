# fight项目文档：（怪物大战写了 636行代码）
# 4.0:
# 之后版本可以不搞AI，或者搞个简单的AI，大型AI费时间，费脑子
# 升级 coinA  N （从m级升到n级需要n-m个coinB）
# 升级 coinB  N （从m级升到n级需要n-m个coinA）
# n级coinA 每回合产出 n个coinA
# n级coinA 每回合产出 n个coinB
# 制作某种元素（作为子弹/盾牌）：make [type] [size^3] [name] 消耗type*（size^3//3）个coin
# 装填子弹：upload shoot [name1]&&[name2]&&[name3]...
# （游戏复杂了就需要给物品起名字，可以搞一个全局变量，把所有名字都加入全局变量来判断是否命名重复）
# 升级枪械： update shoot N
# （可以升级枪 释放子弹的初速度，枪口口径，弹夹容量）
# 射击：shoot（射出你装填的子弹）
# 盾牌：shield [name]
# 小盾牌合成大盾牌： form shield [shield_name] [name1]&&[name2][posI]&&[name3][posII]...
# （后一个盾牌相对于前一个盾牌的位置：前后上下左右）
# element类型：
# 液体也有体积（这里制作出的液体暂时不能被分割）
#   B玻璃，便宜易碎    C生物组织，有血量（和人体一样）    D金属
#   Q可以反弹的固体    R很软的固体  H水  S粘液 U磁铁 T沙子粉末，便宜伤害小   Z密度大，极其坚硬
#   大部分东西可以击碎B  击中C只有扣血效果
# 打中玩家的本体会扣血
# 伤害：尺寸、质量、接触面积、速度. 护甲：可能会被切断，击碎（取决于材料）
# 5.0：
# 随意选择玩家数量和敌人数量 以及多少阵营，每个阵营是哪些人，每个人都要起名字/生成名字 也可以生成随机游戏模式
# 可设定攻击目标
# 指令集完善 解析并判断指令的逻辑完善
# 可以把该游戏改造成一个文字冒险游戏：上下左右探索世界，有地形机制，和背包物品，还有交通工具.
# 但是仍然是回合制，可以把回合理解成是1秒钟/2秒。。。（较小的时间间隔）
# 或者只显示玩家的坐标，而不是画出整张地图。地面以平地为主，辅之以复杂地形
# 回城可以恢复很多东西，但是回城需要卷轴

# attack打shield时有几率打不中
class Make:
    def __init__(self, type, size, name, speed):
        # 名称检查器
        while True:
            if name in Order.make_name:
                name += "#"
            else:
                break
        print("The make name is" + name)
        self.name = name
        Order.make_name.append(self.name)
        self.speed = speed
        self.size_x = size.split("*")[0]
        self.size_y = size.split("*")[1]
        self.size_z = size.split("*")[2]
        if type == "B":
            self.density = 1
            self.p_max = 5
        elif type == "C":
            self.blood = 100
            self.density = 5
        elif type == "D":
            self.density = 8
            self.p_max = 20
        elif type == "Q":
            self.density = 3
            self.p_max = 200
        elif type == "R":
            self.density = 3
            self.p_max = 200
        elif type == "H":
            self.density = 1
        elif type == "S":
            self.density = 2
        elif type == "U":
            self.density = 4
            self.p_max = 5
        elif type == "T":
            self.density = 2
        elif type == "Z":
            self.density = 10
            self.p_max = 500
        if self.speed < 4:
            self.f_p = self.speed * self.size_x * self.density
        elif 4 <= self.speed < 7:
            self.f_p = self.speed * self.size_y * self.density
        else:
            self.f_p = self.speed * self.size_z * self.density

    def __add__(self, other):
        if isinstance(other, Make):
            return Make()

    def is_it_crush(self, u, e):
        if u.f_p >= e.p_max:
            u.f_p -= e.p_max
            return u, 0
        else:
            if u.f_p >= e.f_p:
                u.f_p -= e.f_p
# class MyClass:
#     def __init__(self, value):
#         self.value = value
#
#     def __add__(self, other):
#         if isinstance(other, MyClass):
#             return MyClass(self.value + other.value)
#         else:
#             raise TypeError("Unsupported operand type")
#
# a = MyClass(3)
# b = MyClass(4)
# c = a + b  # 调用 __add__ 方法
# print(c.value)  # 输出 7
class Bio:
    def __init__(self):
        self.coinA = 0
        self.coinB = 0
        self.coinA_level = 1
        self.coinB_level = 1
        self.element = []
        self.blood = 100
        self.shoot_level = 1
        # 弹夹
        self.bullet = []
        self.shield = []
        self.now_shield = ""

    def judge(self, s):
        if s[0] == "a":
            self.coinB -= s[1] - self.coinA_level
            self.coinA_level = s[1]
        elif s[0] == "b":
            self.coinA -= s[1] - self.coinB_level
            self.coinB_level = s[1]
        elif s[0] == "d":
            pass
        elif s[0] == "s":
            self.bullet = []
        elif s[0] == "u":
            self.coinA -= s[1] - self.shoot_level
            self.coinB -= s[1] - self.shoot_level
            self.shoot_level = s[1]
        elif s[0] == "m":
            ss = s.split("!")
            m = Make(ss[1], ss[2], ss[3], 0)
            self.element.append(m)
        elif s[0] == "k":
            ss = s.split("!")
            for i in ss[1:]:
                if i in Order.make_name:
                    self.element.pop(i)
                    self.bullet.append(i)
            # "k!" + '!'.join("".join(o1[2:]).split("&&"))
        elif s[0] == "l":
            ss = s.split("!")
            ss[1] = 2
            # "l!" + o1[2] +"!" + o1[3] + "!" + '!'.join("".join(o1[5:]).split("&&"))
        # 在最后增加coin
        self.coinA += self.coinA_level
        self.coinB += self.coinB_level

    # 这个方法使得写AI也更加方便
    def is_order_legal(self, order):
        if order[0] == "a":
            if order[1:] != int(order[1:]):
                return "incorrect num for A-level"
            if int(order[1:]) - self.coinA_level <= 0:
                return "incorrect A-level"
            if self.coinB >= int(order[1:]) - self.coinA_level:
                return 1
            else:
                return "not enough coinB"
        elif order[0] == "b":
            if order[1:] != int(order[1:]):
                return "incorrect num for B-level"
            if int(order[1:]) - self.coinB_level <= 0:
                return "incorrect B-level"
            if self.coinA >= int(order[1:]) - self.coinB_level:
                return 1
            else:
                return "not enough coinA"
        elif order[0] == "d":
            for i in Order.make_name:
                if i == order[1:]:
                    return 1
            return "no such shield name"
        elif order[0] == "s":
            if self.bullet:
                return 1
            else:
                return "the gun is empty"
        elif order[0] == "u":
            if order[1:] != int(order[1:]):
                return "incorrect num for update-shoot"
            if int(order[1:]) - self.shoot_level <= 0:
                return "incorrect shoot level"
            if self.coinA >= int(order[1:]) - self.shoot_level and self.coinB >= int(order[1:]) - self.shoot_level:
                return 1
            else:
                return "not enough coin"
        elif order[0] == "m":
            ss = order.split("!")
        elif order[0] == "k":
            return 1
        elif order[0] == "l":
            return 0


class Order:
    make_name = []

    @staticmethod
    def help():
        return print("----------help-----------")

    @staticmethod
    def order_translation(o):
        # 去除字符串左右的空格 o = o.strip()
        # 根据空格分隔字符串
        o1 = o.split()
        # 求列表元素数量
        if len(o1) == 2:
            if o1[0] == "coinA":
                return "a"+o1[1]
            elif o1[0] == "coinB":
                return "b"+o1[1]
            elif o1[0] == "shield":
                return "d"+o1[1]
            else:
                return "WRONG ORDER 002!"
        elif len(o1) == 1:
            if o1[0] == "shoot":
                return "s"
            elif o1[0] == "/help" or o1[0] == "help":
                return Order.help()
            else:
                return "WRONG ORDER 001!"
        elif len(o1) == 3 and o1[0] == "update":
            if o1[1] == "shoot":
                return "u"+o1[2]
            elif o1[0] == "make":
                return "m!" + o1[1] + "!" + o1[2] + "!" + o1[3]
            else:
                return "WRONG ORDER 003!"
        elif len(o1) >= 3:
            if o1[0] == "upload" and o1[1] == "shoot":
                if "&&" in o1[2:]:
                    # 拼接起来，用！分隔
                    return "k!" + '!'.join("".join(o1[2:]).split("&&"))
                else:
                    return "WRONG ORDER 0000&&"
            elif o1[0] == "form" and o1[1] == "shield":
                if len(o1) > 5 and "&&" in o1[5:]:
                    return "l!" + o1[2] + "!" + o1[3] + "!" + '!'.join("".join(o1[5:]).split("&&"))
                else:
                    return "WRONG ORDER 0001&&"
            else:
                return "WRONG ORDER 00X!"
        else:
            return "wrong order length!"
