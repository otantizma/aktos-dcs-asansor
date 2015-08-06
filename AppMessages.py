from aktos_dcs.Messages import *

class CabinHeightMessage(Message):
    height = 0

class MotorMessage(Message):
    direction = ""

class LimitMessage(Message):
    limit_status = ""

class IoMessage(Message):
    pin_name = 0
    pin_number = ""
    val = ""
    last_change = False

class UpdateIoMessage(Message):
    pass