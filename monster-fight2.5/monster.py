from spirit import *
from bullets import *
#pygame.Surface.scroll()
#复制并移动 Surface 对象


class Player(Fairy):
    __slots__ = 'screen','all_bullet','ran','life','weapon','speed','rect'

    def __init__(self,screen):
        Fairy.__init__(self)
        self.screen = screen
        self.all_bullet = pygame.sprite.Group()
        self.ran = [0, 4, 0, 1, 1]
        self.life = 6
        self.weapon = 1#武器选择
        self.speed = 0.5
        self.rect = self.image.get_rect()
        self.rect.topleft = [random.randrange(Fairy.len, Fairy.SCREEN_X - Fairy.len, 80),
                             random.randrange(30, Fairy.SCREEN_Y, 20)]

    def control(self):
        super()._boundary()
        super()._move()
        # 按键控制(键盘连续监听）
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_h]:
            self.speed += 0.1

        elif key_pressed[pygame.K_q]:
            #if self.speed > 0:return
            self.image = pygame.transform.rotate(self.image, 90)
            if self.direction == 'w':
                self.direction = 'a'
            elif self.direction == 's':
                self.direction = 'd'
            elif self.direction == 'a':
                self.direction = 's'
            elif self.direction == 'd':
                self.direction = 'w'

        elif key_pressed[pygame.K_e]:
            #if self.speed > 0: return
            self.image = pygame.transform.rotate(self.image, -90)
            if self.direction == 'w':
                self.direction = 'd'
            elif self.direction == 's':
                self.direction = 'a'
            elif self.direction == 'a':
                self.direction = 'w'
            elif self.direction == 'd':
                self.direction = 's'

        elif key_pressed[pygame.K_j]:
            # 控制子弹发射的频率
            rrr = random.randint(1, 5)
            if self.weapon == 1:
                if rrr == 3:
                    b = Bullet(self.direction, self.rect)
                    self.all_bullet.add(b)
            elif self.weapon == 2:
                if rrr == 2:
                    b2 = Biao(self.direction, self.rect)
                    self.all_bullet.add(b2)

        elif key_pressed[pygame.K_LEFT]:
            self.weapon -= 1
            if self.weapon <= 1:self.weapon = 1

        elif key_pressed[pygame.K_RIGHT]:
            self.weapon += 1

        if key_pressed[pygame.K_SPACE]:
            self.speed -= 0.2
            if self.speed <= 0:self.speed = 0

    def display(self):
        super()._write('武器序号:'+str(self.weapon),20,140)
        self.screen.blit(self.image, self.rect)
        for i in self.all_bullet:
            i.move_straight_forward()
        self.all_bullet.draw(self.screen)


class Common(Fairy):
    __slots__ = 'screen','image','ran','speed','rect'

    def __init__(self,screen):
        Fairy.__init__(self)
        self.screen = screen
        self.image = pygame.image.load('E:/图片/dir-w.png')
        self.ran = [0, 4, 0]
        self.speed = random.randint(1, 5)
        self.rect = self.image.get_rect()
        self.rect.topleft = [Fairy.len+random.random() * (Fairy.SCREEN_X-Fairy.len),
                             random.random() * Fairy.SCREEN_Y]
        self.all_bullet = pygame.sprite.Group()

    def ai(self):
        super()._boundary()
        self.ran[0] += 1
        if self.ran[0] % 30 == 0:
            bb = Bullet(self.direction, self.rect)
            self.all_bullet.add(bb)
        elif self.ran[1] % 4 == 0:
            self.image = pygame.image.load('E:/图片/dir-w.png')
            self.direction = 'w'
            self.rect.top -= self.speed
            if self.ran[0] % 20 == 0:
                self.ran[1] = random.randint(4,7)
        elif self.ran[1] % 4 == 1:
            self.image = pygame.transform.rotate(pygame.image.load('E:/图片/dir-w.png'), 180)
            self.direction = 's'
            self.rect.top += self.speed
            if self.ran[0] % 20 == 0:
                self.ran[1] = random.randint(4,7)
        elif self.ran[1] % 4 == 2:
            self.image = pygame.transform.rotate(pygame.image.load('E:/图片/dir-w.png'), 90)
            self.direction = 'a'
            self.rect.left -= self.speed
            if self.ran[0] % 20 == 0:
                self.ran[1] = random.randint(4,7)
        elif self.ran[1] % 4 == 3:
            self.image = pygame.transform.rotate(pygame.image.load('E:/图片/dir-w.png'), -90)
            self.direction = 'd'
            self.rect.left += self.speed
            if self.ran[0] % 20 == 0:
                self.ran[1] = random.randint(4,7)

    def display(self):
        self.screen.blit(self.image, self.rect)
        for i in self.all_bullet:
            i.move_straight_forward()
        self.all_bullet.draw(self.screen)

