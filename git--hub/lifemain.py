import sys,random
from PyQt5.QtWidgets import *
from uach import *


class My(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(My, self).__init__(parent)
        self.setupUi(self)

    def enter(self):
        a1,a2,a3,a4,b3,c3,pl = self.steady()
        self.spinBox_2.setMaximum(20)
        self.spinBox_3.setMaximum(20)
        self.spinBox_4.setMaximum(20)

        y = self.lineEdit.text()
        if (not y.isalpha()) or (len(y) > 6):
            QMessageBox.about(self,'喂!',y+'不是一个正常的姓名')
            return
        x = self.spinBox.value()
        if x == 0:
            QMessageBox.about(self,'注意',y+'死于没有岁数')
            return

        z1 = self.spinBox_2.value()
        z2 = self.spinBox_3.value()
        z3 = self.spinBox_4.value()
        if z1+z2+z3 > 30:
            QMessageBox.about(self,'注意','点数之和不得超过30')
            return
        global trans
        QMessageBox.about(self,'0岁',y+'出生了')
        for i in range(1,x):
            if 1 <= i <= 12:
                QMessageBox.about(self,(str(i)+'岁的'+y)
                                  ,a1[int(random.random()*len(a1))])
            elif 12 < i < 22:
                QMessageBox.about(self, (str(i) + '岁的' + y),
                                  a2[int(random.random()*len(a2))])
                if i == 21:
                    ite1, ok1 = QInputDialog.getItem(self, y, '你的选择',
                                    ('创业', '打工', '摆烂'), 0, False)
                    if ite1 and ok1:
                        if ite1 == '创业':
                            trans = 10
                        elif ite1 == '打工':
                            trans = 20
                        else:
                            trans = 30
                    else:
                        trans = 30
            elif 22 <= i <= 55:
                if trans == 10:
                    QMessageBox.about(self, (str(i) + '岁的' + y)
                                  , a3[int(random.random()*len(a3))])
                elif trans == 20:
                    QMessageBox.about(self, (str(i) + '岁的' + y)
                                  , b3[int(random.random()*len(b3))])
                else:
                    QMessageBox.about(self, (str(i) + '岁的' + y)
                           , c3[int(random.random() * len(c3))])
            else:
                QMessageBox.about(self, (str(i) + '岁的' + y)
                                  , a4[int(random.random()*len(a4))])
        QMessageBox.about(self,(str(x)+'岁的'+y), y+'去世了')
        self.label_9.setText(pl[int(random.random()*len(pl))])

    def steady(self):
        good = ["很好", "真不赖", "简直完美", "棒棒哒", "蛮好", "还行", "中等", "不错"
            , "恶劣", "一般",
                "挺优秀", "很差", "太烂了", "还凑合", "很糟糕", "还能接受", "难以忍受"]
        fp = ["一直", "总是", "经常", "偶尔"]
        adj = ["挑食", "矫情", "内向", "乖巧", "沉默", "活泼", "调皮", "优秀", "奇怪"]
        adv = ["非常", "比较", "有点", "尤其", "很"]
        like = ["像一朵巨大的奇葩", "是一根可爱的棒棒糖", "如同一只走狗", "宛如一颗库柏",
                "跟个大仙一样",
                "及其不好惹", "是个绅士"]
        adj2 = ["凶横的", "可爱的", "亲爱的", "优秀的", "有钱的", "窘迫的", "憨态可掬的",
                "中肯的",
                "一针见血的", "不要脸的"]
        q = ["智商", "情商", "德商", "财商", "美商", "体育能力"]
        subj = ["化学", "物理", "生物", "美术", "音乐", "体育", "语文", "数学",
                "英语", "地理",
                "历史"]
        hobby = ["滑雪", "踢足球", "打篮球", "垫排球", "打棒球", "投掷铅球",
                 "丢沙包", "耍滑板",
                 "瞎起哄",
                 "干神秘的事情", "玩水"]
        adj3 = ["兴奋", "快活", "自豪", "自负", "搞笑", "神秘", "伤心", "自卑",
                "无聊", "劳累", "害怕",
                "焦虑"]
        time = ["早上", "下午", "傍晚", "中午"]
        place = ["竹林里", "房间里", "别人家里", "平坦的地上", "沙滩上", "小河边", "树林里"]
        adj4 = ["帮博士跑腿的", "整天996的", "整天007的", "受排斥的", "抑郁难受的",
                "兴高彩烈的",
                "壮志难酬的"]
        n = ["鲜花", "戒指", "红包", "项链", "一个故事", "%……&YFvf", "一首诗"]
        pl = ["重庆", "北京", "", "安徽宏村", "安徽黄山", "福建武夷山", "福建霞浦", "鸣沙山",
              "开平碉楼",
              "广西阳朔", "贵州黄果树瀑布", "月牙泉", "一块附魔书", "世外桃源", "洱海月湿地公园",
              "小普陀", "岩石园"]
        thing = ["一个游泳池", "一个大别墅", "岩石园", "一块翡翠", "一包辣条", "一间卧室",
                 "一克反物质", "化学药剂"]
        chem = ["一瓶双氧水", "1kg弱酸", "200g强碱", "一个高能粒子", "神秘的UFO"]
        anim = ["猛虎", "鳄鱼", "狮子", "棕熊", "熊猫"]
        body = ["腿脚", "肾脏", "肝脏", "脾胃", "心脏", "记忆", "平衡", "行为", "性格",
                "脾气", "皮肤", "眼睛", "耳朵"]

        a1 = []
        a2 = []
        a3 = []
        b3 = []
        c3 = []
        a4 = []
        for k in good:
            for kk in fp:
                a1.append("你在学校" + kk + k + "，哈哈哈！")
                a1.append("你在家里" + kk + k + "，嘻嘻~")
        for k in adj:
            for kk in adv:
                a1.append("老师说你" + kk + k + "，啧！")
        for k in like:
            for kk in adj2:
                a1.append(kk + "同学说你" + k + "，嘿嘿！")

        for k in q:
            for kk in adv:
                a1.append("别人感觉你" + k + kk + "一般!")
                a1.append("别人觉得你" + k + kk + "好~")

        a1.append("你在晚上能看到一个黑影在房间里穿梭")
        for k in subj:
            a2.append("你反感" + k + "老师，所以翘他的课")

        for k in hobby:
            for kk in good:
                a2.append("你课余时间" + k + "，成绩" + kk + "了~")

        for k in adj3:
            for kk in good:
                a2.append("你开始变得" + k + "，并感到自己未来会" + kk + "~")

        for k in subj:
                a2.append("你最近喜欢" + k + "，想选xx专业")

        for k in time:
            for kk in place:
                for k3 in hobby:
                    a2.append(k + "你在" + kk + k3)
        a2.append("你和隔壁班同学干了起来")
        a2.append("你一直能看到那个耀眼的UFO")
        a2.append("你聆听外星人的谈话，可啥也没听懂")
        a2.append("你有一种不详的预感，可你又是无神论者")
        a2.append("你在期待那个神秘人！")

        for k in subj:
            a3.append("你做了" + k + "相关的工作")

        for k in adj4:
            for kk in adj3:
                b3.append("你成为了" + k + "打工人，感到" + kk)
        for k in adj3:
            a3.append("你准备创业，一开始" + k)
        for k2 in fp:
            for k3 in good:
                a3.append("你自主创业，结果" + k2 + k3)

        for k in n:
            a3.append("你结婚了，送给配偶" + k)
            b3.append("你结婚了，送给配偶" + k)
            c3.append("你结婚了，送给配偶" + k)

        for k in place:
            for k2 in time:
                c3.append("在一个" + k2 + "你们去" + k + "度假")
                a3.append("在一个" + k2 + "你们把家搬到了" + k)

        for k in place:
            c3.append("你参加了别人举办的，去" + k + "的探险活动")

        for k in thing:
            a3.append("你买了" + k)
        for k in like:
            a3.append("单位的人议论你" + k)
            b3.append('单位人议论你'+k)

        for k in time:
            for k2 in time:
                for k3 in chem:
                    a3.append("你做实验从" + k + "做到" + k2 + "用了" + k3)
                    b3.append("你做实验从" + k + "做到" + k2 + "用了" + k3)

        for k in anim:
            for k2 in fp:
                a3.append("你在外面" + k2 + "瞥见" + k + "，它在瞌睡")
                a3.append("你外出的时候" + k2 + "看到" + k + "，它和同伴玩耍")
                b3.append("你隐约" + k2 + "察觉一只小" + k + "，它踽踽独行很可怜")
                a3.append("你做梦" + k2 + "梦到" + k + "，它试图把你逼向绝路")
        c3.append("karl遮住了你的眼睛，但你明显看见了一个UFO")
        c3.append("你遇到了一个小鬼：不给糖，就捣蛋")
        c3.append("道路是曲折的，前途是光明的")

        for k in hobby:
            a4.append("你退休了，所以整天" + k)

        for k in subj:
            for k2 in adj3:
                a4.append("你思考" + k + "但感到" + k2)

        for k in q:
            for k2 in good:
                a4.append("你的" + k + "变得" + k2)

        for k in body:
            for k2 in good:
                a4.append("你的" + k + "变得" + k2)
        for k in hobby:
            a4.append("你又想起了儿时的" + k)
            a4.append("你想到了壮年的" + k)

        a4.append("楼上那位说家不远处有猛兽出没")
        a4.append("#……&*T-G-J-B-J-K-B-J-H-I-##）（**&*&")
        random.shuffle(a1)
        random.shuffle(a2)
        random.shuffle(a3)
        random.shuffle(a4)
        random.shuffle(b3)
        random.shuffle(c3)
        return a1,a2,a3,a4,b3,c3,pl


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #对象数组
    n = int(input('创建几个窗口：'))
    m = [My() for _ in range(n+1)]
    for i in range(n):
        m[i].show()
    sys.exit(app.exec())








