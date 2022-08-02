import pygame
import sys
import time
import random

BACK = (200,200,250)
SCREEN_X = 1400
SCREEN_Y = 750


class Tank(pygame.sprite.Sprite):
    my_all_bullet = pygame.sprite.Group()
    enemy_all_bullet = pygame.sprite.Group()

    def __init__(self,screen,team=0):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.all_bullet = pygame.sprite.Group()
        if team == 0:
            self.imgs = {
                'w': pygame.image.load('E:/图片/heroW.png'),
                's': pygame.image.load('E:/图片/heroS.png'),
                'a': pygame.image.load('E:/图片/heroA.png'),
                'd': pygame.image.load('E:/图片/heroD.png')
            }
        else:
            self.imgs = {
                'w': pygame.image.load('E:/图片/eW.png'),
                's': pygame.image.load('E:/图片/eS.png'),
                'a': pygame.image.load('E:/图片/eA.png'),
                'd': pygame.image.load('E:/图片/eD.png')
            }
        self.team = team
        self.direction = 'w'
        self.img = self.imgs[self.direction]
        # tank初始化位置
        self.rect = self.img.get_rect()
        self.ran = [0, 4, 0]
        if team == 0:
            self.speed = 5
            self.rect.topleft = [random.randrange(30,SCREEN_X,80),
                                 random.randrange(30,SCREEN_Y,20)]
        else:
            self.speed = random.randint(1, 5)
            self.rect.topleft = [random.random()*SCREEN_X, random.random()*SCREEN_Y]

    def __boundary(self):
        # 地图是上下左右贯通的
        # up
        if self.rect.top <= 0-20:
            self.rect.top = SCREEN_Y + 10
        # down
        if self.rect.top >= SCREEN_Y + 20:
            self.rect.top = 0 - 20
        # left
        if self.rect.left <= 0-20:
            self.rect.left = SCREEN_X + 10
        # right
        if self.rect.left >= SCREEN_X + 20:
            self.rect.left = 0 - 20

    def control(self):
        self.__boundary()
        # 按键控制(键盘连续监听）
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w]:
            self.direction = 'w'
            self.rect.top -= self.speed + self.ran[2]
            self.ran[2] = 0
        if key_pressed[pygame.K_s]:
            self.direction = 's'
            self.rect.top += self.speed + self.ran[2]
            self.ran[2] = 0
        if key_pressed[pygame.K_a]:
            self.direction = 'a'
            self.rect.left -= self.speed+ self.ran[2]
            self.ran[2] = 0
        if key_pressed[pygame.K_d]:
            self.direction = 'd'
            self.rect.left += self.speed + self.ran[2]
            self.ran[2] = 0
        if key_pressed[pygame.K_j]:
            #控制子弹发射的频率
            rrr = random.randint(1, 5)
            if rrr == 3:
                b = Bullet(self.direction, self.rect)
                self.all_bullet.add(b)
                Tank.my_all_bullet.add(b)
        if key_pressed[pygame.K_h]:
            # 加速
            self.ran[2] += random.randint(1,10)

    def ai(self):
        self.__boundary()
        self.ran[0] += 1
        if self.ran[0] % 30 == 0:
            bb = Bullet(self.direction, self.rect)
            self.all_bullet.add(bb)
            Tank.enemy_all_bullet.add(bb)
        if self.ran[1] % 4 == 0:
            self.direction = 'w'
            self.rect.top -= self.speed
            if self.ran[0] % 20 == 0:
                self.ran[1] = random.randint(4,7)
        elif self.ran[1] % 4 == 1:
            self.direction = 's'
            self.rect.top += self.speed
            if self.ran[0] % 20 == 0:
                self.ran[1] = random.randint(4,7)
        elif self.ran[1] % 4 == 2:
            self.direction = 'a'
            self.rect.left -= self.speed
            if self.ran[0] % 20 == 0:
                self.ran[1] = random.randint(4,7)
        elif self.ran[1] % 4 == 3:
            self.direction = 'd'
            self.rect.left += self.speed
            if self.ran[0] % 20 == 0:
                self.ran[1] = random.randint(4,7)

    def display(self):
        self.img = self.imgs[self.direction]
        self.screen.blit(self.img, self.rect)
        for i in self.all_bullet:
            i.move()
        self.all_bullet.draw(self.screen)

    @classmethod
    # 清空子弹
    def clear(cls):
        cls.my_all_bullet.empty()
        cls.enemy_all_bullet.empty()


class Bullet(pygame.sprite.Sprite):
    def __init__(self,dir,rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('E:/图片/bullet4.png')
        self.direction = dir
        self.r = rect
        self.rect = self.image.get_rect()
        if self.direction == 'w':
            self.rect.left = rect.left + rect.width/2 - self.rect.width/2
            self.rect.top = rect.top - self.rect.top
        elif self.direction == 's':
            self.rect.left = rect.left + rect.width / 2 - self.rect.width / 2
            self.rect.top = rect.top + rect.height
        elif self.direction == 'a':
            self.rect.left = rect.left - rect.width / 2 - self.rect.width / 2
            self.rect.top = rect.top + rect.width/2 - self.rect.width/2
        elif self.direction == 'd':
            self.rect.left = rect.left + rect.width
            self.rect.top = rect.top + rect.width/2 - self.rect.width/2
        self.speed = 10
        self.distance = 200

    def move(self):
        # 子弹距离坦克的位置太远则会消失
        if (abs(self.rect.top - self.r.top) > self.distance
                or abs(self.rect.left - self.r.left) > self.distance):
            self.kill()
        if self.direction == 'w':
            self.rect.top -= self.speed
        elif self.direction == 's':
            self.rect.top += self.speed
        elif self.direction == 'a':
            self.rect.left -= self.speed
        elif self.direction == 'd':
            self.rect.left += self.speed


class Brick(pygame.sprite.Sprite):
    #基岩--hard_block:不能消失，所有坦克不能推开
    #砖块--brick_block：可以打掉，所有坦克不能推开
    #羊毛--wool：不能消失，所有坦克可以推开
    #石头--stone：可以打掉，所有坦克可以推开
    def __init__(self,attack=0):
        pygame.sprite.Sprite.__init__(self)
        self.attack = attack
        if 1 <= self.attack <= 5:
            self.img = pygame.image.load('E:/图片/1.png')
        elif -10 < self.attack <= 0:
            self.img = pygame.image.load('E:/图片/0.png')
        elif self.attack <= -10:
            self.img = pygame.image.load('E:/图片/6.png')
        else:
            self.img = pygame.image.load('E:/图片/2.png')
        self.rect = self.img.get_rect()
        self.rect.topleft = [random.random() * SCREEN_X,random.random() * SCREEN_Y]


class Map:
    def __init__(self,screen):
        self.brick_block = pygame.sprite.Group()
        self.hard_block = pygame.sprite.Group()
        self.wool = pygame.sprite.Group()
        self.stone = pygame.sprite.Group()
        self.screen = screen

    def clear(self):
        self.hard_block.empty()
        self.brick_block.empty()
        self.wool.empty()
        self.stone.empty()

    def map_total(self):
        self.map1(4,2)
        self.map1(8,0)

    def map1(self, a,style=-1):
        mm = [Brick() for _ in range(a)]
        for i in range(a):
            if style == 0:#横着的方块
                mm[0].rect.topleft = [10,random.randrange(int(SCREEN_Y/4),
                                                          int(3*SCREEN_Y/4),10)]
                mm[i].rect.top = mm[i-1].rect.top
                mm[i].rect.left = mm[i-1].rect.left + 55
            elif style == 1:#竖着的方块
                mm[0].rect.topleft = [random.randrange(int(SCREEN_X/5),
                                                       int(5*SCREEN_X/6),15),10]
                mm[i].rect.top = mm[i - 1].rect.top + 55
                mm[i].rect.left = mm[i - 1].rect.left
            elif style == 2:#斜着的方块
                mm[0].rect.topleft = [random.randrange(int(SCREEN_X/3),
                                                       int(5*SCREEN_X/6),20),
                                      random.randrange(int(SCREEN_Y/5),
                                                       int(2*SCREEN_Y/5),10)]
                mm[i].rect.top = mm[i - 1].rect.top + 55
                mm[i].rect.left = mm[i - 1].rect.left + 55
        self.hard_block.add(mm)

    def map2(self,a=1):
        mm = [Brick(3) for _ in range(a)]
        self.brick_block.add(mm)

    def map3(self,a=1):
        mm = [Brick(-20) for _ in range(a)]
        self.wool.add(mm)

    def map4(self,a=1):
        mm = [Brick(6) for _ in range(a)]
        self.stone.add(mm)

    def display_all(self):
        for i in self.hard_block:
            self.screen.blit(i.img, i.rect)
        for j in self.brick_block:
            self.screen.blit(j.img, j.rect)
        for k in self.wool:
            self.screen.blit(k.img,k.rect)
        for l in self.stone:
            self.screen.blit(l.img,l.rect)


class Sound:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load("E:/图片/back.mp3")
        pygame.mixer.music.set_volume(0.3)
        # 音量大小
        self.__bomb = pygame.mixer.Sound("E:/图片/gunfire.mp3")
        self.__horry = pygame.mixer.Sound("E:/图片/oo.mp3")
        self.__hit = pygame.mixer.Sound("E:/图片/hit.mp3")

    def back(self):
        pygame.mixer.music.play(-1)
        # 背景音乐，-1为循环播放

    def boost(self):
        pygame.mixer.Sound.play(self.__bomb)

    def horry(self):
        pygame.mixer.Sound.play(self.__horry)

    def hit(self):
        pygame.mixer.Sound.play(self.__hit)


class Manager:
    #计时器的id（id是什么数字不重要）,好像id值不能重复
    id = 0
    id2 = 1
    #计算一局游戏的得分，打掉1个坦克得1分
    score = 0
    #计算一局游戏的存活时间，单位为秒
    timer = 0
    #计算游戏是第几局/回合
    j = 1

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_X,SCREEN_Y))
        self.players = pygame.sprite.Group()
        self.enemys = pygame.sprite.Group()
        self.maps = Map(self.screen)
        self.sound = Sound()
        self.ran = [random.random()*10]

    def player(self):
        #生成1辆我方坦克
        p = Tank(self.screen)
        self.players.add(p)

    def enemy(self,x=1):
        #生成x辆敌方坦克
        e = [Tank(self.screen, 1) for _ in range(x)]
        self.enemys.add(e)

    def restart(self):
        Manager.j += 1
        Manager.timer,Manager.score = 0, 0
        self.sound.horry()
        Tank.clear()#清除子弹
        self.players.empty()#清除我方坦克
        self.enemys.empty()#清除敌方坦克
        self.maps.clear()#清除砖块
        mm = Manager()
        mm.main()

    def get(self):
        self.title = pygame.display.set_caption('坦克大战:'+str(Manager.score)+'分数'+
                        '这局开始了'+str(Manager.timer)+'秒  这是第'+str(Manager.j)+'局')

    def pull_wall(self,a,b):
        for i in a:
            for j in b:
                if j.direction == 'w':
                    i.rect.top -= j.speed
                elif j.direction == 's':
                    i.rect.top += j.speed
                elif j.direction == 'a':
                    i.rect.left -= j.speed
                elif j.direction == 'd':
                    i.rect.left += j.speed

    def wall_pump(self,a):
        for i in a:
            for j in a:
                if i != j:
                    walls_pump = pygame.sprite.collide_rect(i, j)
                    if walls_pump:
                        a.remove(i)

    def attack_wall(self,a,b):
        self.sound.hit()
        for k in a.keys():
            k.attack -= 1
            if k.attack == 0:
                b.remove(k)

    def start(self):
        pygame.init()
        self.sound.back()
        self.player()
        self.maps.map_total()
        pygame.time.set_timer(Manager.id,random.randrange(3500,8500,100))
        pygame.time.set_timer(Manager.id2, 1000)
        while True:
            self.screen.fill(BACK)
            for i in self.players:
                i.control()
                i.display()
            for j in self.enemys:
                j.ai()
                j.display()
            self.maps.display_all()
            time.sleep(0.1)#防止坦克跑得太快
            pygame.display.update()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == Manager.id:
                    self.enemy()
                    self.maps.map4(2)
                elif e.type == Manager.id2:
                    Manager.timer += 1
                    self.get()
            #我方坦克与敌方坦克的碰撞
            tanks_pump = pygame.sprite.groupcollide(self.players, self.enemys, True, True)
            # 敌方子弹打玩家坦克
            e_hit_i = pygame.sprite.groupcollide(self.players, Tank.enemy_all_bullet,
                                                     True, True)

            # 我方坦克撞墙
            i_hit_wall = pygame.sprite.groupcollide(self.maps.hard_block, self.players,
                                                    False, True)
            i_hit_brick = pygame.sprite.groupcollide(self.maps.brick_block, self.players,
                                                     True, True)
            if tanks_pump or e_hit_i or i_hit_wall or i_hit_brick:
                self.sound.boost()
                self.restart()
            # 敌方坦克撞墙
            e_hit_wall = pygame.sprite.groupcollide(self.maps.hard_block,
                                                        self.enemys, False, True)
            e_hit_brick = pygame.sprite.groupcollide(self.maps.brick_block,
                                                         self.enemys, True, True)
            if e_hit_wall or e_hit_brick:
                self.sound.boost()
            #玩家子弹打敌方坦克
            i_hit_e = pygame.sprite.groupcollide(Tank.my_all_bullet, self.enemys,
                                                 True, True)
            if i_hit_e:
                Manager.score += 1
                self.sound.boost()

            #我方子弹碰到敌方子弹
            bullet_pump = pygame.sprite.groupcollide(Tank.my_all_bullet,Tank.enemy_all_bullet,
                                                     True,True)
            if bullet_pump:
                self.sound.hit()

            #我方坦克推墙
            i_hit_wool = pygame.sprite.groupcollide(self.maps.wool,self.players,False,False)
            if i_hit_wool:
                self.pull_wall(i_hit_wool.keys(),self.players.sprites())
            i_hit_stone = pygame.sprite.groupcollide(self.maps.stone,self.players,False,False)
            if i_hit_stone:
                self.pull_wall(i_hit_stone.keys(),self.players.sprites())
            #敌方坦克推墙
            e_hit_wool = pygame.sprite.groupcollide(self.maps.wool,self.enemys,False,False)
            if e_hit_wool:
                self.pull_wall(e_hit_wool.keys(),self.enemys.sprites())
            e_hit_stone = pygame.sprite.groupcollide(self.maps.stone,self.enemys,False,False)
            if e_hit_stone:
                self.pull_wall(e_hit_stone.keys(),self.enemys.sprites())
            #我方子弹撞墙
            i_bullet_wall = pygame.sprite.groupcollide(self.maps.hard_block,
                                                       Tank.my_all_bullet,
                                                       False, True)
            i_bullet_wool = pygame.sprite.groupcollide(self.maps.wool,Tank.my_all_bullet
                                                       ,False,True)
            if i_bullet_wall or i_bullet_wool:
                self.sound.hit()
            i_bullet_brick = pygame.sprite.groupcollide(self.maps.brick_block,
                                                        Tank.my_all_bullet,
                                                        False,True)
            i_bullet_stone = pygame.sprite.groupcollide(self.maps.stone,Tank.my_all_bullet,
                                                        False,True)
            if i_bullet_brick:
                self.attack_wall(i_bullet_brick,self.maps.brick_block)
            if i_bullet_stone:
                self.attack_wall(i_bullet_stone, self.maps.stone)
            #敌方子弹撞墙
            e_bullet_wall = pygame.sprite.groupcollide(self.maps.hard_block,
                                                       Tank.enemy_all_bullet, False, True)
            e_bullet_wool = pygame.sprite.groupcollide(self.maps.wool,Tank.enemy_all_bullet
                                                       ,False,True)
            if e_bullet_wall or e_bullet_wool:
                self.sound.hit()
            e_bullet_brick = pygame.sprite.groupcollide(self.maps.brick_block,
                                                        Tank.enemy_all_bullet,False, True)
            e_bullet_stone = pygame.sprite.groupcollide(self.maps.stone,Tank.enemy_all_bullet
                                                        , False, True)
            if e_bullet_stone:
                self.attack_wall(e_bullet_brick, self.maps.stone)
            if e_bullet_brick:
                self.attack_wall(e_bullet_stone,self.maps.brick_block)
            #检测墙体之间的碰撞(保证墙体不会重合）
            self.wall_pump(self.maps.hard_block)
            self.wall_pump(self.maps.brick_block)
            self.wall_pump(self.maps.stone)
            pygame.sprite.groupcollide(self.maps.hard_block,self.maps.brick_block, False, True)
            pygame.sprite.groupcollide(self.maps.hard_block, self.maps.wool, False, True)
            pygame.sprite.groupcollide(self.maps.brick_block, self.maps.wool, True, True)
            pygame.sprite.groupcollide(self.maps.stone,self.maps.hard_block, True, False)
            pygame.sprite.groupcollide(self.maps.stone,self.maps.brick_block, True, True)
            pygame.sprite.groupcollide(self.maps.stone,self.maps.wool, False, True)


m = Manager()
m.start()
