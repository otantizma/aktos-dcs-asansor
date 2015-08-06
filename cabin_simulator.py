from aktos_dcs import *
import math

class Cabin(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.direction = "stop"
        self.cabin_height = 0  # cm
        Limiter()
        self.limit_status = "can_move"

    def handle_LimitMessage(self, msg):
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

    def handle_UpdateIoMessage(self, msg):
        floor_ratio = float(self.cabin_height)/300.0  # what an ugly code
        if floor_ratio % 1 < 0.34 or floor_ratio % 1 > 0.96:
            self.send(IoMessage(pin_name="floor."+str(int(round(floor_ratio)))))  # height of a floor is 300 cm


class CabinHeightScreen(Actor):
    def handle_CabinHeightMessage(self, msg):
        print "elevator's position", msg.height, "cm"

class FloorSwitch(Actor):
    def __init__(self, this_floor, switch_position):
        Actor.__init__(self)
        self.this_floor = this_floor
        if switch_position == "upper":
            self.this_height = 300 * this_floor + 10
        elif switch_position == "lower":
            self.this_height = 300 * this_floor - 10

    def handle_CabinHeightMessage(self, msg):
        if msg.height == self.this_height:
            self.send(IoMessage(pin_name="floor."+str(self.this_floor)))
            print "Elevator is at this floor:", self.this_floor


class Limiter(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.elevator_height = 1200  # cm
        self.limit_status = "can_move"

    def handle_CabinHeightMessage(self, msg):
        if (msg.height >= self.elevator_height and msg.direction == "up"
                or msg.height <= 0 and msg.direction == "down"):
            self.limit_status="cant_move"
            self.send(LimitMessage(limit_status="cant_move"))
            print "should not exceed physical limits of elevator. Stopping."
        elif self.limit_status == "cant_move":
            self.limit_status = "can_move"
            self.send(LimitMessage(limit_status="can_move"))


if __name__ == "__main__":
    ProxyActor()
    CabinHeightScreen()
    Cabin()
    Limiter()
    for i in range(10):
        FloorSwitch(i, "upper")
        FloorSwitch(i, "lower")

    wait_all()
