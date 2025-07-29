# --------------------------------------------------------------#
# BASE CODE
# --------------------------------------------------------------#
import json
from controller import Robot
# --------------------------------------------------------------#
# GLOBALS

#both
Compass = 0
#U14
Front = 0
FrontLeft = 0
FrontRight = 0
Back = 0
BackLeft = 0
BackRight = 0
Left = 0
Right = 0
CurrentRoom = ""
Rooms = dict()
US_Front = 0
US_Left = 0
US_Right = 0
#U19
PositionX = 0
PositionY = 0
Front = 0 
ForntLeft = 0
Back = 0
BackLeft = 0
Back = 0
BackRight = 0
Right =  0
FrontRight = 0

# --------------------------------------------------------------#
# INIT
robot = Robot()  # Create robot object
timeStep = int(robot.getBasicTimeStep())
maxSpeed = 6.28

wheel_left = robot.getDevice("wheel1 motor")
wheel_left.setPosition(float('inf'))

wheel_right = robot.getDevice("wheel2 motor")
wheel_right.setPosition(float('inf'))

distanceSensor1 = robot.getDevice("D1")
distanceSensor1.enable(timeStep)

distanceSensor2 = robot.getDevice("D2")
distanceSensor2.enable(timeStep)

distanceSensor3 = robot.getDevice("D3")
distanceSensor3.enable(timeStep)

distanceSensor4 = robot.getDevice("D4")
distanceSensor4.enable(timeStep)

distanceSensor5 = robot.getDevice("D5")
distanceSensor5.enable(timeStep)

distanceSensor6 = robot.getDevice("D6")
distanceSensor6.enable(timeStep)

distanceSensor7 = robot.getDevice("D7")
distanceSensor7.enable(timeStep)

distanceSensor8 = robot.getDevice("D8")
distanceSensor8.enable(timeStep)

gpsSensor = robot.getDevice("gps") 
gpsSensor.enable(timeStep)

iuSensor = robot.getDevice("inertial_unit")
iuSensor.enable(timeStep)

receiver = robot.getDevice("receiver")
receiver.setChannel(1)
receiver.enable(timeStep)

# --------------------------------------------------------------#
# TEAM NAME
emitter = robot.getDevice("emitter")
emitter.setChannel(1)
emitter.send('set team name'.encode('utf-8'))

# ---------------------------------------------------------------------------------------------------------------#
# HELPER FUNCTIONS
def rad2deg(rad):
    return (rad / 3.14) * 180

def readSensorsU14():
    global Compass, Front, FrontLeft, Left, BackLeft, Back, BackRight, Right, FrontRight
    global US_Front, US_Left, US_Right
    global CurrentRoom, Rooms

    Compass = (rad2deg(iuSensor.getRollPitchYaw()[2]) + 360) % 360
    Front = int(distanceSensor1.getValue() * 10 * 32)
    FrontLeft = int(distanceSensor2.getValue() * 10 * 32)
    Left = int(distanceSensor3.getValue() * 10 * 32)
    BackLeft = int(distanceSensor4.getValue() * 10 * 32)
    Back = int(distanceSensor5.getValue() * 10 * 32)
    BackRight = int(distanceSensor6.getValue() * 10 * 32)
    Right = int(distanceSensor7.getValue() * 10 * 32)
    FrontRight = int(distanceSensor8.getValue() * 10 * 32)
    US_Front = Front
    US_Left = FrontLeft
    US_Right = FrontRight

    if receiver.getQueueLength() > 0:
        received_data = receiver.getString()
        if len(received_data) > 0:
            received_data = json.loads(received_data)
            CurrentRoom = received_data["current_room"]
            room_data = received_data["cleaning_percentage"]
            Rooms = {i['room']: int(float(i["percentage"]) * 100) for i in room_data}
        receiver.nextPacket()

def readSensorsU19():
    global Compass,PositionX,PositionY,FrontLeft,FrontRight,RightFront,RightBack,BackLeft,BackRight,LeftBack,LeftFront,le,re,Battery
    Compass =  (rad2deg(iuSensor.getRollPitchYaw()[2]) + 360 )% 360
    PositionX = gpsSensor.getValues()[0] * 100
    PositionY = gpsSensor.getValues()[2] * 100
    FrontLeft = int(distanceSensor1.getValue() * 10 * 32)
    FrontRight = int(distanceSensor8.getValue() * 10 * 32)
    RightFront = int(distanceSensor7.getValue() * 10 * 32)
    RightBack = int(distanceSensor6.getValue()* 10 * 32)
    BackLeft = int(distanceSensor3.getValue()* 10 * 32)
    BackRight = int(distanceSensor5.getValue()* 10  * 32)
    LeftBack = int(distanceSensor4.getValue() *10 * 32)
    LeftFront = int(distanceSensor2.getValue()*10 * 32)

    if receiver.getQueueLength() > 0:
        received_data = receiver.getString()
        if len(received_data) > 0:
            Battery = float(received_data)
        receiver.nextPacket()

def debugU14():
    global Compass, Front, FrontLeft, Back, BackLeft, Back, BackRight, Right, FrontRight
    print()
    print("---------------------------------------------", "cyan", )
    print("------------------- Debug -------------------", "cyan", )
    print("---------------------------------------------", "cyan", )
    print()
    print("------------------ Distance -----------------", "yellow", )
    print("                       Front: " + str(Front), "yellow")
    print("        FrontLeft: " + str(FrontLeft) + "                 FrontRight: " + str(FrontRight), "yellow")
    print("Left: " + str(Left) + "                                             Right: " + str(Right), "yellow")
    print("        BackLeft: " + str(BackLeft) + "                   BackRight: " + str(BackRight), "yellow")
    print("                       Back: " + str(Back), "yellow")
    print("------------------- Compass -----------------", "yellow", )
    print("Compass: " + str("%.0f " % Compass), "yellow")
    print("Current Room: " + CurrentRoom, "yellow")
    print("Rooms: " + str.join(", ", map(lambda key: f'{key}: {Rooms[key]}', Rooms.keys())), "yellow")


def debugU19():
    global Compass, PositionX, PositionY, FrontLeft, FrontRight, RightFront, RightBack, BackLeft, BackRight, LeftBack, LeftFront, Battery
    print()
    print("---------------------------------------", "cyan", )
    print("------------------ Debug --------------", "cyan", )
    print("---------------------------------------", "cyan", )
    print()
    print("---------------- Battery -------------", "yellow", )
    print(Battery, "yellow", )
    print()
    print("---------------- Distance -------------", "yellow", )
    print("            FrontLeft: " + str(FrontLeft) + " , FrontRight: " + str(FrontRight), "yellow")
    print("LeftFront: " + str(LeftFront) + "                            RightFront: " + str(RightFront), "yellow")
    print("LeftBack:  " + str(LeftBack) + "                             RightBack:  " + str(RightBack), "yellow")
    print("            BackLeft: " + str(BackLeft) + " ,  BackRight:  " + str(BackRight), "yellow")
    print("-----------------  GPS  ---------------", "cyan")
    print("X: " + str("%.2f " % PositionX) + "           Y: " + str("%.2f " % PositionY), "blue")
    print("----------------- Compass -------------", "yellow")
    print("Compass: " + str("%.0f " % Compass), "yellow")
    print("------------------ Time ---------------", "yellow")
    print("Time: " + str(robot.getTime()), "yellow")

#Move with velocity (left, right)
def move(left, right):
    wheel_left.setVelocity(left * maxSpeed / 10)
    wheel_right.setVelocity(right * maxSpeed / 10)

# 0 < Compass < 360
def compassCorrection(alpha):
    if alpha > 360:
        alpha = alpha - 360
    if alpha < 0:
        alpha = alpha + 360
    return alpha

#turn to compass deg
def turn(deg):
    global Compass
    mindeg = deg - 2
    maxdeg = deg + 2

    mindeg = compassCorrection(mindeg)
    maxdeg = compassCorrection(maxdeg)

    if(mindeg < maxdeg ):
        if(mindeg < Compass and Compass < maxdeg):
            return True
    else:
        if(Compass > mindeg or Compass < maxdeg):
            return True
    move(4, -4)
    
    return False






