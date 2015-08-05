from aktos_dcs import *

class Cabin(Actor):
    # 3 yon mesaji var
    # her seferinde 1 cm ciksin
    # yukseklik degiskenini tutsun
    def __init__(self):
        Actor.__init__(self)
        self.direction = "stop"
        self.cabin_height = 0
        Limiter()

    def handle_MotorMessage(self, msg):
        self.direction = msg.direction

    def action(self):
        while True:
            if self.direction == "up":
                self.cabin_height += 1
                self.send(ViewerMessage(height=self.cabin_height))

            elif self.direction == "down":
                self.cabin_height -= 1
                self.send(ViewerMessage(height=self.cabin_height))

            sleep(1) # update interval

class Viewer(Actor):
    def handle_ViewerMessage(self,msg):
        print time.time(), msg.height


class Limiter(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.elevator_height = 20  # meters

    def handle_ViewerMessage(self, msg):
        if (msg.height > self.elevator_height or
            msg.height < 0):
            print "should not exceed physical limits of elevator. Stopping."
            self.send(MotorMessage(direction="stop"))


if __name__ == "__main__":
    ProxyActor()
    Viewer()
    Cabin()
    wait_all()