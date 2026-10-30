#!/usr/bin/env bash
# Start Nav2 Stack and RViz2 with simulation time and custom params
source /opt/ros/jazzy/setup.bash
export TURTLEBOT3_MODEL=burger

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"

MAP_PATH="$WORKSPACE_DIR/maps/map.yaml"
PARAMS_PATH="$WORKSPACE_DIR/params/nav2_params.yaml"
RVIZ_PATH="$WORKSPACE_DIR/rviz/tb3_nav2.rviz"

echo "[INFO] Starting Nav2 Stack with AMCL and RViz2..."
echo "[INFO] Map: $MAP_PATH"
echo "[INFO] Params: $PARAMS_PATH"

ros2 launch nav2_bringup bringup_launch.py \
    use_sim_time:=True \
    map:="$MAP_PATH" \
    params_file:="$PARAMS_PATH" \
    autostart:=True &

NAV2_PID=$!

sleep 3
echo "[INFO] Launching RViz2..."
ros2 run rviz2 rviz2 -d "$RVIZ_PATH" --ros-args -p use_sim_time:=True

wait $NAV2_PID
