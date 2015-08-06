from aktos_dcs import *

class SimulatorInputActor(Actor):

    def action(self):
        max_move_time = 4  # seconds

        while True:
            print "going up"
            self.send(MotorMessage(direction="up"))
            sleep(max_move_time)
            # print "stopping..."
            # self.send(MotorMessage(direction="stop"))
            # sleep(2)
            # print "should not exceed top level"
            # self.send(MotorMessage(direction="up"))
            # sleep(5)
            print "down"
            self.send(MotorMessage(direction="down"))
            sleep(max_move_time)


if __name__ == "__main__":
    ProxyActor()
    SimulatorInputActor()
    wait_all()
