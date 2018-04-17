'''This file contains usefull Classes to Simulate and Implement
PID control of a camera gimbal with computer vision'''

import numpy as np
import cv2


# colors defined in BGR
colors = {
    "red":(0,0,255),
    "yellow":(0,255,255),
    "green":(0,255,0)
    }



class Camera(object):
    '''A camera simulation.
    This represents a virtual camera frame within the physical camera FOV.
    This serves the purpose of simulating the tracking algorithm without any physical actuators.'''
    def __init__(self,size,pos):

        #defines the center of the virtual frame
        self.pos=np.array(pos)
        #defines the size of the virtual frame
        self.size=np.array(size)
        #the frames initial color is red
        self.color=colors["red"]

    def take_image(self,pos):
        #TODO: merge this with the get_difference and is_in_frame methods

        #this method checks to see if the point of interest is in frame
        if self.is_in_frame(pos):
            #if it is color the frame green
            self.color=colors["green"]
            #and return the vector between the frame center and the p.o.i.
            return self.get_difference(pos)
        else:
            #else color the frame yellow
            self.color=colors["yellow"]
            #and return false
            return False

    def is_in_frame(self,pos):
        #this method calculates whether the p.o.i. falls within the frame
        #this variable defines the extents of the frame in both dimesnions
        extents=np.vstack((self.pos+self.size/2.0,self.pos-self.size/2.0)).T
        #truths will define whether or not each component of the p.o.i. falls between the extents in that dimension
        truths=list(map(lambda coord,ext:coord>ext[1] and coord<ext[0],pos,extents))

        #if either of the components do not fall between the extents, the methods returns false
        for truth in truths:
            if not truth:
                return False
        #if not it returns true to say yes, it is in frame
        return True

    def render(self,window):
        #draws the virtual frame on an existing cv2 window in the correct position, and with the appropriate color
        cv2.rectangle(window,tuple((self.pos-self.size/2.0).astype(int)),tuple((self.pos+self.size/2.0).astype(int)),self.color,3)

    def get_difference(self,pos):
        #returns the difference between virtual frame center and p.o.i.
        return np.array(pos)-self.pos

    def process_frame(self,blob):
        #updates the virtual frame position to match the p.o.i. location
        img_data = self.take_image(blob)
        if img_data:
            self.update_rel(img_data)

    def update_rel(self,delta):
        #move the frame to a position relative to its current position
        self.pos=self.pos+np.array(delta)
    def update_abs(self,pos):
        #move the frame to an arbitrary location in space
        self.pos=np.array(pos)




class Blob(object):
    ''' This is an object to simulate a blob that would normally be detected by the physical camera.
    Can be used in liue of a physical camera with blob detection.''''
    def __init__(self,radius,pos):
        #define a radius and location
        self.pos=np.array(pos)
        self.radius=radius
    def update(self,pos):
        #move the blob
        self.pos=np.array(pos)

    def render(self):
        #TODO implement rendering method for opencv
        pass

class Controller(object):

    '''This is a P, PI, PD, or PID controller class to provide closed loop tracking for
    a camera. Can be used with physical camera and actuators (gimbal), or with virtual camera frame'''

    def __init__(self,Kp,Ki=0,Kd=0,time=False):
        #timesteps can be predetermined as an aapproximation, or can be calculated in real time
        # set flag true to compute timestep
        self.use_time=time
        #proportional gain
        self.Kp=Kp
        #integral gain (default 0)
        self.Ki=Ki
        #derivitive gain (default 0)
        self.Kd=Kd
        #running calculated error intgral
        self.integral=None
        #current derivitive
        self.der=None
        #current error
        self.error=None

    def compute(self,error,dt=1):
        #error is passed in from camera class (get_difference method)
        self.error=np.array(error)
        #the integral will not be defined the first time this is run.
        #This allows the algorithm to be 1 or 2 dimensional, based on dimension of error term passed
        if self.integral is not None:
            #calculate integral using right hand reimmans sum
            self.integral=self.integral+self.error*dt
            if self.use_time:
                #computes timestep
                import time
                now=time.time()
                dt=now-self.time
                self.time=now
        else:
            #this will set the integral and derivitve to zero the first time run
            self.reset()
            if self.use_time:
                import time
                self.time=time.time()
        #calculate discrete integral
        self.der=self.error/dt

        #returns the entire compensation term
        return np.array(self.Kp*self.error+self.Ki*self.integral+self.Kd*self.der)

    def reset(self):
        #this is used to return time dependendent terms to zeros
        #this is need on startup, and when the tracked object leaves the frame.
        if self.error is not None:
            self.integral=np.zeros(self.error.size)
            self.der=np.zeros(self.error.size)
