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
    point=pygame.mouse.get_pos()
    i=0
    lamp=Lamp()
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
        # if keys[K_UP]:
        #        point[1]+=.2
        # if keys[K_DOWN]:
        #        point[1]-=.2
        # if keys[K_RIGHT]:
        #        point[0]+=.2
        # if keys[K_LEFT]:
        #        point[0]-=.2
        point=pix_to_inches(pygame.mouse.get_pos())
        # point+=np.array(pygame.mouse.get_rel())

        if keys[pygame.K_ESCAPE]:
            terminate()
        #point=np.array((locs[i],locs[i+1]))
        #print(point)

        # theta1,theta2=update_angles((arm1,arm2),point)
        # if theta1 is not False:
        #     arm1.update(base,np.around(theta1,2))
        #     arm2.update_rel(arm1,np.around(theta2,2))
        # if i<10:i+=2
        # else:i=0
        update_angles((arm1,arm2),point)
        lamp.update(point)



        DISPLAYSURF.fill(BGCOLOR)

        # arm1.draw()
        # arm2.draw()
        lamp.draw()
        pygame.draw.circle(DISPLAYSURF,RED,inches_to_pix(point),3)
        pygame.draw.circle(DISPLAYSURF,BLUE,inches_to_pix((0,0)),int(2*40*8.25),3)
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


# def update_angles(arms,point):
#     point=np.array(point)
#     base=arms[0].base
#     x,y=(point-base)
#     l_t=np.hypot(*(x,y))
#     r=arms[0].length
#     max_radius=functools.reduce(lambda arm1,arm2: arm1.length+arm2.length, arms)
#     if abs(l_t)<=max_radius:
#         phi=np.arctan(y/x)
#         phi_=np.arccos(.5*l_t/r)
#         theta=phi+phi_
#         a=r*np.cos(theta)
#         b=r*np.sin(theta)
#
#
#         alpha=-2*phi_
#
#
#         return (theta,alpha)
#     return (False,False)

def update_angles(arms,point):
    point=np.array(point)
    base=arms[0].base
    x,y=(point-base)
    dist=np.hypot(*(x,y))/2
    radius=arms[0].length
    if abs(dist)<=radius:
        thetaMid=np.arctan(y/x)
        ySide=np.sqrt(radius**2-dist**2)
        phi=np.arctan(ySide/dist)
        theta=thetaMid+phi
        #a=r*np.cos(theta)
        #b=r*np.sin(theta)


        alpha=-2*phi
        print(theta)
        print(alpha)

        return (theta,alpha)
    return (False,False)


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

class Arm(object):

    '''A class to describe a segment of the robot arm'''
    length=8.25
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
        pygame.draw.line(DISPLAYSURF,WHITE,inches_to_pix(self.base+self.offset),inches_to_pix(self.end+self.offset),5)
        pygame.draw.line(DISPLAYSURF,WHITE,inches_to_pix(self.base),inches_to_pix(self.base+self.offset),5)
        pygame.draw.line(DISPLAYSURF,WHITE,inches_to_pix(self.end),inches_to_pix(self.end+self.offset),5)


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
        pygame.draw.line(DISPLAYSURF,WHITE,inches_to_pix(self.proximal.end+self.proximal.offset),inches_to_pix(self.distal.base+self.distal.offset),5)
    def update(self,point):
        point=np.array(point)
        x,y=(point-self.proximal.base)
        dist=np.hypot(*(x,y))/2
        radius=self.proximal.length
        if abs(dist)<=radius:
            thetaMid=np.arctan(y/x)
            ySide=np.sqrt(radius**2-dist**2)
            phi=np.arctan(ySide/dist)
            self.beta=thetaMid+phi
            self.alpha=-2*phi
            print("arm")
            print(self.beta)
            print(self.alpha)
        self.proximal.update(self.base,self.beta)
        self.distal.update_rel(self.proximal,self.alpha)




if __name__ == '__main__':
    main()
