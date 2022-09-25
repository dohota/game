from monster import *


class Rigid(Fairy):
    def __init__(self):
        # 刚体不能与任何东西发生重合，坦克/刚体可以给刚体一个速度
        # 坦克/刚体与刚体发生碰撞，则它们之间的边缘会重合
        # 刚体可以有多个速度，遵守矢量相加的规律
        Fairy.__init__(self)
        self.image = pygame.image.load('E:/图片/6.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = [Fairy.len+random.random() * (Fairy.SCREEN_X - Fairy.len),
                             random.random() * Fairy.SCREEN_Y]
        self.life = 1000
        self.sp1 = []  # 记录上下方向及速度，下方向为正速度
        self.sp2 = []  # 记录左右方向及速度，右方向为正速度
        self.speed1 = 0
        self.speed2 = 0
        self.dir1 = ''
        self.dir2 = ''

    def pump(self,dir:str,speed:float,rect):
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


Bedrock = type('Bedrock', (Fairy,), {})
Brick = type('Brick', (Fairy,), {})
Wool = type('Wool',(Rigid,),{})
Stone = type('Stone',(Rigid,),{})
Thing = type('Thing',(Fairy,),{})


# 基岩bedrock:不能消失，不能推开# 砖块brick：可以打掉，不能推开# 羊毛wool：不能消失，可以推开# 石头stone：可以打掉，可以推开
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

    def ww(self,a:int,style:int,mm):
        for i in range(a):
            if style == 0:#横着的方块
                mm[0].rect.topleft = [random.randint(Fairy.len, Fairy.SCREEN_X- Fairy.len)
                    ,random.randrange(int(Fairy.SCREEN_Y/4),int(3* Fairy.SCREEN_Y/4),10)]
                mm[i].rect.top = mm[i-1].rect.top
                mm[i].rect.left = mm[i-1].rect.left + 55
            elif style == 1:#竖着的方块
                mm[0].rect.topleft = [random.randrange(Fairy.len+int((Fairy.SCREEN_X- Fairy.len)//5),
                                                       Fairy.len+int(5*(Fairy.SCREEN_X- Fairy.len)/6),15)
                                        ,random.randint(0,4* Fairy.SCREEN_Y//5)]
                mm[i].rect.top = mm[i - 1].rect.top + 55
                mm[i].rect.left = mm[i - 1].rect.left
            elif style == 2:#斜着的方块
                mm[0].rect.topleft = [random.randrange(Fairy.len+int((Fairy.SCREEN_X-Fairy.len)//3),
                                                       Fairy.len+int(5*(Fairy.SCREEN_X-Fairy.len)/6),20),
                                      random.randrange(int(Fairy.SCREEN_Y/5),int(2*Fairy.SCREEN_Y/5),10)]
                mm[i].rect.top = mm[i - 1].rect.top + 55
                mm[i].rect.left = mm[i - 1].rect.left + 55

    def map1(self, n:int, style=-1, type='bedrock'):
        if type == 'bedrock':
            mm = [Bedrock() for _ in range(n)]
            for i in mm:
                i.image = pygame.image.load('E:/图片/0.png')
                i.rect = i.image.get_rect()
                i.rect.topleft = [Fairy.len+random.random() * (Fairy.SCREEN_X - Fairy.len),
                             random.random() * Fairy.SCREEN_Y]
                i.life = 1000
            self.ww(n, style, mm)
            self.bedrock.add(mm)
        elif type == 'brick':
            mm = [Brick() for _ in range(n)]
            for i in mm:
                i.image = pygame.image.load('E:/图片/1.png')
                i.rect = i.image.get_rect()
                i.rect.topleft = [Fairy.len+random.random() * (Fairy.SCREEN_X - Fairy.len),
                             random.random() * Fairy.SCREEN_Y]
                i.life = random.randint(1,9)
            self.ww(n, style, mm)
            self.brick.add(mm)
        elif type == 'wool':
            mm = [Wool() for _ in range(n)]
            self.ww(n, style, mm)
            self.wool.add(mm)
        elif type == 'stone':
            mm = [Stone() for _ in range(n)]
            for i in mm:
                i.image = pygame.image.load('E:/图片/2.png')
                i.rect = i.image.get_rect()
                i.rect.topleft = [Fairy.len+random.random() * (Fairy.SCREEN_X - Fairy.len),
                             random.random() * Fairy.SCREEN_Y]
                i.life = random.randint(2,7)
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
            self.screen.blit(i.image, i.rect)
        for j in self.brick:
            self.screen.blit(j.image, j.rect)
        for k in self.wool:
            self.screen.blit(k.image,k.rect)
        for l in self.stone:
            self.screen.blit(l.image,l.rect)

