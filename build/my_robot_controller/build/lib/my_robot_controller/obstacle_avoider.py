#!/usr/bin/env python3

import rclpy
import random
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class ObstacleAvoider(Node):

    def __init__(self):
        super().__init__('obstacle_avoider')

        self.publisher_ = self.create_publisher(Twist, '/model/vehicle/cmd_vel', 10)
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        self.pose = None
        self.timer = self.create_timer(0.5, self.control_loop)

        self.turning = False
        self.turn_time = 0

    def pose_callback(self, msg):
        self.pose = msg

    def control_loop(self):
        if self.pose is None:
            return

        msg = Twist()

        # Detect wall
        near_wall = (
            self.pose.x > 9.0 or self.pose.x < 2.0 or
            self.pose.y > 9.0 or self.pose.y < 2.0
        )

        # STATE: AVOID WALL
        if near_wall:
            center_x, center_y = 5.5, 5.5
            dx = center_x - self.pose.x
            dy = center_y - self.pose.y

            target_theta = math.atan2(dy, dx)
            angle_diff = target_theta - self.pose.theta
            angle_diff = math.atan2(math.sin(angle_diff), math.cos(angle_diff))

            msg.linear.x = 1.5
            msg.angular.z = 2.0 * angle_diff

            self.get_logger().info("Avoiding wall")

        # STATE: EXPLORE        
        else:
            msg.linear.x = 2.0
            msg.angular.z = max(min(msg.angular.z, 2.0), -2.0)

            self.get_logger().info("Exploring")

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoider()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()