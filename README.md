# Autonomous Exploration Robot (ROS 2)

## Overview
This project implements an autonomous agent using ROS 2 that explores a 2D environment and avoids boundaries using feedback control and state-based behavior.

## Features
- ROS 2 Python node (rclpy)
- Autonomous exploration with random motion
- Wall avoidance using position feedback
- Smooth motion control (no jitter)
- State-based behavior:
  - Explore mode
  - Avoid mode

## Architecture

Sense → Think → Act loop:

- Sense: `/turtle1/pose`
- Think: decision logic (explore vs avoid)
- Act: `/turtle1/cmd_vel`

## Behavior

### Explore Mode
- Moves forward
- Applies small random turning

### Avoid Mode
- Detects boundary proximity
- Rotates toward safe direction
- Moves away from wall

## How to Run

```bash
ros2 run turtlesim turtlesim_node
ros2 run my_robot_controller simple_node
