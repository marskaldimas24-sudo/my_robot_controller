# ROS2 Autonomous Robot Navigation (Gazebo)

## Overview
This project implements an autonomous mobile robot using ROS2 and Gazebo simulation.

The robot:
- Navigates autonomously
- Avoids boundaries
- Uses odometry feedback for control
- Applies heading-based steering logic

## Tech Stack
- ROS2 (Jazzy)
- Gazebo (Ignition)
- Python (rclpy)

## eatures
- Publisher: `/model/vehicle/cmd_vel`
- Subscriber: `/model/vehicle/odometry`
- Smooth motion using yaw-based control
- Boundary-aware navigation

## How to Run

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash

# Launch Gazebo
ros2 launch ros_gz_sim gz_sim.launch.py

# Spawn robot
ros2 run ros_gz_sim create -world empty \
-file /opt/ros/jazzy/share/ros_gz_sim_demos/models/vehicle/model.sdf

# Enable robot
gz topic -t /model/vehicle/enable -m gz.msgs.Boolean -p "data: true"

# Bridge topics
ros2 run ros_gz_bridge parameter_bridge \
/model/vehicle/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist

ros2 run ros_gz_bridge parameter_bridge \
/model/vehicle/odometry@nav_msgs/msg/Odometry@gz.msgs.Odometry

# Run controller
ros2 run my_robot_controller simple_node
