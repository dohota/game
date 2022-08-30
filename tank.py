import pygame
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
                'w': pygame.image.load('E:/图片/play-w.png'),
                's': pygame.image.load('E:/图片/play-s.png'),
                'a': pygame.image.load('E:/图片/play-a.png'),
                'd': pygame.image.load('E:/图片/play-d.png')
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
            if self.ran[2] >= 35:self.ran[2] = 35

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
        self.image = pygame.image.load('E:/图片/bullet.png')
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
        self.speed = 18
        self.distance = random.randint(300,500)

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


class Rigid(pygame.sprite.Sprite):
    def __init__(self):
        # 刚体不能与任何东西发生重合，坦克/刚体可以给刚体一个速度
        # 坦克/刚体与刚体发生碰撞，则它们之间的边缘会重合
        # 刚体可以有多个速度，遵守矢量相加的规律
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('E:/图片/0.png')
        self.rect = self.img.get_rect()
        self.rect.topleft = [random.random() * SCREEN_X,random.random() * SCREEN_Y]
        self.sp1 = [] #记录上下方向及速度，下方向为正速度
        self.sp2 = [] #记录左右方向及速度，右方向为正速度
        self.speed1 = 0
        self.speed2 = 0
        self.dir1 = ''
        self.dir2 = ''

    def pump(self,dir,speed,rect):
        #坦克碰刚体/刚体碰刚体
        if dir == 'w':
            self.rect.top = rect.top - self.rect.height
            self.sp1.append(-speed)
        elif dir == 's':
            self.rect.top = rect.top + rect.height
            self.sp1.append(speed)
        elif dir == 'a':
            self.rect.left = rect.left - self.rect.width
            self.sp2.append(-speed)
        elif dir == 'd':
            self.rect.left = rect.left + rect.width
            self.sp2.append(speed)
        self.speed1 = sum(self.sp1)
        self.speed2 = sum(self.sp2)
        if self.speed1 > 0:
            self.dir1 = 's'
        else:
            self.dir1 = 'w'
        if self.speed2 > 0:
            self.dir2 = 'd'
        else:
            self.dir2 = 'a'


class Brick(Rigid):
    def __init__(self,attack=-1,type='wool'):
        Rigid.__init__(self)
        if type == 'wool':
            #羊毛--wool：不能消失，所有坦克可以推开
            self.attack = -1
            self.img = pygame.image.load('E:/图片/6.png')
        elif type == 'stone':
            #石头--stone：可以打掉，所有坦克可以推开
            self.attack = attack
            if self.attack <= 1:self.attack = 1
            self.img = pygame.image.load('E:/图片/2.png')

    def shoot(self):
        # 子弹碰brick
        if self.attack >= 1:
            self.attack -= 1
            if self.attack == 0:
                self.kill()


class Fixed(pygame.sprite.Sprite):
    def __init__(self,attack=-1, type='hard_block'):
        pygame.sprite.Sprite.__init__(self)
        if type == 'hard_block':
            # 基岩--hard_block:不能消失，所有坦克不能推开
            self.attack = -1
            self.img = pygame.image.load('E:/图片/0.png')
        elif type == 'brick_block':
            # 砖块--brick_block：可以打掉，所有坦克不能推开
            self.attack = attack
            if self.attack <= 1:self.attack = 1
            self.img = pygame.image.load('E:/图片/1.png')
        self.rect = self.img.get_rect()
        self.rect.topleft = [random.random() * SCREEN_X, random.random() * SCREEN_Y]

    def shoot(self):
        # 子弹碰fixed(固定方块)
        if self.attack >= 1:
            self.attack -= 1
            if self.attack == 0:
                self.kill()


class Thing(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('E:/图片/h.jpg')
        self.rect = self.img.get_rect()
        self.rect.topleft = [random.random() * SCREEN_X, random.random() * SCREEN_Y]


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

    def ww(self,a,style,mm):
        for i in range(a):
            if style == 0:#横着的方块
                mm[0].rect.topleft = [random.randint(0,SCREEN_X),random.randrange(int(SCREEN_Y/4)
                                                                                  ,int(3*SCREEN_Y/4),10)]
                mm[i].rect.top = mm[i-1].rect.top
                mm[i].rect.left = mm[i-1].rect.left + 55
            elif style == 1:#竖着的方块
                mm[0].rect.topleft = [random.randrange(int(SCREEN_X/5),int(5*SCREEN_X/6),15)
                                                                    ,random.randint(0,SCREEN_Y)]
                mm[i].rect.top = mm[i - 1].rect.top + 55
                mm[i].rect.left = mm[i - 1].rect.left
            elif style == 2:#斜着的方块
                mm[0].rect.topleft = [random.randrange(int(SCREEN_X/3),int(5*SCREEN_X/6),20),
                                      random.randrange(int(SCREEN_Y/5),int(2*SCREEN_Y/5),10)]
                mm[i].rect.top = mm[i - 1].rect.top + 55
                mm[i].rect.left = mm[i - 1].rect.left + 55

    def map1(self, a, style=-1, attack=1, type='stone'):
        if type == 'wool' or type == 'stone':
            mm = [Brick(attack,type) for _ in range(a)]
            self.ww(a,style,mm)
            if type == 'wool':
                self.wool.add(mm)
            elif type == 'stone':
                self.stone.add(mm)
        else:
            nn = [Fixed(attack,type) for _ in range(a)]
            self.ww(a,style,nn)
            if type == 'hard_block':
                self.hard_block.add(nn)
            elif type == 'brick_block':
                self.brick_block.add(nn)

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