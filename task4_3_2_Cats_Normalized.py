import pygame
import numpy as np
from pygame.draw import *

pygame.init()
FPS = 30
screen = pygame.display.set_mode((1000, 600))   
screen.fill((255, 255, 255))

lite_brown = (184, 134, 11)
dark_brown = (128, 128, 0)
black = (0, 0, 0)
grey = (128, 128, 128)
green_window = (0, 250, 154)

shirina = 1000
height = 600

def fon(x, y, color_up, color_bottom):
  '''
      Функция, заливающая фон двумя цветами,
      разделение горизонтальной полосой посередине
      Входные данные:
      x, y - координаты верхнего левого угла экрана, обычно (0, 0), float or int
      color_up - цвет верхней части фона, list (a1, a2, a3) in RGB
      color_down - цвет нижней части фона, list (a1, a2, a3) in RGB
      Возвращает None
  '''
  rect(screen, color_up, (x, y, shirina, height//2))
  rect(screen, color_bottom, (x, (y + height//2), shirina, (height//2)))
  
def klubok(x, y, r):
  '''
      Функция рисующая клубок ниток
      Входные данные:
      x, y - числа, координаты центра клубка, float or int
      r - радиус клубка, float or int
      Выводит None
  '''
  circle(screen, grey, (x, y), r)
  circle(screen, black, (x, y), r, 1)
  arc(screen, black, (x-r, y-r, 4*r, 4*r), 19/32*np.pi, 29*np.pi/32)
  arc(screen, black, (x-r, y-r/2, 4*r, 4*r), 17/32*np.pi, 55*np.pi/64)
  arc(screen, black, (x-r, y, 4*r, 4*r), 4*np.pi/8, 13*np.pi/16)
	
def okno(x, y):
  '''
     Функция, рисующая окно
     Цвет рамы - коричневый, с чёрным контуром ширины 1
     Цвет внутренностей окна - window_outside
     Input:
     x, y - coordinates of the left up edge of the window (in float or int)
     Output:
     None
  '''
  window_outside = (99, 66, 33)
  rect(screen, window_outside, (x, y, 180, 220))
  rect(screen, black, (x, y, 180, 220), 1)
  for i in [20, 100]:
    for j in [20, 120]:
      rect(screen, green_window, (x+i, y+j, 60, 80))
      rect(screen, black, (x+i, y+j, 60, 80), 1)

def cat(screen, x, y, k, color):
  '''
     This function draw a cat
     Input:
     screen - pygame.Surface type
     x, y - coordinates of left point of cat's head
     k - parameter, that changes the length of cat
     color - the general color of the cat
     Output:
     None
  '''
  x+=-k*10   #провести рефакторинг, заменить все x, y на x - 10*k, y + 40*k
  y+=k*40
  surf = pygame.Surface((int(k*20), int(k*57)))
  surf.fill((255, 255, 255))
  surf.set_colorkey((255, 255, 255))
  bigger = pygame.Rect(0, 0, k*20, k*57)
  ellipse(surf, color, bigger)
  ellipse(surf, (0, 0, 0), bigger, 1)
  rotatedSurf = pygame.transform.rotate(surf, 75)
  screen.blit(rotatedSurf, (x+k*120, y-k*45))
  
  ellipse(screen, color, (x+k*40, y-k*60, k*90, k*50)) #тело
  ellipse(screen, (0, 0, 0), (x+k*40, y-k*60, k*90, k*50), 1)
  
  circle(screen, color, (x+k*30, y-k*40), k*20) #голова
  circle(screen, (0, 0, 0), (x+k*30, y-k*40), k*20, 1)
	
  ellipse(screen, color, (x+k*40, y-k*23, k*28, k*15)) #нога 2
  ellipse(screen, (0, 0, 0), (x+k*40, y-k*23, k*28, k*15), 1)
	
  ellipse(screen, color, (x+k*100, y-k*23, k*28, k*15)) #нога 1
  ellipse(screen, (0, 0, 0), (x+k*100, y-k*23, k*28, k*15), 1)
	
  circle(screen, (0, 255, 0), (x+k*19, y-k*40), k*5) #глаза
  circle(screen, (0, 0, 0), (x+k*19, y-k*40), k*5, 1)
  ellipse(screen, (0, 0, 0), (x+k*18, y-k*45, k*2, k*10))
  circle(screen, (0, 255, 0), (x+k*41, y-k*40), k*5)
  circle(screen, (0, 0, 0), (x+k*41, y-k*40), k*5, 1)
  ellipse(screen, (0, 0, 0), (x+k*40, y-k*45, k*2, k*10))

  polygon(screen, (0, 0, 0), [(x+k*37, y-k*59),(x+k*44,y-k*54),(x+k*42, y-k*70)]) #уши
  polygon(screen, (0, 0, 0), [(x+k*23, y-k*59),(x+k*16,y-k*54),(x+k*18, y-k*70)])

  circle(screen, (0, 0, 0), (x+k*23, y-k*33), k*7, 1, False, False, False, True) #рот
  circle(screen, (0, 0, 0), (x+k*37, y-k*33), k*7, 1, False, False, True, False)
  circle(screen, (255, 105, 180), (x+k*30, y-k*33), k*2)

def cat_right(screen, x, y, k, color):
  surf = pygame.Surface((300, 300))
  surf.fill((255, 255, 255))
  surf.set_colorkey((255, 255, 255))
  cat(surf, 50, 70, 1, (139, 69, 19))
  rotatedSurf = pygame.transform.flip(surf, True, False)
  screen.blit(rotatedSurf, (600, 450))
fon (0, 0, lite_brown, dark_brown)
klubok(450, 500, 50)
okno (350, 30)
okno(100, 30)
okno(600, 30)
cat(screen, 0, 0, 2.2, (139, 69, 19))  #70 500
cat(screen, 450, 400, 1.0, (150, 150, 150))
klubok(530, 450, 30)
#cat_right(screen, 50, 70, 


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finished = True

pygame.quit()
