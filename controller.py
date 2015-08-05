from aktos_dcs import *

class Controller(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.control()

    def control(self):
        while True:
            print "will sen up"
            self.send(MotorMessage(direction="up"))
            sleep(3)
            print "stop now"
            self.send(MotorMessage(direction="stop"))
            sleep(1)
            print "down"
            self.send(MotorMessage(direction="down"))
            sleep(3)


if __name__ == "__main__":
    ProxyActor()
    controller = Controller()

    wait_all()
