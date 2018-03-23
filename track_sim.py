import numpy as np
import cv2

colors = {
    "red":(0,0,255),
    "yellow":(0,255,255),
    "green":(0,255,0)
    }


class Camera(object):
    def __init__(self,size,pos):
        self.pos=np.array(pos);
        self.size=np.array(size);
        self.color=colors["red"];

    def take_image(self,pos):
        if self.is_in_frame(pos):
            print("got it")
            self.color=colors["green"]
            return self.get_difference(pos);
        else:

            self.color=colors["yellow"]
            return False

    def is_in_frame(self,pos):
        extents=np.vstack((self.pos+self.size/2.0,self.pos-self.size/2.0)).T
        truths=list(map(lambda coord,ext:coord>ext[1] and coord<ext[0],pos,extents));
        for truth in truths:
            if not truth:
                return False

        return True

    def render(self,window):
        cv2.rectangle(window,tuple((self.pos-self.size/2.0).astype(int)),tuple((self.pos+self.size/2.0).astype(int)),self.color,3)

    def get_difference(self,pos):
        return np.array(pos)-self.pos;
    def process_frame(self,blob):
        img_data = self.take_image(blob);
        if img_data:
            self.update_rel(img_data);

    def update_rel(self,delta):
        self.pos=self.pos+np.array(delta);
    def update_abs(self,pos):
        self.pos=np.array(pos);




class Blob(object):
    def __init__(self,radius,pos):
        self.pos=np.array(pos);
        self.radius=radius;
    def update(self,pos):
        self.pos=np.array(pos);

    def render(self):
        pass

class Controller(object):

    def __init__(self,Kp,Ki=0,Kd=0,time=False):
        #self.pos=np.array(pos);
        self.use_time=time;

        self.Kp=Kp;
        self.Ki=Ki;
        self.Kd=Kd;
        self.integral=None;
        self.der=None;
        self.error=None;
    def compute(self,error,dt=1):


        self.error=np.array(error);
        if self.integral is not None:
            self.integral=self.integral+self.error*dt;
            if self.use_time:
                import time
                now=time.time()
                dt=now-self.time
                self.time=now
        else:
            self.reset()
            if self.use_time:
                import time
                self.time=time.time()
        print('dt');
        print(dt)
        self.der=self.error/dt;
        return np.array(self.Kp*self.error+self.Ki*self.integral+self.Kd*self.der);
        #self.pos=(self.pos+comp).astype(int);
        #return self.pos
    def reset(self):
        if self.error is not None:
            self.integral=np.zeros(self.error.size)
            self.der=np.zeros(self.error.size)
