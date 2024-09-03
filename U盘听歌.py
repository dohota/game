import pygame
import sys
import os
import random
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((900, 550))
# 设定音乐文件所在的文件夹
music_folder = 'F:'
# 遍历文件夹，获取所有MP3文件的路径
music_files = [os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.endswith('.mp3')]
if not music_files:
    print("没有找到音乐文件！")
button_rect = pygame.Rect(200, 200, 200, 50)  # 按钮的位置和大小
button_color = (random.randint(0, 250),random.randint(0, 250),random.randint(0, 250))  # 按钮颜色

is_playing = False
running = True
while running:
    for event in pygame.event.get(): # 关闭窗口
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN: # 检查鼠标是否点击了按钮
            if button_rect.collidepoint(event.pos):
                if is_playing:
                    pygame.mixer.music.pause()
                    is_playing = False
                else:
                    pygame.mixer.music.unpause()
                    if not pygame.mixer.music.get_busy():
                        selected_music = random.choice(music_files)
                        pygame.mixer.music.load(selected_music)
                        pygame.mixer.music.play()
                        pygame.display.set_caption(selected_music)
                    is_playing = True
    screen.fill((250, 250, 250))  # 填充背景色
    pygame.draw.rect(screen, button_color, button_rect) # 绘制按钮
    # 如果音乐正在播放，在按钮上绘制文本提示
    if is_playing:
        font = pygame.font.Font(None, 36)
        text = font.render('pause', True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)
    else:
        font = pygame.font.Font(None, 36)
        text = font.render('random play', True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)
    pygame.display.flip()
    # 控制游戏帧率
    pygame.time.Clock().tick(60)
pygame.quit()
sys.exit()
