import pygame
import random
from bullets import *
#pygame.Surface.scroll()
#复制并移动 Surface 对象


class Monster(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.all_bullet = pygame.sprite.Group()
        self.imgs = {
            'w': pygame.image.load('E:/图片/player-w.png'),
            's': pygame.transform.rotate(pygame.image.load('E:/图片/player-w.png'), 180),
            'a': pygame.transform.rotate(pygame.image.load('E:/图片/player-w.png'),90),
            'd': pygame.transform.rotate(pygame.image.load('E:/图片/player-w.png'),-90)
        }
        self.direction = 'w'
        self.img = self.imgs[self.direction]
        self.rect = self.img.get_rect()

    def boundary(self):
        # 地图是上下左右贯通的
        # up
        if self.rect.top <= 0-20:
            self.rect.top = Page.SCREEN_Y + 10
        # down
        if self.rect.top >= Page.SCREEN_Y + 20:
            self.rect.top = 0 - 20
        # left
        if self.rect.left <= Page.len-20:
            self.rect.left = Page.SCREEN_X + 10
        # right
        if self.rect.left >= Page.SCREEN_X + 20:
            self.rect.left = Page.len - 20


class Player(Monster):
    def __init__(self,screen):
        Monster.__init__(self,screen)
        self.ran = [0, 4, 0,1,1]
        self.show = False
        self.dang = 'empty'#挡位
        self.weapon = 1#武器选择
        self.speed = 0
        self.rect.topleft = [random.randrange(Page.len, Page.SCREEN_X-Page.len, 80),
                             random.randrange(30, Page.SCREEN_Y, 20)]

    def move(self):
        if self.direction == 'w':
            self.rect.top -= self.speed
        elif self.direction == 's':
            self.rect.top += self.speed
        elif self.direction == 'a':
            self.rect.left -= self.speed
        elif self.direction == 'd':
            self.rect.left += self.speed

    def write(self,t,x,y):
        font = pygame.font.SysFont('arial',30)
        text = font.render(t, True, (255, 0, 0), None)
        r = text.get_rect()
        r.topleft = (x, y)
        self.screen.blit(text, r)

    def control(self):
        super().boundary()
        # 按键控制(键盘连续监听）
        press = pygame.key.get_pressed()
        if press[pygame.K_BACKSPACE]:
            if not self.show: self.show = True#显示

        elif press[pygame.K_RETURN]:#需要挂空挡
            if self.show and self.dang == 'empty': self.show = False#消失

        if self.show:
            if press[pygame.K_UP] and self.speed == 0:
                        if self.dang == 'empty':#空挡
                            self.dang = 'empty'
                        elif self.dang == 'back':#后退
                            self.dang = 'empty'
                        elif self.dang == 'attack1':#攻击
                            self.dang = 'back'
                        elif self.dang == 'forward1':#前进
                            self.dang = 'attack1'
                        elif self.dang == 'turn':#转弯档
                            self.dang = 'forward1'

            elif press[pygame.K_DOWN] and self.speed == 0:
                    if self.dang == 'empty':
                        self.dang = 'back'
                    elif self.dang == 'back':
                        self.dang = 'attack1'
                    elif self.dang == 'attack1':
                        self.dang = 'forward1'
                    elif self.dang == 'forward1':
                        self.dang = 'turn'
                    elif self.dang == 'turn':
                        self.dang = 'turn'

            elif press[pygame.K_LEFT]:
                if self.dang == 'forward1':return#不能低于第一档
                if self.dang == 'forward' + str(self.ran[3]):
                    if (self.dang == 'forward2' and self.speed <= 1) or (self.dang == 'forward3' and self.speed <= 4):
                        #要低到一定速度才能减档
                        self.ran[3] -= 1
                        self.dang = 'forward' + str(self.ran[3])
                elif self.dang == 'attack' + str(self.ran[4]):
                    self.ran[4] -= 1
                    self.dang = 'attack' + str(self.ran[4])
                    self.weapon = self.ran[4]

            elif press[pygame.K_RIGHT]:
                if self.dang == 'forward'+str(self.ran[3]):
                    if self.dang == 'forward3':return#不能超过第三档
                    self.ran[3] += 1
                    self.dang = 'forward'+str(self.ran[3])
                elif self.dang == 'attack'+str(self.ran[4]):
                    self.ran[4] += 1
                    self.dang = 'attack'+str(self.ran[4])
                    self.weapon = self.ran[4]

            if self.dang == 'forward1':
                if self.speed < 0: self.speed = 0
                if self.speed > 1: self.speed = 1
                self.move()
                if press[pygame.K_SPACE]:
                    self.speed -= 0.1
                elif press[pygame.K_h]:
                    self.speed += 0.2

            elif self.dang == 'forward2':
                if self.speed > 4: self.speed = 4
                if self.speed > 1:#要达到一定速度才能减档
                    self.move()
                    if press[pygame.K_SPACE]:
                        self.speed -= 0.2
                    elif press[pygame.K_h]:
                        self.speed += 0.35

            elif self.dang == 'forward3':
                if self.speed > 4:
                    self.move()
                    if press[pygame.K_SPACE]:
                        self.speed -= 0.3
                    elif press[pygame.K_h]:
                        self.speed += 0.5

            elif self.dang == 'back':
                if self.speed > 0: self.speed = 0
                self.move()
                if press[pygame.K_SPACE]:
                    self.speed += 0.2
                elif press[pygame.K_h]:
                    self.speed -= 0.1

            elif self.dang == 'attack1':
                if press[pygame.K_j]:
                        rrr = random.randint(1, 5)# 控制子弹发射的频率
                        if rrr == 3:
                            b = Bullet(self.direction, self.rect)
                            self.all_bullet.add(b)

            elif self.dang == 'attack2':
                if press[pygame.K_j]:
                        rrr = random.randint(1, 5)
                        if rrr == 2:
                            b = Biao(self.direction, self.rect)
                            self.all_bullet.add(b)

            elif self.dang == 'turn':
                rrr = random.randint(1,7)
                if press[pygame.K_q]:#左转
                    if rrr == 3:
                        if self.direction == 'w':
                            self.direction = 'a'
                        elif self.direction == 's':
                            self.direction = 'd'
                        elif self.direction == 'a':
                            self.direction = 's'
                        elif self.direction == 'd':
                            self.direction = 'w'
                elif press[pygame.K_e]:#右转
                    if rrr == 4:
                        if self.direction == 'w':
                            self.direction = 'd'
                        elif self.direction == 's':
                            self.direction = 'a'
                        elif self.direction == 'a':
                            self.direction = 'w'
                        elif self.direction == 'd':
                            self.direction = 's'

    def display(self):
        self.write('player:'+str(self.dang),20,140)
        if self.show:
            self.img = self.imgs[self.direction]
            self.screen.blit(self.img, self.rect)
            for i in self.all_bullet:
                i.move_straight_forward()
            self.all_bullet.draw(self.screen)


class Common(Monster):
    def __init__(self,screen):
        Monster.__init__(self, screen)
        self.imgs = {
            'w': pygame.image.load('E:/图片/dir-w.png'),
            's': pygame.image.load('E:/图片/dir-s.png'),
            'a': pygame.image.load('E:/图片/dir-a.png'),
            'd': pygame.image.load('E:/图片/dir-d.png')
        }
        self.ran = [0, 4, 0]
        self.speed = random.randint(1, 5)
        self.rect.topleft = [Page.len+random.random() * (Page.SCREEN_X-Page.len), random.random() * Page.SCREEN_Y]

    def ai(self):
        super().boundary()
        self.ran[0] += 1
        if self.ran[0] % 30 == 0:
            bb = Bullet(self.direction, self.rect)
            self.all_bullet.add(bb)
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
            i.move_straight_forward()
        self.all_bullet.draw(self.screen)

