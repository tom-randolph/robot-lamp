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
        assert pos in range(0,181);
        self.pos=pos;
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
