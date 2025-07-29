"""
SmartHome Utils - U14Robot Module

This module provides a class for controlling the U14 robot in the SmartHome simulation environment.
It handles sensor readings, movement control, and room information.
"""

import json
from controller import Robot


class U14Robot:
    """
    A class to control the U14 robot in the SmartHome simulation environment.

    This class provides methods for reading sensor data, controlling robot movement,
    and interacting with the simulation environment. It encapsulates all the functionality
    needed to navigate the robot through a simulated home environment.

    Attributes:
        maxSpeed (float): Maximum speed constant for the robot's wheels (6.28 rad/s).
        Compass (float): Current compass heading in degrees (0-360).
        Front (int): Distance reading from the front sensor.
        FrontLeft (int): Distance reading from the front-left sensor.
        FrontRight (int): Distance reading from the front-right sensor.
        Back (int): Distance reading from the back sensor.
        BackLeft (int): Distance reading from the back-left sensor.
        BackRight (int): Distance reading from the back-right sensor.
        Left (int): Distance reading from the left sensor.
        Right (int): Distance reading from the right sensor.
        CurrentRoom (str): Name of the room the robot is currently in.
        Rooms (dict): Dictionary containing room names and their cleaning percentages.
    """

    maxSpeed = 6.28

    def __init__(self, team_name):
        """
        Initialize the U14Robot with sensors, motors, and communication devices.

        Sets up all the necessary components for the robot to function in the simulation,
        including distance sensors, wheel motors, GPS, inertial unit, and communication.

        Args:
            team_name (str): The name of the team using this robot, used for identification.
        """
        # Initialize sensor reading variables
        self.Compass = 0
        self.Front = 0
        self.FrontLeft = 0
        self.FrontRight = 0
        self.Back = 0
        self.BackLeft = 0
        self.BackRight = 0
        self.Left = 0
        self.Right = 0
        self.CurrentRoom = ""
        self.Rooms = dict()

        # Initialize robot and its components
        self.robot = Robot()  # Create robot object
        self.timeStep = int(self.robot.getBasicTimeStep())

        # Set up wheel motors
        self.wheel_left = self.robot.getDevice("wheel1 motor")
        self.wheel_left.setPosition(float('inf'))

        self.wheel_right = self.robot.getDevice("wheel2 motor")
        self.wheel_right.setPosition(float('inf'))

        # Set up distance sensors
        self.distanceSensor1 = self.robot.getDevice("D1")
        self.distanceSensor1.enable(self.timeStep)

        self.distanceSensor2 = self.robot.getDevice("D2")
        self.distanceSensor2.enable(self.timeStep)

        self.distanceSensor3 = self.robot.getDevice("D3")
        self.distanceSensor3.enable(self.timeStep)

        self.distanceSensor4 = self.robot.getDevice("D4")
        self.distanceSensor4.enable(self.timeStep)

        self.distanceSensor5 = self.robot.getDevice("D5")
        self.distanceSensor5.enable(self.timeStep)

        self.distanceSensor6 = self.robot.getDevice("D6")
        self.distanceSensor6.enable(self.timeStep)

        self.distanceSensor7 = self.robot.getDevice("D7")
        self.distanceSensor7.enable(self.timeStep)

        self.distanceSensor8 = self.robot.getDevice("D8")
        self.distanceSensor8.enable(self.timeStep)

        # Set up GPS sensor
        self.gpsSensor = self.robot.getDevice("gps")
        self.gpsSensor.enable(self.timeStep)

        # Set up inertial unit (compass)
        self.iuSensor = self.robot.getDevice("inertial_unit")
        self.iuSensor.enable(self.timeStep)

        # Set up receiver for room information
        self.receiver = self.robot.getDevice("receiver")
        self.receiver.setChannel(1)
        self.receiver.enable(self.timeStep)

        self.team_name = team_name

        # Send team name to the simulation
        emitter = self.robot.getDevice("emitter")
        emitter.setChannel(1)
        emitter.send(self.team_name.encode('utf-8'))

    def step(self):
        """
        Advance the simulation by one time step and update sensor readings.

        This method performs two main functions:
        1. Advances the simulation by calling the robot's step method
        2. Updates all sensor readings by calling read_sensors()

        Returns:
            int: -1 if the simulation has ended, 0 otherwise
        """
        if self.robot.step(self.timeStep) == -1:
            return -1
        self.read_sensors()
        return 0

    @staticmethod
    def rad_to_deg(rad):
        """
        Convert radians to degrees.

        Args:
            rad (float): Angle in radians.

        Returns:
            float: Angle in degrees.
        """
        return (rad / 3.14) * 180

    def read_sensors(self):
        """
        Read and update all sensor values.

        Updates the robot's sensor readings including compass heading, distance sensors,
        and room information received from the simulation environment.
        """
        # Update compass and distance sensor readings
        self.Compass = (self.rad_to_deg(self.iuSensor.getRollPitchYaw()[2]) + 360) % 360
        self.Front = int(self.distanceSensor1.getValue() * 10 * 32)
        self.FrontLeft = int(self.distanceSensor2.getValue() * 10 * 32)
        self.Left = int(self.distanceSensor3.getValue() * 10 * 32)
        self.BackLeft = int(self.distanceSensor4.getValue() * 10 * 32)
        self.Back = int(self.distanceSensor5.getValue() * 10 * 32)
        self.BackRight = int(self.distanceSensor6.getValue() * 10 * 32)
        self.Right = int(self.distanceSensor7.getValue() * 10 * 32)
        self.FrontRight = int(self.distanceSensor8.getValue() * 10 * 32)

        # Process received data about rooms and cleaning status
        if self.receiver.getQueueLength() > 0:
            received_data = self.receiver.getString()
            if len(received_data) > 0:
                received_data = json.loads(received_data)
                self.CurrentRoom = received_data["current_room"]
                room_data = received_data["cleaning_percentage"]
                self.Rooms = {i['room']: int(float(i["percentage"]) * 100) for i in room_data}
            self.receiver.nextPacket()

    def debug_print(self):
        """
        Print debug information about the robot's current state.

        Displays formatted information about distance sensor readings, compass heading,
        current room, and cleaning percentages for all rooms.
        """
        print()
        print("---------------------------------------------")
        print("------------------- Debug -------------------")
        print("---------------------------------------------")
        print()
        print("------------------ Distance -----------------")
        print("                       Front: " + str(self.Front))
        print("        FrontLeft: " + str(self.FrontLeft) + "                 FrontRight: " + str(self.FrontRight))
        print("Left: " + str(self.Left) + "                                             Right: " + str(self.Right))
        print("        BackLeft: " + str(self.BackLeft) + "                   BackRight: " + str(self.BackRight))
        print("                       Back: " + str(self.Back))
        print("------------------- Compass -----------------")
        print("Compass: " + str("%.0f " % self.Compass))
        print("Current Room: " + self.CurrentRoom)
        print("Rooms: " + str.join(", ", map(lambda key: f'{key}: {self.Rooms[key]}', self.Rooms.keys())))

    def move(self, left, right):
        """
        Set the velocity of the robot's wheels.

        Args:
            left (float): Velocity for the left wheel (0-10 scale, will be converted to rad/s).
            right (float): Velocity for the right wheel (0-10 scale, will be converted to rad/s).
        """
        self.wheel_left.setVelocity(left * U14Robot.maxSpeed / 10)
        self.wheel_right.setVelocity(right * U14Robot.maxSpeed / 10)

    @staticmethod
    def compass_correction(alpha):
        """
        Normalize a compass angle to be within 0-360 degrees.

        Args:
            alpha (float): The angle to normalize.

        Returns:
            float: Normalized angle between 0 and 360 degrees.
        """
        if alpha > 360:
            alpha = alpha - 360
        if alpha < 0:
            alpha = alpha + 360
        return alpha

    def turn(self, deg):
        """
        Turn the robot to face a specific compass direction.

        This method attempts to turn the robot to face the specified compass direction.
        It returns True when the robot is facing within ±2 degrees of the target direction.

        Args:
            deg (float): Target compass direction in degrees (0-360).

        Returns:
            bool: True if the robot is facing the target direction (within ±2 degrees),
                 False otherwise.
        """
        min_deg = deg - 2
        max_deg = deg + 2

        min_deg = U14Robot.compass_correction(min_deg)
        max_deg = U14Robot.compass_correction(max_deg)

        if min_deg < max_deg:
            if min_deg < self.Compass < max_deg:
                return True
        else:
            if self.Compass > min_deg or self.Compass < max_deg:
                return True
        self.move(4, -4)

        return False
