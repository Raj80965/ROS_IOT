#!/usr/bin/env bash
# Start TurtleBot3 World in Gazebo Sim
source /opt/ros/jazzy/setup.bash
export TURTLEBOT3_MODEL="${TURTLEBOT3_MODEL:-burger}"

echo "[INFO] Starting Gazebo Simulation with TurtleBot3 $TURTLEBOT3_MODEL..."
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
