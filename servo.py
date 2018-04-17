import serial

class ArduServo(object):
    '''This is a first implementation of an abstracted servo on an arduino. We use pyserial to communicate with the arduino,
    which is listening for commands and writing them directly to a servo.'''
    #TODO implement multiple servo control
    def __init__(self,port,baud=9600):
        #setup the servo object with a serial port and baud rate
        self.port=port
        self.baud=baud
        #initialize positon as zero
        self.pos=0


    def open(self):
        try:
            #attempt to connect over serial
            self.ser=serial.Serial(self.port,self.baud)
        except:
            #TODO handle exceptions for por already being open
            raise
    def close(self):
        try:
            #close the serial connection
            self.ser.close()
        except:
            #TODO handle exceptions for port not being open
            raise
    def write(self,pos):
        #checking if the command is a valid integer between 0 and 180
        assert pos in range(0,181)
        #update member variable
        self.pos=pos
        #send the command over serial as bytearray, this ensures it is interpretted as the correct type on the arduino
        self.ser.write(bytearray([pos]))

if __name__=="__main__":
    import sys
    # a short test example to ensure it is working, port name can be passed as CL arg
    import time
    port='COM4'
    if len(sys.argv)>1:
        port=sys.argv[1]
    servo =ArduServo(port)
    servo.open()

    while(True):
        print('looped')
        servo.write(180)
        time.sleep(5)
        servo.write(0)
        time.sleep(5)
