#!/usr/bin/env python3

import rclpy
import random
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from scipy.spatial.transform import Rotation as R

class ObstacleAvoider(Node):

    def __init__(self):
        super().__init__('obstacle_avoider')

        self.publisher_ = self.create_publisher(Twist, '/model/vehicle/cmd_vel', 10)
        self.subscription = self.create_subscription(
            Odometry, '/model/vehicle/odometry',
            self.odom_callback,
            10
        )

        self.pose = None
        self.timer = self.create_timer(0.05, self.control_loop)

        self.turning = False
        self.turn_time = 0

    from scipy.spatial.transform import Rotation as R

    def odom_callback(self, msg):
        if self.pose is None:
            self.get_logger().info("Robot READY 🚀")

        self.pose = msg.pose.pose

        orientation_q = self.pose.orientation

        rot = R.from_quat([
            orientation_q.x,
            orientation_q.y,
            orientation_q.z,
            orientation_q.w
        ])

        _, _, self.yaw = rot.as_euler('xyz')

    def control_loop(self):
        if self.pose is None:
            return

        msg = Twist()

        x = self.pose.position.x
        y = self.pose.position.y

        self.get_logger().info(f"x={x:.2f}, y={y:.2f}")

        near_wall = (
            x > 5.0 or x < -5.0 or
            y > 5.0 or y < -5.0
        )

        if near_wall:
            center_x, center_y = 0.0, 0.0
            dx = center_x - x
            dy = center_y - y

            target_angle = math.atan2(dy, dx)

            angle_error = target_angle - self.yaw
            angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))

            msg.linear.x = 1.0
            msg.angular.z = max(min(2.0 * angle_error, 2.0), -2.0)

            self.get_logger().info("Avoiding wall")

        else:
            msg.linear.x = 4.0
            msg.angular.z = 0.1

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