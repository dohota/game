import random
from monster import *
from manager import *


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
        self.distance = [random.randint(300,500),random.randint(300,400)]

    def move_straight_forward(self):
        # 子弹离monster太远,则消失
        #超出游戏边框，也消失
        if abs(self.rect.top - self.r.top) > self.distance[0] or abs(self.rect.left - self.r.left) > self.distance[0]\
                or self.rect.left <= Page.len:
            self.kill()
        if self.direction == 'w':
            self.rect.top -= self.speed
        elif self.direction == 's':
            self.rect.top += self.speed
        elif self.direction == 'a':
            self.rect.left -= self.speed
        elif self.direction == 'd':
            self.rect.left += self.speed


class Biao(Bullet):
    def __init__(self,dir,rect):
        Bullet.__init__(self,dir,rect)
        self.image = pygame.image.load('E:/图片/bullet1.png')

    def move_straight_back(self):
        if self.direction == 'w':
            self.rect.top += self.speed
        elif self.direction == 's':
            self.rect.top -= self.speed
        elif self.direction == 'a':
            self.rect.left += self.speed
        elif self.direction == 'd':
            self.rect.left -= self.speed

    def move_straight_forward(self):
        if abs(self.rect.top - self.r.top) > self.distance[1] or abs(self.rect.left - self.r.left) > self.distance[1]:
            self.move_straight_back()
        if self.direction == 'w':
            self.rect.top -= self.speed
        elif self.direction == 's':
            self.rect.top += self.speed
        elif self.direction == 'a':
            self.rect.left -= self.speed
        elif self.direction == 'd':
            self.rect.left += self.speed

