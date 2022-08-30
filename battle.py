import sys
import time
from tank import *


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
        self.rann = ['hard_block','brick_block','wool','stone']
        # 己方坦克有几条命
        self.life = 6

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
        mmmm = Manager()
        mmmm.main()

    def write(self, t, x, y):
        font = pygame.font.SysFont(['方正粗黑宋简体', 'microsoftsansserif'], 40)
        text = font.render(t, True, (255, 0, 0), None)
        r = text.get_rect()
        r.topleft = (x, y)
        self.screen.blit(text, r)

    def main(self):
        pygame.init()
        self.sound.back()
        pygame.display.set_caption("坦克大战--开始界面")
        self.screen.fill((150, 250, 200))
        self.write("1p", 280, 50)
        self.write("2p", 280, 150)
        while True:
            pygame.display.update()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.MOUSEBUTTONUP:
                    click = pygame.mouse.get_pos()  # 获取鼠标位置
                    if 240 <= click[0] <= 320 and 20 <= click[1] <= 80:
                        self.start()
                        #mmm = Manager()
                        #mmm.start()

    def minus_life(self,x=1):
        self.sound.boost()
        self.life -= x
        if self.life <= 0:
            self.restart()

    def start(self):
        self.sound.back()
        self.player()
        self.maps.map1(random.randint(2,10),random.randint(0,2),-1,'hard_block')
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
            time.sleep(0.07)#防止坦克跑得太快
            pygame.display.update()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == Manager.id:
                    self.enemy()
                    self.maps.map1(2,-1,random.randint(1,9),self.rann[random.randint(0,3)])
                elif e.type == Manager.id2:
                    Manager.timer += 1
                    pygame.display.set_caption \
                    ('这是第'+ str(Manager.j)+'局,开局'+str(Manager.timer)+'秒,'
                     +str(Manager.score)+'杀,生命值'+str(self.life))

            #我方坦克与敌方坦克碰撞
            tanks_pump = pygame.sprite.groupcollide(self.players, self.enemys, False, True)
            if tanks_pump:self.minus_life(3)
            # 子弹打坦克
            e_hit_i = pygame.sprite.groupcollide(self.players, Tank.enemy_all_bullet,False, True)
            if e_hit_i:self.minus_life(1)
            i_hit_e = pygame.sprite.groupcollide(Tank.my_all_bullet, self.enemys, True, True)
            if i_hit_e:
                Manager.score += 1
                self.sound.boost()
            # 坦克撞墙
            i_hit_wall = pygame.sprite.groupcollide(self.maps.hard_block, self.players,False, False)
            i_hit_brick = pygame.sprite.groupcollide(self.maps.brick_block, self.players,True, False)
            e_hit_wall = pygame.sprite.groupcollide(self.maps.hard_block, self.enemys, False, True)
            e_hit_brick = pygame.sprite.groupcollide(self.maps.brick_block, self.enemys, True, True)
            if i_hit_wall:self.minus_life(4)
            if i_hit_brick:self.minus_life(2)
            if e_hit_wall or e_hit_brick:self.sound.boost()
            #我方子弹碰到敌方子弹
            bullet_pump = pygame.sprite.groupcollide(Tank.my_all_bullet,Tank.enemy_all_bullet,True,True)
            if bullet_pump:self.sound.hit()
            #坦克推墙
            i_hit_wool = pygame.sprite.groupcollide(self.maps.wool,self.players,False,False)
            i_hit_stone = pygame.sprite.groupcollide(self.maps.stone, self.players, False, False)
            e_hit_wool = pygame.sprite.groupcollide(self.maps.wool, self.enemys,False, False)
            e_hit_stone = pygame.sprite.groupcollide(self.maps.stone, self.enemys,False, False)
            if i_hit_wool or i_hit_stone or e_hit_wool or e_hit_stone:
                for i in i_hit_wool.keys():
                    for ii in list(i_hit_wool.values())[0]:
                        i.pump(ii.direction,ii.speed,ii.rect)
                for j in i_hit_stone.keys():
                    for jj in list(i_hit_stone.values())[0]:
                        j.pump(jj.direction,jj.speed,jj.rect)
                for k in e_hit_wool.keys():
                    for kk in list(e_hit_wool.values()):
                        for kkk in kk:
                            k.pump(kkk.direction,kkk.speed,kkk.rect)
                for l in e_hit_stone.keys():
                    for ll in list(e_hit_stone.values()):
                        for lll in ll:
                            l.pump(lll.direction,lll.speed,lll.rect)
            #墙推墙
            for i in list(self.maps.stone)+list(self.maps.wool):
                for j in list(self.maps.stone)+list(self.maps.wool):
                    if i != j:
                        p = pygame.sprite.collide_rect(i, j)
                        if p:i.pump(j.dir2, j.speed2, j.rect)
            #子弹撞墙
            i_bullet_wall = pygame.sprite.groupcollide(self.maps.hard_block,Tank.my_all_bullet,False, True)
            i_bullet_wool = pygame.sprite.groupcollide(self.maps.wool,Tank.my_all_bullet,False,True)
            i_bullet_brick = pygame.sprite.groupcollide(self.maps.brick_block, Tank.my_all_bullet, False, True)
            i_bullet_stone = pygame.sprite.groupcollide(self.maps.stone, Tank.my_all_bullet, False, True)
            e_bullet_wall = pygame.sprite.groupcollide(self.maps.hard_block, Tank.enemy_all_bullet, False, True)
            e_bullet_wool = pygame.sprite.groupcollide(self.maps.wool, Tank.enemy_all_bullet, False, True)
            e_bullet_brick = pygame.sprite.groupcollide(self.maps.brick_block, Tank.enemy_all_bullet, False, True)
            e_bullet_stone = pygame.sprite.groupcollide(self.maps.stone, Tank.enemy_all_bullet, False, True)
            if i_bullet_wall or i_bullet_wool or e_bullet_wall or e_bullet_wool:self.sound.hit()
            if i_bullet_stone or i_bullet_brick or e_bullet_brick or e_bullet_stone:
                self.sound.hit()
                for i in i_bullet_stone.keys():
                    i.shoot()
                for j in i_bullet_brick.keys():
                    j.shoot()
                for k in e_bullet_brick.keys():
                    k.shoot()
                for l in e_bullet_stone.keys():
                    l.shoot()
            #检测墙体之间的碰撞(保证墙体不会重合，除了hard_block可以与自身重合）
            for i in self.maps.brick_block:
                for j in self.maps.brick_block:
                    if i != j:
                        walls_pump = pygame.sprite.collide_rect(i, j)
                        if walls_pump:self.maps.brick_block.remove(i)
            pygame.sprite.groupcollide(self.maps.hard_block,self.maps.brick_block,False, True)
            pygame.sprite.groupcollide(self.maps.hard_block, self.maps.wool, False, True)
            pygame.sprite.groupcollide(self.maps.brick_block, self.maps.wool, True, True)
            pygame.sprite.groupcollide(self.maps.stone,self.maps.hard_block, True, False)
            pygame.sprite.groupcollide(self.maps.stone,self.maps.brick_block, True, True)


if __name__ == '__main__':
    m = Manager()
    m.main()
