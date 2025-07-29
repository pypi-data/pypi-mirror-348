# Smart Home Utils

A Python utility library for controlling and managing robot navigation in a smart home environment. This library provides sensor reading capabilities, movement controls, and debugging functions for robot navigation.

## Features

- Sensor data reading and processing
- Robot movement control functions
- Compass and orientation management
- Distance sensor handling
- GPS position tracking
- Debug output functionality
- Object-oriented interface for U14 robot control
- Support for both U14 and U19 robot configurations

## U14Robot Class

The package provides an object-oriented interface through the `U14Robot` class, which encapsulates all functionality needed to control a U14 robot:

```python
from smarthome_utils import U14Robot

# Initialize the robot with your team name
robot = U14Robot("Team Name")

# Read sensor data
robot.read_sensors()

# Move the robot
robot.move(5, 5)  # Move forward
robot.turn(90)    # Turn to 90 degrees

# Debug output
robot.debug_print()
```

### U14Robot Methods

- `__init__(team_name)`: Initialize the robot with your team name
- `read_sensors()`: Update all sensor readings
- `move(left, right)`: Control robot movement by setting wheel velocities
- `turn(deg)`: Rotate the robot to a specific compass degree
- `compass_correction(alpha)`: Ensure compass values stay within 0-360 degree range
- `debug_print()`: Display detailed sensor information
- `rad_to_deg(rad)`: Convert radians to degrees

## Legacy Functions (smarthome_utils module)

The package also includes the original procedural interface:

### Sensor Reading

- `readSensorsU14()`: Reads sensor data for U14 configuration
- `readSensorsU19()`: Reads sensor data for U19 configuration

### Movement Control

- `move(left, right)`: Controls robot movement by setting wheel velocities
- `turn(deg)`: Rotates the robot to a specific compass degree
- `compassCorrection(alpha)`: Ensures compass values stay within 0-360 degree range

### Debug Functions

- `debugU14()`: Displays detailed sensor information for U14 configuration
- `debugU19()`: Displays detailed sensor information for U19 configuration

## Dependencies

- `controller`: Robot control interface
- `json`: For data parsing

## Hardware Requirements

The library is designed to work with robots equipped with:
- 8 distance sensors (D1-D8)
- GPS sensor
- Inertial measurement unit
- Two wheel motors
- Communication devices (emitter and receiver)

## Usage Examples

### Object-Oriented Approach (Recommended)

```python
from smarthome_utils import U14Robot

# Initialize the robot
robot = U14Robot("Team Name")

# Main control loop
while robot.robot.step(robot.timeStep) != -1:
    # Read sensor data
    robot.read_sensors()

    # Example: Move forward if front is clear, otherwise turn
    if robot.Front > 100:
        robot.move(5, 5)  # Move forward
    else:
        robot.turn(90)    # Turn to 90 degrees

    # Print debug information
    robot.debug_print()
```