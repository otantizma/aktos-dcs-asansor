from aktos_dcs import *

class Motor(Actor):
    # 3 yon mesaji var
    # her seferinde 1 cm ciksin
    # yukseklik degiskenini tutsun
    def __init__(self):
        Actor.__init__(self)
        self.direction = "stop"
        self.cabin_height = 0
        self.move_cabin()

    def handle_MotorMessage(self,msg):
        self.direction = msg.direction

    def move_cabin(self):
        while True:
            if self.direction == "up":
                self.cabin_height = self.cabin_height + 1

            elif self.direction == "down":
                self.cabin_height = self.cabin_height - 1

            self.send(ViewerMessage(height=self.cabin_height))
            sleep(1) # update interval

class Limit_Organizer(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.max_level = 5
        self.min_level = 0

    def handle_ViewerMessage(self,msg):
        if msg.height == self.max_level:
            self.send(MotorMessage(direction="stop"))


class Viewer(Actor):
    def handle_ViewerMessage(self,msg):
        print time.time(), msg.height


if __name__ == "__main__":
    ProxyActor()
    view = Viewer()
    motor = Motor()

    wait_all()