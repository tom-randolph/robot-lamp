import random, pygame, sys, functools
import numpy as np
from numpy import pi as PI
from pygame.locals import *
FPS =30
WINDOWWIDTH = 1080
WINDOWHEIGHT = 720

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Robot Arm')

    #showStartScreen()
    runGame()



def runGame():
    base=(0,0)
    millis=0
    theta1=PI/2
    theta2=0
    arm1=Arm(base,theta1)
    arm2=Arm(arm1.end,theta2)
    arm3=Arm(arm1.end,theta2)
    pix_to_inches(arm1.end)
    point=[6,6]

    while True: # main game loop
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                terminate()
        keys=pygame.key.get_pressed()
        # if keys[K_UP]:
        #        theta2-=PI/100
        # if keys[K_DOWN]:
        #        theta2+=PI/100
        # if keys[K_RIGHT]:
        #        theta1-=PI/100
        # if keys[K_LEFT]:
        #        theta1+=PI/100
        if keys[K_UP]:
               point[1]+=.2
        if keys[K_DOWN]:
               point[1]-=.2
        if keys[K_RIGHT]:
               point[0]+=.2
        if keys[K_LEFT]:
               point[0]-=.2

        if keys[pygame.K_ESCAPE]:
            terminate()

        theta1,theta2=update_angles((arm1,arm2),point)
        if theta1 is not False:
            arm1.update(base,theta1)
            arm2.update_rel(arm1,theta2)




        DISPLAYSURF.fill(BGCOLOR)

        arm1.draw()
        arm2.draw()
        pygame.draw.circle(DISPLAYSURF,RED,inches_to_pix(point),10)
        millis_old=millis
        millis= pygame.time.get_ticks()
        secs=millis/1000.
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()


def drawTime(millis):
    timeSurf = BASICFONT.render('Time: %s' % (millis), True, WHITE)
    timeRect = timeSurf.get_rect()
    timeRect.topleft = (WINDOWWIDTH - 320, 10)
    DISPLAYSURF.blit(timeSurf, timeRect)


def update_angles(arms,point):
    point=np.array(point)
    base=arms[0].base
    x,y=(point-base)
    l_t=np.hypot(*(x,y))
    r=arms[0].length
    max_radius=functools.reduce(lambda arm1,arm2: arm1.length+arm2.length, arms)
    if abs(l_t)<=max_radius:
        phi=np.arctan(y/x)
        phi_=np.arccos(.5*l_t/r)
        theta=phi+phi_
        a=r*np.cos(theta)
        b=r*np.sin(theta)


        alpha=-2*phi_


        return (theta,alpha)
    return (False,False)


def pix_to_inches(pix):
    '''use to put coordinates in "physical frame" from game frame'''
    pix=np.array(pix)
    inches=(pix-((WINDOWWIDTH/2-300),(WINDOWHEIGHT-200)))/40
    return inches
def inches_to_pix(inches):
    inches=np.array((inches[0],-inches[1]))
    pix=(inches*40+((WINDOWWIDTH/2-300),(WINDOWHEIGHT-200))).astype(int)
    #pix[1]*=-1
    return pix

class Arm(object):

    '''A class to describe a segment of the robot arm'''
    length=8
    scale=40

    def __init__(self,base,theta):
        self.update(base,theta)

    def update(self,base,theta):
        self.base=np.array(base)
        self.theta=theta
        self.end=self.length*np.array((np.cos(theta),np.sin(theta)))+self.base
    def update_rel(self,parent,theta):
        self.update(parent.end,theta+parent.theta)

    def draw(self):
        pygame.draw.line(DISPLAYSURF,WHITE,inches_to_pix(self.base),inches_to_pix(self.end),5)




if __name__ == '__main__':
    main()
