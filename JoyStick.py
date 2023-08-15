import pygame
import numpy as np
from adam_sdk import AdamManager
from adam_sdk import SerializableCommands
from adam_sdk import MotorCommand

adamController = None
adamController = AdamManager()

pygame.init()
#initialise the joystick module
pygame.joystick.init()

#define max angle in percent
MAX_X_ANGLE = 100
MAX_Y_ANGLE = 100

#create empty list to store joysticks
joysticks = []

#set default position
x = MAX_X_ANGLE / 2
y = MAX_Y_ANGLE / 2

x1 = x
y1 = y
x2 = 0
y2 = 15
x3 = 0
y3 = 15
x4 = 5
y4 = 5
x5 = y
y5 = y
x6 = x
y6 = y
x7 = x
y7 = y

#game loop
run = True
while run:

  for joystick in joysticks:

    def AnalogueSticks(index):
       H = joystick.get_axis(index[0])
       H = np.around(H, decimals=3)

       W = joystick.get_axis(index[1])
       W = np.around(W, decimals=3)

       return (H, W)

    def CalcMovment(x, y, H, W):

      if abs(H) > 0.01:
         x += H * 0.5
         if x > 100:
            x = 100
         if x < 0:
            x = 0
      if abs(W) > 0.01:
         y += W * 0.5
         if y > 100:
            y = 100
         if y < 0:
            y = 0

      return (x, y, H, W)

    def CalcVectorMovment(x, y, H, W):
      x = 50 + H * 50
      if x > 100:
         x = 100
      if x < 0:
         x = 0

      y = 50 + W * 50
      if y > 100:
         y = 100
      if y < 0:
         y = 0

      return (x, y, H, W)

    def CalDigitAngle(x, y, input):
      x += input[0] * 0.5
      if x > 100:
         x = 100
      if x < 0:
         x = 0

      y -= input[1] * 0.5
      if y > 100:
         y = 100
      if y < 0:
         y = 0
      return (x, y)

    def NeckHeadFunc(x, y):
      hat = joystick.get_hat(0)
      neckhead = CalDigitAngle(x, y, hat)
      return (neckhead)

    def ChestPressFunc(x1, y1):
      # A button
      if joystick.get_button(0):
        y1 += 0.5
        if y1 > 100:
           y1 = 100
      # B button
      if joystick.get_button(1):
        x1 += 0.5
        if x1 > 100:
           x1 = 100
      # X button
      if joystick.get_button(2):
        x1 -= 0.5
        if x1 < 0:
           x1 = 0
      # Y button
      if joystick.get_button(3):
        y1 -= 0.5
        if y1 < 0:
           y1 = 0
      return (x1, y1)

    def LeftArmFunc(x2, y2):
      # Left Bumper
      if joystick.get_button(4):
        xy = AnalogueSticks([0, 1])
        xy = CalcMovment(x2, y2, xy[0], xy[1])
        return (xy)
      else:
        return (x2, y2)

    def RightArmFunc(x3, y3):
      # Right Bumper
      if joystick.get_button(5):
        xy = AnalogueSticks([3, 4])
        #print(xy)
        xy = CalcMovment(x3, y3, xy[0], xy[1])
        return (xy)
      else:
        return (x3, y3)

    def HandFunc(x4, y4):
      xy = AnalogueSticks([2, 5])
      xy = CalcVectorMovment(x4, y4, xy[0], xy[1])
      return (xy)

    def MecanumWheelsMoveFunc(x6, y6):
      #Left Bumper
      if not joystick.get_button(4):
        xy = AnalogueSticks([0, 1])
        xy = CalcVectorMovment(x6, y6, xy[0], xy[1])
        return (xy)
      else:
        xy = AnalogueSticks([0, 1])
        return (x6, y6, xy)

    def MecanumWheelsRotateFunc(x7, y7):
      #Right Bumper
      if not joystick.get_button(5):
        xy = AnalogueSticks([2, 3])
        xy = CalcVectorMovment(x7, y7, xy[0], xy[1])
        return (xy)
      else:
        xy = AnalogueSticks([2, 3])
        return (x7, y7, xy)

    #HomePos
    if joystick.get_button(10):
      adamController.return_to_start_position()

    #main
    xy = NeckHeadFunc(x, y)
    #print("NeckHead:", xy)
    x = xy[0]
    y = xy[1]

    xy = ChestPressFunc(x1, y1)
    #print("ChestPress:", xy)
    x1 = xy[0]
    y1 = xy[1]

    xy = LeftArmFunc(x2, y2)
    #print("LeftArm:", xy)
    x2 = xy[0]
    y2 = xy[1]

    xy = RightArmFunc(x3, y3)
    #print("RightArm:", xy)
    x3 = xy[0]
    y3 = xy[1]

    xy = HandFunc(x4, y4)
    #print("HandFunc:", xy)
    x4 = xy[0]
    y4 = xy[1]

    xy = MecanumWheelsMoveFunc(x6, y6)
    #print("MecanumWheelsMove:", xy)
    x6 = xy[0]
    y6 = xy[1]

    xy = MecanumWheelsRotateFunc(x7, y7)
    #print("MecanumWheelsRotate:", xy)
    x7 = xy[0]
    y7 = xy[1]

    adamController.move((x6, y6), x7)
    adamController.handle_command(commands=SerializableCommands([MotorCommand('neck', x), MotorCommand('head', y),
                                                                 MotorCommand('chest', x1), MotorCommand('press', y1),
                                                                 MotorCommand('left_hand', x4), MotorCommand('right_hand', y4),
                                                                 MotorCommand('left_upper_arm', x2), MotorCommand('right_upper_arm', x3),
                                                                 MotorCommand('left_shoulder', y2), MotorCommand('right_shoulder', y3)]))

      #event handler
  for event in pygame.event.get():
    if event.type == pygame.JOYDEVICEADDED:
      joy = pygame.joystick.Joystick(event.device_index)
      joysticks.append(joy)