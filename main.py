import pygame
import sys
import random
import math

pygame.init()
pygame.mixer.init()

sw = 700
sh = 500

screen = pygame.display.set_icon(pygame.image.load('icon.png'))
screen = pygame.display.set_caption('Pong')
screen = pygame.display.set_mode((sw, sh))

player_rect = pygame.Rect(50, 210, 10, 90)
opponent_rect = pygame.Rect(640, 210, 10, 90)
R, G, B = 1, 254, 100
CRR, CRG, CRB = '+', '-', '+' # CR = Color rate (gives the RGB effect)
x, y, speed, mul = 350, 250, 0.8, [random.choice([-1, 1]), random.choice([-1, 1])]
score_player, score_opponent = 0, 0
score_font = pygame.font.Font('LECO.ttf', 35)


def split_line():
    y = 12
    for i in range(10):
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(349, y, 2, 25))
        y += 50


def score():
    sp_surface = score_font.render(str(score_player), False, (255, 255, 255))
    so_surface = score_font.render(str(score_opponent), False, (255, 255, 255))
    if score_player < 10:
        screen.blit(sp_surface, (320, 10))
    elif 9 < score_player < 100:
        screen.blit(sp_surface, (299, 10))
    else:
        screen.blit(sp_surface, (280, 10))
    screen.blit(so_surface, (359, 10))


def player():
    pygame.draw.rect(screen, (255, 255, 255), player_rect)

    key = pygame.key.get_pressed()
    if key[pygame.K_UP] and player_rect.y > 0:
        player_rect.move_ip(0, -1)
        return 'up'
    if key[pygame.K_DOWN] and player_rect.y < 410:
        player_rect.move_ip(0, 1)
        return 'down'


def opponent():
    pygame.draw.rect(screen, (255, 255, 255), opponent_rect)

    if y <= opponent_rect.y + 45 and opponent_rect.y > 0:
        opponent_rect.y -= 1.9
    if y >= opponent_rect.y + 45 and opponent_rect.y < 410:
        opponent_rect.y += 1.9


def change_color(index, color, color_rate):
    if color == 255:
        color_rate = '-'
    if color == 0:
        color_rate = '+'
    if  color_rate == '+':
        color += 0.5
    else:
        color -= 0.5

    return color, color_rate


def collision():
    global x, y, speed, mul, score_opponent, score_player

    if x < -(speed ** 2) * 200:
        score_opponent += 1
        reset()
    if x > 700 + (speed ** 2) * 200:
        score_player += 1
        reset()
    if y + speed * mul[1] >= 496.5:
        pygame.mixer.music.load("sfx/wall.mp3")
        pygame.mixer.music.play()
        mul[1] *= -1
    if y + speed * mul[1] <= 3.5:
        pygame.mixer.music.load("sfx/wall.mp3")
        pygame.mixer.music.play()
        mul[1] *= -1

    if (58 <= x - 3.5 <= 60) and (player_rect.y <= y - 3.5 <= player_rect.y + 90):
        mul[0] *= -1
        pygame.mixer.music.load("sfx/hit.mp3")
        pygame.mixer.music.play()
        if speed < 1.8:
            speed += 0.2
        if player() == 'down' and mul[1] == -1:
            mul[1] = 1
        if player() == 'up' and mul[1] == 1:
            mul[1] = -1
    if (640 <= x - 3.5 <= 642) and (opponent_rect.y <= y - 3.5 <= opponent_rect.y + 90):
        mul[0] *= -1
        pygame.mixer.music.load("sfx/hit.mp3")
        pygame.mixer.music.play()
        if speed < 1.8:
            speed += 0.2

    return speed * mul[0], speed * mul[1]


def reset():
    global x, y, speed, mul

    pygame.mixer.music.load("sfx/score.mp3")
    pygame.mixer.music.play()
    x, y, speed, mul = 350, 250, 0.8, [random.choice([-1, 1]), random.choice([-1, 1])]


def ball():
    global R, G, B, CRR, CRG, CRB, x, y

    dx, dy = collision()
    x += dx
    y += dy

    R, CRR = change_color(0, R, CRR)
    G, CRG = change_color(1, G, CRG)
    B, CRB = change_color(2, B, CRB)

    pygame.draw.circle(screen, (R, G, B), (x, y), 7)


while True:
    screen.fill((0, 0, 0))

    player()
    opponent()
    split_line()
    score()
    ball()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.time.Clock().tick(300)
    pygame.display.update()
