import pygame
from pygame.draw import*
from random import randint
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
w = 1200
h = 600
FPS = 30
t = 0.1
money_parameter = 1

#CHEETING

end_of_cheeting = False
while not end_of_cheeting:
    cheeting = str(input())
    if cheeting == 'SPEED_HUCK':
        t = 0.01
    elif cheeting == 'MONEY_BUST':
        money_parameter = int(input())
    else:
        end_of_cheeting = True

screen = pygame.display.set_mode((w, h))

#Ball colors

number_of_balls = 10
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# Letters that accept

LETTERS = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o',
           'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
           'z', 'x', 'c', 'v', 'b', 'n', 'm', '0', '1', '2', '3',
           '4', '5', '6', '7', '8', '9']

def check_for_penitration(x0, y0, x, y, r):
    
    '''if you click ball, return True, if you miss - False'''
    
    if ((x0-x)**2+(y0 - y)**2)**0.5 < r:
        return True
    else:
        return False
        
def pay_for_good_job(type_b):
    
    '''good job needs to be paied'''
    
    if type_b == 'COMMON':
        return 1*money_parameter
    elif type_b == 'PULSAR':
        return 5*money_parameter
    elif type_b == 'RANDOM':
        return 2*money_parameter

def check_for_walls(x, y, vx, vy, r):
    
    '''Check for walls, nothing special'''
    
    if x > w-r:
        vx = -vx
    if y > h-r:
        vy = - vy
    if x < r:
        vx = -vx
    if y < r:
        vy = - vy
    return vx, vy


def new_ball(type_b_input):
    
    ''' define a ball '''
    
    if type_b_input == 'COMMON':
        type_b = type_b_input
        r = randint(10, 50)
        x = randint(r, w-r)
        y = randint(r, h-r)
        color = COLORS[randint(0, 5)]
        vx, vy = randint(-10, 10), randint(-10, 10)
        ball = [x, y, vx, vy, r, color, type_b, 0]
    elif type_b_input == 'PULSAR':
        type_b = type_b_input
        r = 15
        x = randint(r, w-r)
        y = randint(r, h-r)
        color = (200, 200, 200)
        vx, vy = randint(20, 30), randint(-30, 30)
        ball = [x, y, vx, vy, r, color, type_b, 0]
    elif type_b_input == 'RANDOM':
        type_b = type_b_input
        r = randint(20,50)
        x = randint(r, w-r)
        y = randint(r, h-r)
        color = RED
        ball = [x, y, 0, 0, r, color, type_b, randint(FPS//2,FPS*2)]
    return ball

def rendering(screen, ball):
    
    '''Draw a ball on the screen, each ball has a type'''
    
    if ball[6] == 'COMMON':
        circle(screen, ball[5], (ball[0], ball[1]), ball[4])
    elif ball[6] == 'PULSAR':
        circle(screen, ball[5], (ball[0], ball[1]), ball[4])
    elif ball[6] == 'RANDOM':
        circle(screen, ball[5], (ball[0], ball[1]), ball[4], 5)
        

def action(screen, ball):
    
    '''This function defines balls movements'''
    
    if ball[6] == 'COMMON':
        ball[2], ball[3] = check_for_walls(ball[0], ball[1], ball[2], ball[3], ball[4])
        ball[0]+=ball[2]*t
        ball[1]+=ball[3]*t
    elif ball[6] == 'PULSAR':
        if ball[7] == 0:
            ball[7] = randint(90,99)/100
        if (ball[2]**2 + ball[3]**2)**0.5 < 20 or (ball[2]**2 + ball[3]**2)**0.5 > 150:
            ball[7] = 1/ball[7]
        ball[2], ball[3] = check_for_walls(ball[0], ball[1], ball[2], ball[3], ball[4])
        ball[0]+=ball[2]*t
        ball[1]+=ball[3]*t
        ball[2] = ball[2]*ball[7]
        ball[3] = ball[3]*ball[7]
    elif ball[6] == 'RANDOM':
        if time % ball[7] == 0:
            ball[1] = randint(ball[4], h-ball[4])
            ball[0] = randint(ball[4], w-ball[4])
    elif ball[6] == 'NONE':
        None

# __main__

pygame.display.update()
clock = pygame.time.Clock()
finished = False
score = 0
c = 0   # c - previous number of clicks
level = 1
life = 50
clicks = 1
time = 0
number_of_balls = 5
curent_number = number_of_balls
balls = [[0, 0, 0, 0, 0, '0', 'NONE', 0]]*number_of_balls

for i in range(number_of_balls):
    balls[i] = new_ball('COMMON')

#Main_game_space

while not finished:
    clock.tick(FPS)
    time+=1
    if time > 1000:
        time = 0
    c = clicks
    
    catched = []
    if curent_number == 0:
        level+=1
        number_of_balls=int((25+level)**0.7)
        curent_number = number_of_balls
        balls = [[0, 0, 0, 0, 0, '0', 'NONE', 0]]*number_of_balls
        for i in range(number_of_balls):
            RANDOM = randint(1,100)
            if RANDOM < 20:
                balls[i] = new_ball('PULSAR')
            elif RANDOM < 40:
                balls[i] = new_ball('RANDOM')
            else:
                balls[i] = new_ball('COMMON')

    if life <= 0:
        finished = True
        
    screen.fill(BLACK)
    for ball in balls:
        action(screen, ball)
        rendering(screen, ball)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x0, y0 = event.pos
            for i in range(number_of_balls):
                ball = balls[i]
                if ball[6] != 'NONE':
                    if check_for_penitration(x0, y0, ball[0], ball[1], ball[4]):
                        catched.append(i)
                        curent_number+=-1
                        score+=pay_for_good_job(ball[6])        
            clicks+=1
            if c != clicks and len(catched) == 0:
                life+=-1
    for i in catched:
        balls[i][6] = 'NONE'
    #Parameters
    text = myfont.render("Score = "+str(score)+"  Health = "+str(life)+
                         "   Level = "+str(level), True, [255, 255, 255])
    textpos = (10, 10)
    screen.blit(text, textpos)
    pygame.display.update()

#Game_over
finished = False
while not finished:
    clock.tick(FPS)
    screen.fill(BLACK)
    text = myfont.render("YOU DIED", True, [255, 255, 255])
    textpos = (w/2-50, h/2)
    screen.blit(text, textpos)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            finished = True


#Write_your_name
name_of_gamer = ''
finished = False 
while not finished:
    clock.tick(FPS)
    screen.fill(BLACK)
    text = myfont.render("Write Your Name", True, [255, 255, 255])#Write your name
    textpos = (w/2-100, h/2-50)
    screen.blit(text, textpos)
    text = myfont.render(name_of_gamer, True, [255, 255, 255])
    textpos = (w/2-100, h/2)
    screen.blit(text, textpos)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            for i in LETTERS:
                if event.key == eval('pygame.K_'+i):
                    name_of_gamer+=i
            if event.key == pygame.K_BACKSPACE:
                name_of_gamer = name_of_gamer[0:len(name_of_gamer)-1]
            if event.key == pygame.K_SPACE:
                name_of_gamer+='_'
            if event.key==pygame.K_RETURN:
                finished = True


#Leaderboard_Change
leaderboard = open('leaderboard.txt', 'r')
helper = open('helper.txt', 'w')
s = leaderboard.readline()
H = False
while s != '':
    i = 0
    while s[i] != ' ':
        i+=1
    j = i+1
    while s[j]!= ' ':
        j+=1
    if int(s[i+1:j]) < score and not(H):
        H = True
        print(str(name_of_gamer)+" "+str(score)+" "+str(level),file=helper)
    helper.write(s)
    s = leaderboard.readline()
if not H:
    print(str(name_of_gamer)+" "+str(score)+" "+str(level),file=helper)
helper.close()
leaderboard.close()

helper = open('helper.txt', 'r')
leaderboard = open('leaderboard.txt', 'w')
s = helper.readline()
while s != '':   
    leaderboard.write(s)
    s = helper.readline()
helper.close()
leaderboard.close()

#Show leaders

finished = False
while not finished:
    clock.tick(FPS)
    leaderboard = open('leaderboard.txt', 'r')
    screen.fill(BLACK)
    text = myfont.render("Leaderboard", True, [255, 255, 255])#Write your name
    textpos = (w/2-100, 20)
    screen.blit(text, textpos)
    i = 0
    s = leaderboard.readline()
    while i < 10 and s != '' and H:
        text = myfont.render(s.rstrip(), True, [255, 255, 255])
        textpos = (w/2-100, 50+i*50)
        screen.blit(text, textpos)
        i+=1
        s = leaderboard.readline()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            finished = True
    leaderboard.close()
pygame.quit()
