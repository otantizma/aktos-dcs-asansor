from aktos_dcs import Actor,  ProxyActor, sleep, joinall
from aktos_dcs import gevent_actor
import gevent
from aktos_dcs.Messages import *
from gevent.socket import wait_read
import sys

class Controller(Actor):
    def __init__(self):
        Actor.__init__(self)

    def mesaj_gonder(self):
        self.send(MotorMessage(direction="up",reciever="motor"))


if __name__ == "__main__":
    pass