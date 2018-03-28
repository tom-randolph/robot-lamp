import matplotlib.pyplot as plt
from track_sim import Controller
import numpy as np
#from scipy.integrate import odeint

setpoint=341.4
pos=0
dt=.01

PID=Controller(.5,1,.005,time=True)

ts=np.arange(0,1,dt)
ys=[]
integral=[]
error=[]
der=[]
for t in ts:
    ys.append(pos)
    integral.append(PID.integral)
    error.append(PID.error)
    der.append(PID.der)
    pos=pos+PID.compute(setpoint-pos,dt)

    #print(PID.error)


f, (ax1,ax2)=plt.subplots(1,2)
ax1.plot(ts,ys)
ax2.plot(ts,integral)
ax2.plot(ts,error)
ax2.plot(ts,der)
ax2.legend(['integral','error','derivative'])
plt.show()
