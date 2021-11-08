''' Game "The gun" by Rogozhnikov Vasili '''
import math
from random import choice
from random import randrange as rnd
import pygame


FPS = 30

yellow = (0, 255, 255)
RED = 0xFF0000
BLUE = 0x0000FF
yellow = YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)                   
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

def field(screen):
    pygame.draw.rect(screen, (0, 150, 0), (0, 470, 800, 130))

def tree(screen, x, y, l, color_stvol, color_listia, levels):
    """
        x, y - координаты центра ствола снизу
        l - характерный размер дерева, длина ствола, основа для расчёта кроны
        color_stvol и color_listva не нуждаются в комментариях
        levels - уровни кроны
        крона рандомна, значения ширины и высоты овалов принадлежат [l, 2l] и [1.5l, 3l] соотв.
        возвращает высоту дерева h
    """
    pygame.draw.line(screen, color_stvol, (x, y), (x,y-l), l//4)
    pygame.draw.ellipse(screen, color_listia, (x-l/2, y-l*1.6, l, 0.9*l), 0)
    pygame.draw.ellipse(screen, yellow, (x-l/2-1, y-l*1.6-1, l+2, 0.9*l+2), 1)
    pygame.draw.ellipse(screen, color_listia, (x-l, y-l*2.4, 2*l, 1.0*l), 0)
    pygame.draw.ellipse(screen, yellow, (x-l-1, y-l*2.4-1, 2*l+2, 1.0*l+2), 1)
    pygame.draw.ellipse(screen, color_listia, (x-l*0.6, y-3.4*l, 1.2*l, 1.6*l), 0)
    pygame.draw.ellipse(screen, yellow, (x-l*0.6-1, y-3.4*l-1, 1.2*l+2, 1.6*l+2), 1)

def tank(gun):
    
    ''' Function draw a tank, return Pygame.surface object '''
    
    surf = pygame.Surface((300, 300))
    surf.fill((255, 255, 255))
    surf.set_colorkey((255, 255, 255))
    pygame.draw.rect(surf, (0, 0, 0), (130, 145, 20, 10))
    pygame.draw.rect(surf, (0, 0, 0), (115, 155, 50, 12))
    for i in range(6):
        pygame.draw.circle(surf, (0, 0, 0), ((120+9*i), 165), 6)
        pygame.draw.circle(surf, (0, 200, 0), ((120+9*i), 165), 5)
    if not gun.orientation:
        surf = pygame.transform.flip(surf, True, False)
    pygame.draw.line(surf,gun.color,
                     (150, 150),
                     (gun.x+(gun.f2_power/10+10)*math.cos(gun.an)-gun.x+150,
                      gun.y+(gun.f2_power/10+10)*math.sin(gun.an)-gun.y+150),
                     3)
    return surf

def tank_target(tank):
    
    '''Function draw a AI tank, return Pygame.surface object'''
    
    surf = pygame.Surface((300, 300))
    surf.fill((255, 255, 255))
    surf.set_colorkey((255, 255, 255))
    pygame.draw.rect(surf, (0, 0, 0), (130, 145, 20, 10))
    pygame.draw.rect(surf, (0, 0, 0), (115, 155, 50, 12))
    pygame.draw.line(surf, tank.color, (150, 150), (170, 150), 3)
    for i in range(6):
        pygame.draw.circle(surf, (0, 0, 0), ((120+9*i), 165), 6)
        pygame.draw.circle(surf, (0, 200, 0), ((120+9*i), 165), 5)
    if not tank.vx > 0:
        surf = pygame.transform.flip(surf, True, False)
    return surf

class Ball:
    
    '''global class defines bullets (balls)'''
    
    def __init__(self, screen: pygame.Surface, x, y, tipe):
        
        """ Конструктор класса ball
        Аргументы:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        global global_y
        self.y_min = global_y + 20
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 1
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.tipe = tipe  #лазер or common
        if self.tipe == 'C':
            self.live = 80
        elif self.tipe == 'L':
            self.live = 80
        elif self.tipe == 'D':
            self.live = 80
        elif self.tipe == 'DL': # auto tanks
            self.live = 30


    def move(self):
        
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки.
        То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy,
        силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        
        if self.live <= 0:
            self.x = -100
            self.y = -100
        else:
            if self.tipe == 'C':
                fi = 0.5
                C = 3   # изменение vy
            elif self.tipe == 'L':
                fi = 0
                C = 0
            elif self.tipe == 'D':
                fi = 0
                C = 0.1
                if self.vy == 0:
                    self.x = self.y = -100
            elif self.tipe == 'DL':
                fi = 0
                C = 0
                    
            self.x += self.vx
            self.y -= self.vy
            self.vy -= C
            if self.tipe != 'DL' and self.tipe != 'L':
                if self.x > 800-self.r:
                    self.vx = - fi*self.vx
                    self.vy = self.vy*fi
                    self.x += self.vx
                if self.x < self.r:
                    self.vx = - fi*self.vx
                    self.vy = self.vy*fi
                    self.x += self.vx
                if self.y > self.y_min-self.r:
                    self.vy = - fi*self.vy
                    self.vx = self.vx*fi
                    self.y -= self.vy
                if self.y < self.r:
                    self.vy = - fi*self.vy
                    self.vx = self.vx*fi
                    self.y -= self.vy
            else:
                if self.x > 800-self.r:
                    self.vx = - fi*self.vx
                    self.vy = self.vy*fi
                    self.x += self.vx
                if self.x < self.r:
                    self.vx = - fi*self.vx
                    self.vy = self.vy*fi
                    self.x += self.vx
                if self.y > 600:
                    self.vy = - fi*self.vy
                    self.vx = self.vx*fi
                    self.y -= self.vy
                if self.y < self.r:
                    self.vy = - fi*self.vy
                    self.vx = self.vx*fi
                    self.y -= self.vy
            self.live-=1

    def draw(self):
        
        '''function draw a ball (circle)'''
        
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj, who_shoot):
        
        """Функция проверяет сталкивалкивается ли данный обьект с целью,
           описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели.
            В противном случае возвращает False.
        """
        if who_shoot == 'TARGET':
            if self.tipe == 'D' or self.tipe == 'DL':
                if ((self.x - obj.x)**2 + (self.y - obj.y)**2)**0.5 < self.r+10:
                    self.live = 0
                    return True
                else:
                    return False
        elif who_shoot == 'PLAYER':
            if self.tipe != 'D' and self.tipe != 'DL':
                if obj.tipe == 'AIRPLANE':
                    if ((self.x - obj.x)**2 + (self.y - obj.y)**2)**0.5< self.r+obj.r:
                        self.live = 0
                        return True
                    else:
                        return False
                elif obj.tipe == 'TANK':
                    if ((self.x - obj.x)**2 + (self.y - obj.y)**2)**0.5< self.r+obj.r:
                        self.live = 0
                        return True
                    else:
                        return False
        


class Gun:
    
    '''global class defines guns'''
    
    def __init__(self, screen):
        self.orientation = True
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 20
        self.y = 450
        self.alive = 5

    def motion(self, vx, vy):
        self.x+=vx
        if self.y > 450 and vy < 0:
            self.y+=vy
        if self.y < 580 and vy > 0:
            self.y+=vy
            
        
    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event, tipe):
        
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x, self.y, tipe)
        new_ball.r += 5
        if (event.pos[0]-new_ball.x)<0:
            self.an = math.atan2((event.pos[1]-new_ball.y),
                                 -max(abs(event.pos[0]-new_ball.x),0.001))
        if (event.pos[0]-new_ball.x)>0:
            self.an = math.atan2((event.pos[1]-new_ball.y),
                                 max(abs(event.pos[0]-new_ball.x),0.001))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        
        """ Прицеливание. Зависит от положения мыши. """
        
        if event:
            if event.pos[0]-self.x > 0:
                self.an = math.atan2((event.pos[1]-self.y) ,
                                     max(abs(event.pos[0]-self.x),0.001))
            if event.pos[0]-self.x < 0:
                self.an = math.atan2((event.pos[1]-self.y) ,
                                     -max(abs(event.pos[0]-self.x),0.001))
            if abs(self.an) < math.pi/2:
                gun.orientation = True
            else:
                gun.orientation = False
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def auto_targetting(self, obj):
        
        ''' targetting for NPC '''
        
        if obj.x-self.x > 0:
            self.an = math.atan2((obj.y - self.y),
                                 max(abs(obj.x-self.x),0.001))
        if obj.x-self.x < 0:
            self.an = math.atan2((obj.y - self.y),
                                 -max(abs(obj.x-self.x),0.001))
        if abs(self.an) < math.pi/2:
            self.orientation = True
        else:
            self.orientation = False
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY
    
    def auto_fire_start(self):
        self.f2_on = 1

    def auto_fire_end(self, obj):
        new_ball = Ball(self.screen, self.x, self.y, 'DL')
        new_ball.r += 5
        if (obj.x-new_ball.x)<0:
            self.an = math.atan2((obj.y-new_ball.y),
                                 -max(abs(obj.x-new_ball.x),0.001))
        if (obj.x-new_ball.x)>0:
            self.an = math.atan2((obj.y-new_ball.y),
                                 max(abs(obj.x-new_ball.x),0.001))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    
    def draw(self):

        ''' this function draw the tank'''
        
        self.screen.blit(tank(self), (self.x-150, self.y-150))

    def power_up(self):
        
        ''' This function is responsible for changing the force of the shot '''
        
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY
    def alive_check(self):
        ''' checks if the cannon is alive '''
        if self.alive > 0:
            return True
        else:
            return False

class Target:
    
    '''The global class defines targets'''
    
    def __init__(self, screen):
        
        ''' initialization '''
        
        self.airhealth = 5   # global number of airplane healthes
        self.tankhealth = 10 # global number of tank healthes
        self.tipe = choice(['TANK','AIRPLANE'])
        self.vx = rnd(-8,8)
        self.vy = rnd(-8,8)
        self.points = 0
        self.live = 1
        self.screen = screen
        r = self.r = rnd(5, 20)
        self.new_target()
        self.time = 10
        

    def new_target(self):
        
        """ Инициализация новой цели. """
        
        self.tipe = choice(['TANK','AIRPLANE'])
        if self.tipe == 'TANK':
            x = self.x = rnd(300, 780)
            y = self.y = 450
            self.live = self.tankhealth
            self.vx = rnd(-8, 8)
            self.vy = 0
            self.r = 15
            self.gun = Gun(screen)
            self.gun.x = self.x
            self.gun.y = self.y
        if self.tipe == 'AIRPLANE':
            x = self.x = rnd(200, 780)
            y = self.y = rnd(100, 300)
            r = self.r = rnd(10, 20)
            self.vx = rnd(-15, 15)
            self.vy = rnd(-2,2)
            self.live = self.airhealth
            self.gun = None
        color = self.color = RED

    def hit(self, obj, points=1):
        
        """Попадание шарика в цель."""
        
        global number_of_targets, score
        if obj.tipe == 'C':
            self.live -=2
        else:
            self.live -=1
        if target.live <=0:
            number_of_targets-=1
            self.x = -100
            self.y = -100
            score+=1
        self.points += points

    def draw(self):
        
        ''' Draw a target '''
        
        if self.live >= 1:
            if self.tipe == 'AIRPLANE':
                pygame.draw.line(screen, RED,
                                 (self.x-self.r, self.y-2*self.r),
                                 (self.x-self.r+2*self.r*self.live/self.airhealth,
                                  self.y-2*self.r), 3)
                pygame.draw.circle(
                    self.screen,
                    self.color,
                    (self.x, self.y),
                    self.r)
            elif self.tipe == 'TANK':
                pygame.draw.line(screen, RED,
                                 (self.x-20, self.y-40),
                                 (self.x-20+2*self.r*self.live/self.tankhealth,
                                  self.y-40), 3)
                #self.screen.blit(tank_target(self), (self.x-150, self.y-150))
                self.gun.draw()
    
    def check_bomb(self, obj):
        
        ''' Checking whether the target will shoot '''
        
        if self.live > 0:     #need to fix
            if self.tipe == 'AIRPLANE':
                if self.time <= 0:
                    if abs(obj.x - self.x) < 5:
                        self.bomb(obj)
                else:
                    self.time-=1
            elif self.tipe == 'TANK':
                self.gun.auto_targetting(obj)
                if self.time <= 0:
                    self.bomb(obj)
                    self.gun.auto_fire_start()
                else:
                    self.time -= 1
    
    def bomb(self, obj):
        
        ''' Shoot of the target '''
        
        global ball, FPS
        if self.tipe == 'AIRPLANE':
            new_ball = Ball(self.screen, self.x, self.y, 'D')
            new_ball.r += 5
            new_ball.vx = 0
            new_ball.vy = -4
            balls.append(new_ball)
            self.time = 3*FPS
        elif self.tipe == 'TANK':
            self.gun.auto_targetting(obj)
            self.gun.power_up()
            if rnd(0, 10) == 1:
                self.gun.auto_fire_end(obj)
                self.time  = FPS * 5
            
        
        
    def move(self):
        
        ''' motion of the target'''
        
        global global_y
        if self.tipe == 'AIRPLANE':
            if self.live >= 1:
                self.x += self.vx
                self.y += self.vy
                if self.x > 800-self.r:
                    self.x += -rnd(5,15) #+-
                    self.vx = -self.vx
                if self.x < 0:
                    self.x += rnd(5,15)
                    self.vx = -self.vx
                if self.y > 400-self.r:
                    self.y += -2
                    self.vy = -self.vy
                if self.y < self.r:
                    self.y += 2
                    self.vy = -self.vy
            else:
                None
        elif self.tipe == 'TANK':        #
            if self.live >= 1:
                self.x += self.vx
                self.y -= self.vy
                self.gun.x = self.x
                self.gun.y = self.y 
                if abs(self.vy) != 0:
                    self.vy-=0.9
                if rnd(0,100) == 1:
                    self.vy = rnd(10,15)
                    self.y -= 20
                if self.x > 900-self.r:
                    self.x += -rnd(5,15) #+-
                    self.vx = -self.vx
                if self.x < 400:
                    self.x += rnd(5,15)
                    self.vx = -self.vx
                if self.y > global_y and self.vy < 0:
                    self.y = global_y
                    self.vy = 0


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
bullet = 0
balls = []


tipe = 'C'
bullet = 0
score = 0
clock = pygame.time.Clock()
gun = Gun(screen)

global_y = 450
number = 5
targets = []
number_of_targets = number
for i in range(number_of_targets):
    target = Target(screen)
    targets.append(target)

finished = False

while not finished:     # main loop
    screen.fill(WHITE)
    field(screen)
    tree(screen, 600, 470, 80, (137, 88, 34), (100, 250, 50), 3)
    tree(screen, 500, 470, 50, (137, 88, 34), (100, 250, 50), 3)
    gun.draw()
    for target in targets:
        target.move()
        target.check_bomb(gun)
        target.draw()
    for b in balls:
        b.draw()
        if b.live <= 0:
            balls.pop(balls.index(b))
    text = myfont.render("Score = "+str(score)+" live = "+str(gun.alive),
                         True, [0, 0, 0])
    textpos = (10, 10)
    screen.blit(text, textpos)
    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():   # диспетчеризация событий
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
            bullet+=1
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event, tipe)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                tipe = 'C'
            if event.key == pygame.K_2:
                tipe = 'L'
        if pygame.key.get_pressed()[pygame.K_a]:   # motions of the main tank
            gun.motion(-5, 0)
        if pygame.key.get_pressed()[pygame.K_d]:         
            gun.motion(5, 0)
        if pygame.key.get_pressed()[pygame.K_w]:         
            gun.motion(0, -3)
        if pygame.key.get_pressed()[pygame.K_s]:         
            gun.motion(0, 3)
    
    global_y = gun.y
    for b in balls:
        b.move()
        if b.hittest(gun, 'TARGET'):
            gun.alive -= 1
        for target in targets:
            if b.hittest(target, 'PLAYER') and target.live:
                target.hit(b)
    if not(number_of_targets != 0 or balls):
        screen.fill(WHITE)
        text = myfont.render("You win with "+str(bullet//2)+" shots",
                             True, [0, 0, 0])
        textpos = (200, 300)
        screen.blit(text, textpos)#finish
        pygame.display.update()
        for i in range(100):
            clock.tick(FPS)
        for target in targets:
            target.new_target()
            number_of_targets = number
        bullet = 0
    if not(gun.alive_check()):
        screen.fill(WHITE)
        text = myfont.render("Game over. Your final score: "+str(score),
                             True, [200, 0, 0])
        textpos = (100, 300)
        screen.blit(text, textpos)#finish
        pygame.display.update()
        for i in range(100):
            clock.tick(FPS)
        finished = True
    gun.power_up()
    
pygame.quit()
