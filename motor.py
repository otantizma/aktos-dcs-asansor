from aktos_dcs import Actor,  ProxyActor, sleep, joinall
from aktos_dcs import gevent_actor
import gevent
from aktos_dcs.Messages import *
from gevent.socket import wait_read
import sys

class Cabin(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.height = 0

    def handle_CabinMessage(self,msg):
        self.height = msg.height

class Motor(Actor):
    # 3 yon mesaji var
    # her seferinde 1 cm ciksin
    # yukseklik degiskenini tutsun
    def __init__(self):
        Actor.__init__(self)
        self.direction = "stop"
        self.cabin_height = 0

    def handle_MotorMessage(self,msg):
        if msg.reciever == "motor":
            if self.direction != msg.direction:
                self.direction = msg.direction
                kill(movekabin)
                if msg.direction != "stop":
                    self.direction = msg.direction
                    spawn(movekabin)

    def move_cabin(self):
        if self.direction == "up":
            self.cabin_height = self.cabin_height + 1
        elif self.direction == "down":
            self.cabin_height = self.cabin_height - 1
        sleep(1)
        self.send(CabinMessage(height=self.cabin_height))
        if self.direction == "stop":
            gevent.kill(self.move_cabin())


if __name__ == "__main__":
    pass