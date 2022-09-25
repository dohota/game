import pygame


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
