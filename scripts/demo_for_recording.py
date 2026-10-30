#!/usr/bin/env python3
"""
Automated Demonstration Script for Screen Recording
Provides a 5-second countdown to let the user start recording,
then navigates the robot across obstacles to the goal.
"""

import time
import sys
import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


def main():
    print("\n=======================================================")
    print("      TURTLEBOT3 AUTONOMOUS NAVIGATION DEMO            ")
    print("=======================================================")
    print("Get your screen recorder ready (Win + Alt + R)!")
    print("Starting in:")
    for count in range(5, 0, -1):
        print(f"  --> {count} seconds...")
        time.sleep(1)

    print("\n[INFO] Initializing ROS 2 and Nav2 BasicNavigator...")
    rclpy.init()
    navigator = BasicNavigator()

    print("[INFO] Checking Nav2 stack status...")
    navigator.waitUntilNav2Active()
    print("[INFO] Nav2 is active and ready for navigation!")

    # Set navigation goal past obstacles
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose.pose.position.x = 1.5
    goal_pose.pose.position.y = 0.5
    goal_pose.pose.position.z = 0.0
    goal_pose.pose.orientation.w = 1.0

    print(f"\n[ACTION] Sending Navigation Goal: (x=1.5, y=0.5) across the obstacle field...")
    navigator.goToPose(goal_pose)

    start_time = time.time()
    i = 0
    while not navigator.isTaskComplete():
        i += 1
        feedback = navigator.getFeedback()
        if feedback and i % 4 == 0:
            elapsed = int(time.time() - start_time)
            print(
                f"  [STATUS] Distance Remaining: {feedback.distance_remaining:.2f} m | "
                f"Elapsed Time: {elapsed} s"
            )
        time.sleep(0.5)

    result = navigator.getResult()
    print("\n=======================================================")
    if result == TaskResult.SUCCEEDED:
        total_time = int(time.time() - start_time)
        print(f"  >>> SUCCESS: Goal reached in {total_time} seconds! <<<")
        print("  >>> Autonomous Navigation & Obstacle Avoidance Verified! <<<")
    else:
        print("  >>> Navigation completed with status:", result)
    print("=======================================================")
    print("You can now STOP your screen recording!\n")

    rclpy.shutdown()


if __name__ == '__main__':
    main()
