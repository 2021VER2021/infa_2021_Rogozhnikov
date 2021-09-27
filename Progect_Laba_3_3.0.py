import pygame
import random as rn
from pygame.draw import*

pygame.init()
h0 = 500
w0 = 600
FPS = 30
screen = pygame.display.set_mode((h0,w0))

red = (255, 0, 0)
green = (0, 255, 0)
d_green = (0, 130, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)
purple = (150, 30, 30)  #make thiscolor better

def apple(screen, x, y, r, color):
    circle(screen, color, (x, y), r)
def tree(screen, x, y, l, color_stvol, color_listia, levels, common):
    """
        x, y - координаты центра ствола снизу
        l - характерный размер дерева, длина ствола, основа для расчёта кроны
        color_stvol и color_listva не нуждаются в комментариях
        levels - уровни кроны
        крона рандомна, значения ширины и высоты овалов принадлежат [l, 2l] и [1.5l, 3l] соотв.
        возвращает высоту дерева h
    """
    if common:
        line(screen, color_stvol, (x, y), (x,y-l), l//4)
        ellipse(screen, color_listia, (x-l/2, y-l*1.6, l, 0.9*l), 0)
        ellipse(screen, yellow, (x-l/2-1, y-l*1.6-1, l+2, 0.9*l+2), 1)
        ellipse(screen, color_listia, (x-l, y-l*2.4, 2*l, 1.0*l), 0)
        ellipse(screen, yellow, (x-l-1, y-l*2.4-1, 2*l+2, 1.0*l+2), 1)
        ellipse(screen, color_listia, (x-l*0.6, y-3.4*l, 1.2*l, 1.6*l), 0)
        ellipse(screen, yellow, (x-l*0.6-1, y-3.4*l-1, 1.2*l+2, 1.6*l+2), 1)
    else:
        line(screen, color_stvol, (x, y), (x,y-l), l//4)
        for i in range(levels):
            Lx = rn.randint(10,20)*l//10    #maybe not //, but /
            Ly = rn.randint(15,30)*l//10
            ellipse(screen, color_listia, (x-Lx, y-l*(i+1)-Ly, 2*Lx, Ly), 0)
        h = 3*l + Ly
        return h             

def sun_pro(screen, x, y, r):
    for i in range(r,1,-1):
        circle(screen, (150+r-i, 150+r-i,255-r+i), (x, y), i)
        

def apple_tree(screen, x, y, l, color_stvol, color_listia):
    h = tree(screen, x, y, l, color_stvol, color_listia, 3, False)
    r = 10
    for i in range(4):
        apple(screen, x+rn.randint(-l+r,l-r), y-rn.randint(l+r,h-r), r, (255, 110+rn.randint(-20,20), 110+rn.randint(-20,20)))

def apple_tree_common(screen, x, y, l, color_stvol, color_listia):
    tree(screen, x, y, l, color_stvol, color_listia, 3, True)
    apple(screen, x+l/4, y-l, l/8, purple)
    apple(screen, x+l/2, y-1.9*l, l/8, purple)
    apple(screen, x-l/2, y-1.9*l, l/8, purple)
    apple(screen, x+l/4, y-l*3.0, l/8, purple)

def screen_color(screen):
    rect(screen, (150,150,255), (0, 0, h0, w0/2), 0)
    rect(screen, (50,255,100), (0, w0/2, h0, w0/2), 0)

def uni_eye(screen, x, y, r):
    circle(screen, purple, (x, y), r)
    ellipse(screen, white, (x-r/2, y-r/4, r, r/2), 0)
    circle(screen, black, (x+r/4, y), r/6)

def sun(screen, x, y, r):
    circle(screen, yellow, (x, y), r)

def uni_tail(screen, x, y, l, Left):
    if Left:
        for i in range(0,int(l),2):                 # i -- l - высота
            dx , dy = rn.randint(i//8, i//4)+l//4, l/50*(rn.randint(0,4)+2)
            ellipse(screen, (rn.randint(150,200), rn.randint(150,200), rn.randint(150,200)), (x-3*i**0.6+rn.randint(int(-2*i**0.5),int(2*i**0.5)), y-dy+i, 1.5*dx, 2*dy), 0)
    else:
        for i in range(0,int(l),2):                 # i -- l - высота
            dx , dy = -rn.randint(i//8, i//4)-l//4, l/50*(rn.randint(0,4)+2)
            ellipse(screen, (rn.randint(150,200), rn.randint(150,200), rn.randint(150,200)), (x+3*i**0.6+rn.randint(int(-2*i**0.5),int(2*i**0.5)), y-dy+i, 1.5*dx, 2*dy), 0)

def uni_body(screen, x, y, l, T):
    ellipse(screen, white, (x-abs(l), y-abs(l/2), abs(2*l), abs(l*0.8)), 0)
    line(screen, white, (x-0.8*l, y), (x-0.8*l, y+abs(l*0.8)), abs(l)//10)
    line(screen, white, (x-0.3*l, y), (x-0.3*l, y+abs(l*0.7)), abs(l)//10)
    line(screen, white, (x+0.3*l, y), (x+0.3*l, y+abs(l*0.8)), abs(l)//10)
    line(screen, white, (x+0.8*l, y), (x+0.8*l, y+abs(l*0.7)), abs(l)//10)
    line(screen, white, (x+0.78*l, y), (x+0.78*l, y-abs(l*0.8)), abs(l)//3)
    polygon(screen, red, [(x+0.80*l+l*0.08, y-abs(l*0.90)), (x+0.90*l+abs(l*0.09), y-abs(l*1.55)), (x+0.90*l+l*0.05, y-abs(l*0.90))])
    if T:
        ellipse(screen, white, (x+0.60*l, y-abs(l*0.95), abs(0.5*l), abs(0.4*l)), 0)
        ellipse(screen, white, (x+0.90*l, y-abs(l*0.82), abs(0.4*l), abs(0.2*l)), 0)
    else:
        ellipse(screen, white, (x+0.60*l-abs(0.5*l), y-abs(l*0.95), abs(0.5*l), abs(0.4*l)), 0)
        ellipse(screen, white, (x+0.90*l-abs(0.4*l), y-abs(l*0.82), abs(0.4*l), abs(0.2*l)), 0)

def unihorn_RIGHT(screen, x, y, l):
    uni_tail(screen, x-l, y-l//10, l*0.7, True)
    uni_body(screen, x, y, l, True)
    uni_eye(screen, x+0.93*l, y-l*0.78, l*0.10)
    uni_tail(screen, x+0.60*l, y-0.90*l, l*0.8, True)

def unihorn_LEFT(screen, x, y, l):
    uni_tail(screen, x-l, y-abs(l//10), -l*0.7, False)
    uni_body(screen, x, y, l, False)
    uni_eye(screen, x+0.93*l, y-abs(l*0.78), abs(l*0.10))
    uni_tail(screen, x+0.60*l, y-abs(0.90*l), -l*0.8, False)
    
    
    
screen_color(screen)
unihorn_RIGHT(screen, 240, 350, 60)
for i in range(15):
    apple_tree_common(screen, 150+rn.randint(-100,100), 300+i*20, 40+rn.randint(0,30), white, d_green) 
sun_pro(screen, h0-100, 100, 100)
unihorn_RIGHT(screen, 400, 450, 80)
unihorn_LEFT(screen, 400, 300, -60)
unihorn_LEFT(screen, 400, 550, -30)
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()

