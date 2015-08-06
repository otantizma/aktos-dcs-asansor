from aktos_dcs import *

class Cabin(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.direction = "stop"
        self.cabin_height = 0  # cm
        Limiter()
        self.limit_status = "can_move"

    def handle_LimitMessage(self,msg):
        self.limit_status = msg.limit_status

    def handle_MotorMessage(self, msg):
        self.direction = msg.direction
        if self.limit_status == "cant_move":
            self.send(CabinHeightMessage(height=self.cabin_height, direction=msg.direction))

    def action(self):
        while True:
            if self.limit_status == "can_move":
                if self.direction == "up":
                    self.cabin_height += 10
                    self.send(CabinHeightMessage(height=self.cabin_height, direction="up"))

                elif self.direction == "down":
                    self.cabin_height -= 10
                    self.send(CabinHeightMessage(height=self.cabin_height, direction="down"))

            sleep(0.1)  # update interval

class CabinHeightScreen(Actor):
    def handle_CabinHeightMessage(self, msg):
        print "elevator is at this meter:", msg.height

class FloorSwitch(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.this_floor = 1
        self.this_height = 300

    def handle_CabinHeightMessage(self,msg):
        if msg.height == self.this_height:
            print "Elevator is at this floor:",self.this_floor


class Limiter(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.elevator_height = 1000  # cm

    def handle_CabinHeightMessage(self, msg):
        if (msg.height >= self.elevator_height and msg.direction == "up"
                or msg.height <= 0 and msg.direction == "down"):
            self.send(LimitMessage(limit_status="cant_move"))
            print "should not exceed physical limits of elevator. Stopping."
        else:
            self.send(LimitMessage(limit_status="can_move"))


if __name__ == "__main__":
    ProxyActor()
    CabinHeightScreen()
    Cabin()
    Limiter()
    FloorSwitch()

    wait_all()
