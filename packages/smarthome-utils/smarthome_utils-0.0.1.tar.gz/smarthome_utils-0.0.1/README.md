# Smart Home Utils

A Python utility library for controlling and managing robot navigation in a smart home environment. This library provides sensor reading capabilities, movement controls, and debugging functions for robot navigation.

## Features

- Sensor data reading and processing
- Robot movement control functions
- Compass and orientation management
- Distance sensor handling
- GPS position tracking
- Debug output functionality
- Support for both U14 and U19 robot configurations

## Main Functions

### Sensor Reading

- `readSensorsU14()`: Reads sensor data for U14 configuration including:
  - Distance sensors (front, back, left, right, and diagonal positions)
  - Compass orientation
  - Room information and cleaning status

- `readSensorsU19()`: Reads sensor data for U19 configuration including:
  - Distance sensors in 8 directions
  - GPS position
  - Battery status
  - Compass orientation

### Movement Control

- `move(left, right)`: Controls robot movement by setting wheel velocities
- `turn(deg)`: Rotates the robot to a specific compass degree
- `compassCorrection(alpha)`: Ensures compass values stay within 0-360 degree range

### Debug Functions

- `debugU14()`: Displays detailed sensor information for U14 configuration
- `debugU19()`: Displays detailed sensor information for U19 configuration including:
  - Battery status
  - Distance readings
  - GPS coordinates
  - Compass heading
  - Time

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

## Usage

Import the utility module and use its functions to control the robot and read sensor data:

```python
from smarthome_utils import move, turn, readSensorsU14, debugU14

# Read sensor data
readSensorsU14()

# Move the robot
move(5, 5)  # Move forward
turn(90)    # Turn to 90 degrees

# Debug output
debugU14()
```