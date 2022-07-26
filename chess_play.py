import pygame
import sys
WHITE = (255,255,255)
BLACK = (0,0,0)
BACKCOLOR = (100,180,250)

BOARDLINE = 10
#x行x列
BOUNDARY = 50
#棋盘到游戏界面边界的距离
CHESSLEN = 50
#棋盘里每一棋格的大小
CHESS_R = 20

SCREEN = BOARDLINE*CHESSLEN+2*BOUNDARY


class Manager:
    def __init__(self):
        self.IMG = pygame.image.load('E:/图片/chessboard.jpg')
        self.IMG = pygame.transform.scale(self.IMG,(CHESSLEN,CHESSLEN))

        self.screen = pygame.display.set_mode((SCREEN,SCREEN))
        self.title = pygame.display.set_caption('五子棋')
        self.isblack = True
        self.boardcount = [[0 for i in range(BOARDLINE)] for i in range(BOARDLINE)]

        self.s = Sound()

    def mii(self,row,col):
        return(BOUNDARY+col*CHESSLEN,BOUNDARY+row*CHESSLEN)

    def draw(self):
        for i in range(BOARDLINE):
            for j in range(BOARDLINE):
                screenpos = self.mii(i,j)
                self.screen.blit(self.IMG,screenpos)

    def inarea(self,pos):
        return BOUNDARY <= pos[0] <= SCREEN-BOUNDARY and BOUNDARY <= pos[1] <= SCREEN-BOUNDARY

    def iim(self,pos):
        x = (pos[0]-BOUNDARY)//CHESSLEN
        y = (pos[1]-BOUNDARY)//CHESSLEN
        return (x,y)

    def makemove(self,pos):
        if self.boardcount[pos[1]][pos[0]] == 0:
            self.boardcount[pos[1]][pos[0]] = 1 if self.isblack else -1
            return True
        return False

    def draw2(self):
        for row in range(len(self.boardcount)):
            for col in range(len(self.boardcount[row])):
                spos = self.mii(row,col)
                screenpos = (spos[0]+CHESSLEN/2,spos[1]+CHESSLEN/2)
                if self.boardcount[row][col] == 1:
                    pygame.draw.circle(self.screen,BLACK,screenpos,CHESS_R)
                if self.boardcount[row][col] == -1:
                    pygame.draw.circle(self.screen,WHITE,screenpos,CHESS_R)

    def winner(self,a,m2):
        if self.heng(m2) or self.shu(m2) or self.xie(m2):
            return 1 if a else -1
        return 0

    def heng(self,m):
        x = m[0]
        row = self.boardcount[m[1]]
        left_start = max(0,x-4)
        left_end = x
        for i in range(left_start,left_end+1):
            if abs(sum(row[i:i+5])) == 5:
                return True
        return False

    def shu(self,m):
        y = m[0]
        col = self.boardcount[m[0]]
        top_start = max(0, y - 4)
        top_end = y
        for i in range(top_start, top_end + 1):
            if abs(sum(col[i:i + 5])) == 5:
                return True
        return False

    def xie(self,m):
        x,y = m[0],m[1]
        all = []
        for i in range(-4,5):
            if 0 <= x+i < BOARDLINE and 0 <= y+i < BOARDLINE:
                all.append(self.boardcount[y+i][x+i])
        roll = self.roll_sum(all,5)
        if 5 in roll:
            return True

        all = []
        for i in range(-4, 5):
            if 0 <= x + i < BOARDLINE and 0 <= y - i < BOARDLINE:
                all.append(self.boardcount[y - i][x + i])
        roll = self.roll_sum(all, 5)
        if 5 in roll:
            return True
        return False

    def roll_sum(self,values,size):
        r = []
        for i in range(len(values)-size+1):
            r.append(abs(sum(values[i:i+size])))
        return r

    def end(self,a):
        self.draw2()
        font = pygame.font.SysFont(['方正粗黑宋简体', 'microsoftsansserif'], 50)
        winner = '黑棋' if a else '白棋'
        text = font.render(winner+'获胜了',True,BLACK,None)
        self.screen.blit(text,(0,0))
        pygame.display.flip()

    def main(self,x):
        self.s.back(x)
        while True:
            pygame.init()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.MOUSEBUTTONUP:
                    clickpos = pygame.mouse.get_pos()#获取鼠标位置
                    if self.inarea(clickpos):
                        #self.s.chess_down()
                        mmp = self.iim(clickpos)
                        self.isblack = not self.isblack if self.makemove(mmp) else self.isblack
                        if self.winner(self.isblack,mmp):
                            self.end(not self.isblack)
                            self.isblack = True
                            self.boardcount = [[0 for i in range(BOARDLINE)] for i in range(BOARDLINE)]
            self.screen.fill(BACKCOLOR)
            self.draw()
            self.draw2()
            pygame.display.flip()


class Sound:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load("E:/图片/back.mp3")
        self._bomb = pygame.mixer.Sound("E:/图片/walk.mp3")

    def back(self,x=0.3,y=-1):
        pygame.mixer.music.set_volume(x)
        #音量大小
        pygame.mixer.music.play(y)
        #背景音乐，-1为循环播放

    def chess_down(self):
        pygame.mixer.Sound.play(self._bomb)



