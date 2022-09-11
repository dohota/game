from monster import *
from manager import *


class Cube(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('E:/图片/0.png')
        self.rect = self.img.get_rect()
        self.rect.topleft = [Page.len+random.random() * (Page.SCREEN_X-Page.len),
                             random.random() * Page.SCREEN_Y]


class Pump_cube(Cube):
    def __init__(self):
        # 刚体不能与任何东西发生重合，坦克/刚体可以给刚体一个速度
        # 坦克/刚体与刚体发生碰撞，则它们之间的边缘会重合
        # 刚体可以有多个速度，遵守矢量相加的规律
        Cube.__init__(self)
        self.img = pygame.image.load('E:/图片/6.png')
        self.sp1 = []  # 记录上下方向及速度，下方向为正速度
        self.sp2 = []  # 记录左右方向及速度，右方向为正速度
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


class Shoot_cube(Cube):
    def __init__(self,attack=1):
        Cube.__init__(self)
        self.img = pygame.image.load('E:/图片/1.png')
        self.attack = attack

    def shoot(self):
        # 子弹碰brick
        if self.attack >= 1:
            self.attack -= 1
            if self.attack == 0:
                self.kill()


class Stone(Pump_cube,Shoot_cube):
    def __init__(self,attack=1):
        Pump_cube.__init__(self)
        Shoot_cube.__init__(self,attack)
        self.img = pygame.image.load('E:/图片/2.png')

# 基岩bedrock:不能消失，不能推开(class Cube)
# 砖块brick：可以打掉，不能推开(class Shoot_cube)
# 羊毛wool：不能消失，可以推开(class Pump_cube)
# 石头stone：可以打掉，可以推开(class Stone)


class Thing(Cube):
    def __init__(self):
        Cube.__init__(self)
        self.img = pygame.image.load('E:/图片/h.jpg')

    def life_plus(self):
        pass


class Map:
    def __init__(self,screen):
        self.bedrock = pygame.sprite.Group()
        self.brick = pygame.sprite.Group()
        self.wool = pygame.sprite.Group()
        self.stone = pygame.sprite.Group()
        self.screen = screen

    def clear(self):
        self.bedrock.empty()
        self.brick.empty()
        self.wool.empty()
        self.stone.empty()

    def ww(self,a,style,mm):
        for i in range(a):
            if style == 0:#横着的方块
                mm[0].rect.topleft = [random.randint(Page.len,Page.SCREEN_X-Page.len)
                    ,random.randrange(int(Page.SCREEN_Y/4),int(3*Page.SCREEN_Y/4),10)]
                mm[i].rect.top = mm[i-1].rect.top
                mm[i].rect.left = mm[i-1].rect.left + 55
            elif style == 1:#竖着的方块
                mm[0].rect.topleft = [random.randrange(Page.len+int((Page.SCREEN_X-Page.len)//5),
                                                       Page.len+int(5*(Page.SCREEN_X-Page.len)/6),15)
                                        ,random.randint(0,4*Page.SCREEN_Y//5)]
                mm[i].rect.top = mm[i - 1].rect.top + 55
                mm[i].rect.left = mm[i - 1].rect.left
            elif style == 2:#斜着的方块
                mm[0].rect.topleft = [random.randrange(Page.len+int((Page.SCREEN_X-Page.len)//3),
                                                       Page.len+int(5*(Page.SCREEN_X-Page.len)/6),20),
                                      random.randrange(int(Page.SCREEN_Y/5),int(2*Page.SCREEN_Y/5),10)]
                mm[i].rect.top = mm[i - 1].rect.top + 55
                mm[i].rect.left = mm[i - 1].rect.left + 55

    def map1(self, n, style=-1, type='bedrock', attack=1):
        if type == 'bedrock':
            mm = [Cube() for _ in range(n)]
            self.ww(n, style, mm)
            self.bedrock.add(mm)
        elif type == 'brick':
            mm = [Shoot_cube(attack) for _ in range(n)]
            self.ww(n, style, mm)
            self.brick.add(mm)
        elif type == 'wool':
            mm = [Pump_cube() for _ in range(n)]
            self.ww(n, style, mm)
            self.wool.add(mm)
        elif type == 'stone':
            mm = [Stone(attack) for _ in range(n)]
            self.ww(n, style, mm)
            self.stone.add(mm)

    def display_all(self):
        # 检测墙体之间的碰撞(保证墙体不会重合，除了bedrock可以与自身重合）
        for i in self.brick:
            for j in self.brick:
                if i != j:
                    walls_pump = pygame.sprite.collide_rect(i, j)
                    if walls_pump:
                        self.brick.remove(i)
        pygame.sprite.groupcollide(self.bedrock, self.brick, False, True)
        pygame.sprite.groupcollide(self.bedrock, self.wool, False, True)
        pygame.sprite.groupcollide(self.brick, self.wool, True, True)
        pygame.sprite.groupcollide(self.stone, self.bedrock, True, False)
        pygame.sprite.groupcollide(self.stone, self.brick, True, True)
        for i in self.bedrock:
            self.screen.blit(i.img, i.rect)
        for j in self.brick:
            self.screen.blit(j.img, j.rect)
        for k in self.wool:
            self.screen.blit(k.img,k.rect)
        for l in self.stone:
            self.screen.blit(l.img,l.rect)

