from aktos_dcs.Messages import *

class CabinHeightMessage(Message):
    height = 0.0

class MotorMessage(Message):
    direction = ""

class LimitMessage(Message):
    limit_status = ""
