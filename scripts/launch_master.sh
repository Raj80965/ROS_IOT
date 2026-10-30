#!/usr/bin/env bash
# Antropi Robotics Master Launch Script
# Launches Gazebo Sim (TurtleBot3 Waffle) + Nav2 Stack + 3D RViz2

export DISPLAY=:0
export WAYLAND_DISPLAY=wayland-0
export XDG_RUNTIME_DIR=/run/user/$(id -u)
export QT_QPA_PLATFORM=xcb
source /opt/ros/jazzy/setup.bash

# Sanitize model argument
MODEL_ARG="${1:-${TURTLEBOT3_MODEL:-burger}}"
export TURTLEBOT3_MODEL="$(echo "$MODEL_ARG" | tr -d "'\"[:space:]")"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"

MAP_PATH="$WORKSPACE_DIR/maps/map.yaml"
if [ "$TURTLEBOT3_MODEL" = "waffle" ]; then
    PARAMS_PATH="$WORKSPACE_DIR/params/waffle_params.yaml"
else
    PARAMS_PATH="$WORKSPACE_DIR/params/nav2_params.yaml"
fi
RVIZ_PATH="$WORKSPACE_DIR/rviz/tb3_nav2.rviz"

echo "=========================================================="
echo " Starting Gazebo Simulation with TurtleBot3 $TURTLEBOT3_MODEL..."
echo "=========================================================="
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py &
GAZEBO_PID=$!

echo "[INFO] Waiting 7 seconds for Gazebo Sim to initialize..."
sleep 7

echo "=========================================================="
echo " Starting Nav2 Stack (AMCL, Costmaps, Planners)..."
echo "=========================================================="
ros2 launch nav2_bringup bringup_launch.py \
    use_sim_time:=True \
    map:="$MAP_PATH" \
    params_file:="$PARAMS_PATH" \
    autostart:=True &
NAV2_PID=$!

echo "[INFO] Waiting 5 seconds for Nav2 nodes..."
sleep 5

echo "=========================================================="
echo " Launching 3D RViz2..."
echo "=========================================================="
LIBGL_ALWAYS_SOFTWARE=1 ros2 run rviz2 rviz2 -d "$RVIZ_PATH" --ros-args -p use_sim_time:=True &
RVIZ_PID=$!

echo "=========================================================="
echo " ALL SYSTEMS LIVE! READY FOR RECORDING & NAVIGATION!"
echo "=========================================================="

wait $GAZEBO_PID $NAV2_PID $RVIZ_PID
