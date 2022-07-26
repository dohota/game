import pygame
import sys
import time
import random


class Auto(pygame.sprite.Sprite):
    #自己的飞机类
    topb = pygame.sprite.Group()
    #类变量

    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.auto = pygame.image.load("E:/图片/plane1.jpg")
        self.rect = self.auto.get_rect()
        # self.x = 300,self.y = 300
        self.rect.topleft = [300,300]
        self.speed = 5
        self.screen = screen
        self.bu = pygame.sprite.Group()

    def control(self):
        #按键控制
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w]:
            self.rect.top -= self.speed
        if key_pressed[pygame.K_s]:
            self.rect.bottom += self.speed
        if key_pressed[pygame.K_a]:
            self.rect.left -= self.speed
        if key_pressed[pygame.K_d]:
            self.rect.right += self.speed
        if key_pressed[pygame.K_SPACE]:
            b = Bullet(self.screen,self.rect.left,self.rect.top)
            self.bu.add(b)
            Auto.topb.add(b)

    def display(self):
        self.screen.blit(self.auto,self.rect)
        self.bu.update()
        self.bu.draw(self.screen)

    def update(self):
        self.control()
        self.display()

    @classmethod
    #清空子弹
    def clear(cls):
        cls.topb.empty()


class Enemy(pygame.sprite.Sprite):
    #敌机类
    tope = pygame.sprite.Group()

    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.en = pygame.image.load("E:/图片/enemy.jpg")
        self.rect = self.en.get_rect()
        x = random.randrange(1,1000,50)
        self.rect.topleft = [x,0]
        #相当于self.x，self.y的位置,生成敌机的初始位置
        self.speed = 6
        self.screen = screen
        self.bu = pygame.sprite.Group()
        self.dire = True#方向

    def display(self):
        self.screen.blit(self.en,self.rect)
        self.bu.update()
        self.bu.draw(self.screen)

    def auto(self):
        #判断方向
        if self.dire:
            self.rect.right += self.speed
        else:
            self.rect.right -= self.speed
        #控制转向
        if self.rect.right > 850:
            self.dire = False
        elif self.rect.right < 0:
            self.dire = True
        self.rect.bottom += self.speed

    def ai(self):
        #用随机数来判断防止发太多子弹
        r = random.randint(1,20)
        if r == 6:
            bb = Bu(self.screen,self.rect.left,self.rect.top)
            self.bu.add(bb)
            Enemy.tope.add(bb)

    def update(self):
        self.auto()
        self.ai()
        self.display()

    @classmethod
    # 清空子弹
    def clear(cls):
        cls.tope.empty()


class Bullet(pygame.sprite.Sprite):
    def __init__(self,screen,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("E:/图片/buee.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        self.screen = screen
        self.speed = 10

    def update(self):
        self.rect.top -= self.speed
        if self.rect.top < -20:
            #子弹越界则清除子弹对象
            self.kill()


class Bu(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("E:/图片/buee.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.screen = screen
        self.speed = 10

    def update(self):
        self.rect.top += self.speed
        if self.rect.top > 800:
            self.kill()


class Pumb:
    def __init__(self,screen,f):
        self.screen = screen
        if f:
            #判断类型，决定爆炸
            self.bo = pygame.image.load("E:/图片/boom.jpg")
        else:
            self.bo = pygame.image.load("E:/图片/boost.jpg")
        self.pos = [0,0]
        self.look = False
        #可见/不可见

    def action(self,rect):
        self.pos = rect.left
        self.look = False

    def draw(self):
        if not self.look:
            return
        self.screen.blit(self.bo,(self.pos[0],self.pos[1]))
        self.look = False


class Sound:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load("E:/图片/back.mp3")
        pygame.mixer.music.set_volume(0.3)
        #音量大小
        self._bomb = pygame.mixer.Sound("E:/图片/gunfire.mp3")

    def back(self):
        pygame.mixer.music.play(-1)
        #背景音乐，-1为循环播放

    def boost(self):
        pygame.mixer.Sound.play(self._bomb)
        #炸弹音乐


class Man:
    create = 20
    #敌机定时器
    gametime = 10
    isgame = False
    #判断游戏结束
    over = 3
    #倒计时

    def __init__(self):
        self.screen = pygame.display.set_mode((1000,750))#初始化窗口
        #self.back = self.screen.fill((250, 250, 250))
        self.title = pygame.display.set_caption('飞机大战')
        self.players = pygame.sprite.Group()
        self.enemys = pygame.sprite.Group()
        self.pb = Pumb(self.screen,True)
        self.eb = Pumb(self.screen,False)
        self.sound = Sound()

    def overtime(self):
        self.write('game over %d'%Man.over,500,500)
        Man.over -= 1
        #倒计时减去1
        if Man.over == 0:
            #倒计时停止
            pygame.time.set_timer(Man.gametime,0)
            Man.over = 3
            Man.isgame = False
            self.restart()

    def restart(self):
        Enemy.clear()
        Auto.clear()
        ma = Man()
        ma.main()

    def player(self):
        player = Auto(self.screen)
        self.players.add(player)

    def enemy(self):
        enemy = Enemy(self.screen)
        self.enemys.add(enemy)

    def write(self,t,x=0,y=0):
        #显示字
        font = pygame.font.SysFont(['方正粗黑宋简体', 'microsoftsansserif'], 50)
        text = font.render(t,True,(255,0,0),None)
        r = text.get_rect()
        r.topleft = (x,y)
        self.screen.blit(text,r)

    def main(self,*a):
        pygame.init()
        self.sound.back()
        #创建一个玩家
        self.player()
        #开启创建敌机定时器
        pygame.time.set_timer(Man.create,1000)
        while True:
            self.screen.fill(a)
            self.write('hp:100')
            if Man.isgame:
                self.write('game over %d'%Man.over,100,100)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == Man.create:
                    #创建一个敌机
                    self.enemy()
                elif e.type == Man.gametime:
                    self.overtime()
            #判断飞机间碰撞
            self.pb.draw()
            self.eb.draw()

            if self.players.sprites():
                isover = pygame.sprite.spritecollide(self.players.sprites()[0],Enemy.tope,True)
                if isover:
                    Man.isgsme = True
                    pygame.time.set_timer(Man.gametime,1000)
                    #开始游戏倒计时
                    self.pb.action(self.players.sprites()[0].rect)
                    self.players.remove(self.players.sprites()[0])
                    self.sound.boost()

            ppp = pygame.sprite.groupcollide(self.players,self.enemys,True,True)
            if ppp:
                Man.isgsme = True
                pygame.time.set_timer(Man.gametime, 1000)
                items = list(ppp.items())[0]
                x = items[0]
                y = items[1][0]
                self.pb.action(x.rect)
                self.eb.action(y.rect)
                self.sound.boost()

            #判断子弹与敌机碰撞
            isenemy = pygame.sprite.groupcollide(Auto.topb,self.enemys,True,True)
            if isenemy:
                items = list(isenemy.items())[0]
                y = items[1][0]
                self.eb.action(y.rect)
                self.sound.boost()

            self.players.update()
            self.enemys.update()
            pygame.display.update()
            time.sleep(0.1)