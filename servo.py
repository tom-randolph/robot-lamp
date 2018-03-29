import serial

class ArduServo(object):

    def __init__(self,port,baud=9600):
        self.port=port;
        self.baud=baud;
        self.pos=0;


    def open(self):
        try:
            self.ser=serial.Serial(self.port,self.baud);
        except:
            raise;
    def close(self):
        try:
            self.ser.close();
        except:
            raise;
    def write(self,pos):
        if pos >150: pos =150;
        if pos<90: pos =90;
        self.pos=pos;
        print(pos);
        self.ser.write(bytearray([pos]));

if __name__=="__main__":
    import time
    servo =ArduServo('COM4');
    servo.open();

    while(True):
        print('looped');
        servo.write(180);
        time.sleep(500);
        servo.write(0);
        time.sleep(500);
