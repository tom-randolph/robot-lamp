'''This is a demonstartion of the inverse kinematics arm that animates the motion of the arm. The kinematics are calculated in the update_angle() function and Lamp.update() functions
The angles are calculated to keep the arm in the 'elbow up' configuration with the end effector at the location of the mouse. It is all animated in the frame with circles highlighting the range of motion and degrees of freedom.'''

import random, pygame, sys, functools
import numpy as np
from numpy import pi as PI
from pygame.locals import *
FPS =60
WINDOWWIDTH = 1080
WINDOWHEIGHT = 720

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
GRAY  = ( 150,  150,  150)
BLUE      = (0,90,255)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

locs=[  10,10,
  8,10,
  6,10,
  4,10,
  2,10,
  0,10]

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
    arm1=Parallel(base,theta1,segment_type="proximal")
    arm2=Parallel(arm1.end,theta2,segment_type="distal")
    arm3=Arm(arm1.end,theta2)
    pix_to_inches(arm1.end)
    point=[10,10]
    # point=pygame.mouse.get_pos()
    i=0
    lamp=Lamp()
    # pygame.time.delay(2000)
    print(point)
    while True: # main game loop

        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                terminate()
        keys=pygame.key.get_pressed()

        point=pix_to_inches(pygame.mouse.get_pos())
        # point+=command_distance(pix_to_inches(pygame.mouse.get_pos()),lamp.distal.end)

        # point+=np.array(pygame.mouse.get_rel())

        if keys[pygame.K_ESCAPE]:
            terminate()

        lamp.update(point)



        DISPLAYSURF.fill(BGCOLOR)
        pygame.draw.circle(DISPLAYSURF,RED,inches_to_pix(point),int(lamp.proximal.length*40),3)
        pygame.draw.circle(DISPLAYSURF,GREEN,inches_to_pix(base),int(lamp.proximal.length*40),3)

        pygame.draw.circle(DISPLAYSURF,BLUE,inches_to_pix((0,0)),int(2*40*10),3)
        lamp.draw()
        lamp.display_angles()
        lamp.display_pos()

        pygame.draw.circle(DISPLAYSURF,DARKGREEN,inches_to_pix(point),5)

        millis_old=millis
        millis= pygame.time.get_ticks()
        secs=millis/1000.

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()


def pix_to_inches(pix):
    '''use to put coordinates in "physical frame" from game frame'''
    pix=np.array(pix)
    inches=(pix-((WINDOWWIDTH/2-300),(WINDOWHEIGHT-200)))/40
    inches[1]=-inches[1]
    return inches
def inches_to_pix(inches):
    inches=np.array((inches[0],-inches[1]))
    pix=(inches*40+((WINDOWWIDTH/2-300),(WINDOWHEIGHT-200))).astype(int)
    #pix[1]*=-1
    return pix

def command_distance(mouse,end_effector):

    mouse=np.array(mouse)
    end_effector=np.array(end_effector)
    dist=mouse-end_effector
    print(dist)
    # if dist<12:
    #     if dist<4:
    #         cmd=-(-.1,-.1)
    #     elif dist>8:
    #         cmd=(.1,.1)
    if False is True:
        pass
    else: cmd=(0,0)
    return np.array(cmd)




class Arm():

    '''A class to describe a segment of the robot arm'''
    length=10
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
        pygame.draw.line(DISPLAYSURF,GRAY,inches_to_pix(self.base),inches_to_pix(self.end),10)

class Parallel(Arm):
    offset_proximal=np.array((-1,1))
    offset_distal=np.array((1,1))
    def __init__(self,base,theta,segment_type=None):
        super().__init__(base,theta)
        if segment_type == "proximal":
            self.offset=self.offset_proximal
        elif segment_type == "distal":
            self.offset=self.offset_distal
        else:
            print(segment_type)
            print("Second argument must be \"proximal\" or \"distal\"")
            self.offset=np.array((0,0))
    def draw(self):
        super().draw()
        pygame.draw.line(DISPLAYSURF,WHITE,inches_to_pix(self.base+self.offset),inches_to_pix(self.end+self.offset),10)
        pygame.draw.line(DISPLAYSURF,WHITE,inches_to_pix(self.base),inches_to_pix(self.base+self.offset),10)
        pygame.draw.line(DISPLAYSURF,WHITE,inches_to_pix(self.end),inches_to_pix(self.end+self.offset),10)


class Lamp():

    def __init__(self,base=(0,0),beta=PI/2,alpha=PI/2):
        self.base=np.array(base)
        self.beta=beta
        self.alpha=alpha
        self.proximal=Parallel(base,beta,segment_type="proximal")
        self.distal=Parallel(self.proximal.end,alpha,segment_type="distal")

    def draw(self):
        self.proximal.draw()
        self.distal.draw()
        pygame.draw.line(DISPLAYSURF,WHITE,inches_to_pix(self.proximal.end+self.proximal.offset),inches_to_pix(self.distal.base+self.distal.offset),10)
    def update(self,point):
        point=np.array(point)
        x,y=(point-self.proximal.base)
        dist=np.hypot(*(x,y))/2
        radius=self.proximal.length
        if abs(dist)<=radius:
            thetaMid=np.arctan(y/x)
            ySide=np.sqrt(radius**2-dist**2)
            phi=np.arctan(ySide/dist)
            self.beta=np.around(thetaMid+phi,2)
            self.alpha=np.around(-2*phi,2)
            # print("arm")
            # print(self.beta)
            # print(self.alpha)
        self.proximal.update(self.base,self.beta)
        self.distal.update_rel(self.proximal,self.alpha)
    def display_angles(self):
        aSurf = BASICFONT.render('Alpha:  %s ' % (np.around((PI/2+self.alpha),2)), True, WHITE)
        aRect = aSurf.get_rect()
        aRect.topleft = inches_to_pix(self.base)+np.array((30,10))
        DISPLAYSURF.blit(aSurf, aRect)
        bSurf = BASICFONT.render('Beta: %s' % (np.around((self.beta),2)), True, WHITE)
        bRect = bSurf.get_rect()
        bRect.topleft = aRect.bottomleft
        DISPLAYSURF.blit(bSurf, bRect)
    def display_pos(self):
        aSurf = BASICFONT.render('x:  %s ' % (np.around((self.distal.end[0]),2)), True, WHITE)
        aRect = aSurf.get_rect()
        aRect.topleft = inches_to_pix(self.base)+np.array((400,10))
        DISPLAYSURF.blit(aSurf, aRect)
        bSurf = BASICFONT.render('y: %s' % (np.around((self.distal.end[1]),2)), True, WHITE)
        bRect = bSurf.get_rect()
        bRect.topleft = aRect.bottomleft
        DISPLAYSURF.blit(bSurf, bRect)


class Motor():

    def __init__(self):
        pass


if __name__ == '__main__':
    main()
