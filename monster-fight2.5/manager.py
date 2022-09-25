import sys
import time
from sound import *
from maps import *


class Collision:
    pass


class Page:
    def __init__(self):
        self.screen = pygame.display.set_mode((Fairy.sx,Fairy.sy))
        self.sound = Sound()

    def main(self):
        pygame.init()
        self.sound.back()
        pygame.display.set_caption("初始界面")
        self.screen.fill(Fairy.START_BACK)
        self.write('单人模式',400, 20)
        self.write('双人本机操作', 400, 200)
        self.write('双人联机',400, 300)
        self.write('游戏说明', 400, 400)
        while 1:
            time.sleep(0.1)
            pygame.display.update()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.MOUSEBUTTONUP:
                    xx, yy = pygame.mouse.get_pos()  # 获取鼠标位置
                    if 400 <= xx <= 400 + 20 and 20 <= yy <= 20 + 10:
                        m = Logic()
                        m.start()

    def write(self,t,x:float,y:float):
        font = pygame.font.Font('E:/图片/WenDaoXingYeSong-2.ttf', 30)
        text = font.render(t, True, (255, 0, 0), None)
        r = text.get_rect()
        r.topleft = (x, y)
        self.screen.blit(text, r)


class Logic:
    #计时器的id（id是什么数字不重要）,好像id值不能重复
    id = 0
    id2 = 1
    #计算游戏是第几局/回合
    j = 1

    def __init__(self):
        pygame.display.set_caption("怪物大战")
        self.screen = pygame.display.set_mode((Fairy.SCREEN_X,Fairy.SCREEN_Y),pygame.RESIZABLE)
        self.players = pygame.sprite.Group()
        self.enemys = pygame.sprite.Group()
        self.maps = Map(self.screen)
        self.sound = Sound()
        self.ran = [random.random()*10]
        self.rann = ['bedrock','brick','wool','stone']
        # 己方坦克有几条命
        self.life = 6
        # 计算一局游戏的存活时间，单位为秒
        self.timer = 0
        # 计算一局游戏的打怪数
        self.kill = 0

    def write(self,t,x:float,y:float):
        font = pygame.font.Font('E:/图片/WenDaoXingYeSong-2.ttf',30)
        text = font.render(t, True, (255, 0, 0), None)
        r = text.get_rect()
        r.topleft = (x, y)
        self.screen.blit(text, r)

    def player(self):
        #生成1个玩家
        p = Player(self.screen)
        self.players.add(p)

    def enemy(self,x=1):
        #生成x个Common敌人
        e = [Common(self.screen) for _ in range(x)]
        self.enemys.add(e)

    def restart(self):
        Logic.j += 1
        Logic.timer,Logic.score = 0, 0
        self.sound.horry()
        #清除所有子弹
        for i in self.players:
            i.all_bullet.empty()
        for j in self.enemys:
            j.all_bullet.empty()
        self.players.empty()#清除我方坦克
        self.enemys.empty()#清除敌方坦克
        self.maps.clear()#清除砖块
        mmmm = Page()
        mmmm.main()

    def minus_life(self,x=1):
        self.sound.boost()
        self.life -= x
        if self.life <= 0:
            self.restart()

    def ppp(self):
        # 我方坦克与敌方坦克碰撞
        tanks_pump = pygame.sprite.groupcollide(self.players, self.enemys, False, True)
        if tanks_pump: self.minus_life(3)
        # 子弹打坦克
        for a in self.enemys:
            e_hit_i = pygame.sprite.groupcollide(self.players, a.all_bullet, False, True)
            if e_hit_i: self.minus_life(1)
        for b in self.players:
            i_hit_e = pygame.sprite.groupcollide(b.all_bullet, self.enemys, True, True)
            if i_hit_e:
                self.kill += 1
                self.sound.boost()
        # 我方子弹碰到敌方子弹
        for c in self.players:
            for d in self.enemys:
                bullet_pump = pygame.sprite.groupcollide(c.all_bullet, d.all_bullet, True, True)
                if bullet_pump: self.sound.hit()
        # 坦克撞墙
        i_hit_wall = pygame.sprite.groupcollide(self.maps.bedrock, self.players, False, False)
        i_hit_brick = pygame.sprite.groupcollide(self.maps.brick, self.players, True, False)
        e_hit_wall = pygame.sprite.groupcollide(self.maps.bedrock, self.enemys, False, True)
        e_hit_brick = pygame.sprite.groupcollide(self.maps.brick, self.enemys, True, True)
        if i_hit_wall: self.minus_life(4)
        if i_hit_brick: self.minus_life(2)
        if e_hit_wall or e_hit_brick: self.sound.boost()
        # 坦克推墙
        i_hit_wool = pygame.sprite.groupcollide(self.maps.wool, self.players, False, False)
        i_hit_stone = pygame.sprite.groupcollide(self.maps.stone, self.players, False, False)
        e_hit_wool = pygame.sprite.groupcollide(self.maps.wool, self.enemys, False, False)
        e_hit_stone = pygame.sprite.groupcollide(self.maps.stone, self.enemys, False, False)
        if i_hit_wool or i_hit_stone or e_hit_wool or e_hit_stone:
            for i in i_hit_wool.keys():
                for ii in list(i_hit_wool.values())[0]:
                    i.pump(ii.direction, ii.speed, ii.rect)
            for j in i_hit_stone.keys():
                for jj in list(i_hit_stone.values())[0]:
                    j.pump(jj.direction, jj.speed, jj.rect)
            for k in e_hit_wool.keys():
                for kk in list(e_hit_wool.values()):
                    for kkk in kk:
                        k.pump(kkk.direction, kkk.speed, kkk.rect)
            for l in e_hit_stone.keys():
                for ll in e_hit_stone.values():
                    for lll in ll:
                        l.pump(lll.direction, lll.speed, lll.rect)
        # 墙推墙
        for i in list(self.maps.stone) + list(self.maps.wool):
            for j in list(self.maps.stone) + list(self.maps.wool):
                if i != j:
                    p = pygame.sprite.collide_rect(i, j)
                    if p: i.pump(j.dir2, j.speed2, j.rect)
        # 子弹撞墙
        for e in self.players:
            i_bullet_wall = pygame.sprite.groupcollide(self.maps.bedrock, e.all_bullet, False, True)
            i_bullet_wool = pygame.sprite.groupcollide(self.maps.wool, e.all_bullet, False, True)
            i_bullet_brick = pygame.sprite.groupcollide(self.maps.brick, e.all_bullet, False, True)
            i_bullet_stone = pygame.sprite.groupcollide(self.maps.stone, e.all_bullet, False, True)
            if i_bullet_wall or i_bullet_wool or i_bullet_stone or i_bullet_brick:
                self.sound.hit()
            for i in i_bullet_stone.keys():
                i.minus_life(1)
            for j in i_bullet_brick.keys():
                j.minus_life(1)
        for f in self.enemys:
            e_bullet_wall = pygame.sprite.groupcollide(self.maps.bedrock, f.all_bullet, False, True)
            e_bullet_wool = pygame.sprite.groupcollide(self.maps.wool, f.all_bullet, False, True)
            e_bullet_brick = pygame.sprite.groupcollide(self.maps.brick, f.all_bullet, False, True)
            e_bullet_stone = pygame.sprite.groupcollide(self.maps.stone, f.all_bullet, False, True)
            if e_bullet_wall or e_bullet_wool or e_bullet_brick or e_bullet_stone:
                self.sound.hit()
            for k in e_bullet_brick.keys():
                k.minus_life(1)
            for l in e_bullet_stone.keys():
                l.minus_life(1)

    def start(self):
        self.sound.back()
        self.player()
        self.maps.map1(random.randint(2,10),random.randint(0,2),'bedrock')
        pygame.time.set_timer(Logic.id,random.randrange(3500,8500,100))
        pygame.time.set_timer(Logic.id2, 1000)
        while 1:
            self.screen.fill(Fairy.GAME_BACK)
            #中文要借助外来字体显示
            self.write('玩家生命值:' + str(self.life), 20, 20)
            self.write('这是第' + str(Logic.j) + '轮游戏', 20, 50)
            self.write('游戏已经进行' + str(self.timer) + '秒', 20,80)
            self.write('消灭' + str(self.kill) + '个怪物', 20, 110)
            for i in self.players:
                i.control()
                i.display()
            for j in self.enemys:
                j.ai()
                j.display()
            self.maps.display_all()
            time.sleep(0.07)  # 防止monster跑得太快
            pygame.display.update()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == Logic.id:
                    self.enemy()
                    self.maps.map1(2, -1,self.rann[random.randint(0,3)])
                elif e.type == Logic.id2:
                    self.timer += 1
            self.ppp()


if __name__ == '__main__':
    m = Page()
    m.main()
