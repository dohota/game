# pyqt
This is meant to learn python-pyqt5


#1.manage是一个实体管理系统
#2.life是一个人生模拟器（复杂功能没实现）

#3.uach 是一个qt designer编译的页面文件
#4.chess是一个逻辑文件，用来调用两个游戏

#5.chess—play是五子棋游戏
五子棋的问题：1.有的时候五个棋子相连却不能判断出来
2.黑棋/白棋胜利的字体不能显示出来

#6.plane-flight是飞机大战游戏
飞机大战的问题：1.两个飞机碰撞时没有爆炸效果（其实这个爆炸效果也不重要）
2.显示game over的时候字跳的太快了
显示字的时候会被别的东西遮盖住（可以结合pyqt进行改进）

#7.总结：以上四个文件用pyqt调用了pygame的代码
不过有部分问题，未来说不定能通过多线程解决
1.一次只能打开一个游戏窗口.退出游戏即退出程序
2.飞机大战重新开始游戏会出现错误
3.如果多次按按钮，则会重新开始游戏

学习pygame和pyqt的目的不在于做出多么厉害的东西，而是在于学会基础操作
为未来打下基础。真正做游戏可以用unity（要学c#）
博客园--我的博客：https://www.cnblogs.com/karl-lighting/
普通游戏一般用单线程，性能不够了可能会用多线程

#8.tank-fight是坦克大战游戏
实现了各种的方块，实现了和敌方坦克战斗，音效和碰撞的逻辑
这个游戏没啥问题，但还需要优化一下：
1.增强代码的可拓展性，增加更多的音效和地图类型
2.完善敌方坦克的Ai
3.实现socket联机，开房间

#9 tank和battle是坦克大战10.0版本的两个文件
10.0版本初步实现了游戏界面

###3D游戏不一定需要unity，可以用js和后端来搞，同时需要blender3D建模

#10 怪物大战2.0：基本实现了坦克大战向怪物大战的过渡，同时增加了挡位机制（比较复杂）
接下来怪物大战会有很多种类的怪物，武器，道具，属性
pygame好像一直都不能显示中文
其中有个inte.py是我弄的一个未完成的游戏解释器

