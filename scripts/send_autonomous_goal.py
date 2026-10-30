#!/usr/bin/env python3
"""
Autonomous Navigation Goal Script for TurtleBot3
Demonstrates autonomous navigation to a goal while avoiding obstacles.
Uses the Nav2 Simple Commander API.
"""

import time
import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


def main():
    rclpy.init()
    navigator = BasicNavigator()

    print("[INFO] Waiting for Nav2 stack to become active...")
    navigator.waitUntilNav2Active()
    print("[INFO] Nav2 is active and ready!")

    # Define the target navigation goal
    # In turtlebot3_world, robot starts at (-2.0, -0.5).
    # Goal pose on the opposite side past obstacles: (1.5, 0.5)
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose.pose.position.x = 1.5
    goal_pose.pose.position.y = 0.5
    goal_pose.pose.position.z = 0.0
    goal_pose.pose.orientation.x = 0.0
    goal_pose.pose.orientation.y = 0.0
    goal_pose.pose.orientation.z = 0.0
    goal_pose.pose.orientation.w = 1.0

    print(f"[INFO] Sending navigation goal: x={goal_pose.pose.position.x}, y={goal_pose.pose.position.y}...")
    navigator.goToPose(goal_pose)

    # Monitor progress
    i = 0
    while not navigator.isTaskComplete():
        i += 1
        feedback = navigator.getFeedback()
        if feedback and i % 5 == 0:
            print(
                f"[NAVIGATION] Distance remaining: {feedback.distance_remaining:.2f} m | "
                f"Navigation time: {feedback.navigation_time.sec} s"
            )
        time.sleep(0.5)

    # Check result
    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print("[SUCCESS] Goal successfully reached! Autonomous navigation completed.")
    elif result == TaskResult.CANCELED:
        print("[WARNING] Goal was canceled.")
    elif result == TaskResult.FAILED:
        print("[ERROR] Goal failed.")
    else:
        print("[ERROR] Goal returned invalid status.")

    navigator.lifecycleShutdown()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
