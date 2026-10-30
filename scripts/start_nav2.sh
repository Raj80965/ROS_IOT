#!/usr/bin/env bash
export DISPLAY=:0
export WAYLAND_DISPLAY=wayland-0
export XDG_RUNTIME_DIR=/run/user/$(id -u)
export QT_QPA_PLATFORM=xcb
source /opt/ros/jazzy/setup.bash
# Support both burger and waffle
export TURTLEBOT3_MODEL="${TURTLEBOT3_MODEL:-burger}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"

MAP_PATH="$WORKSPACE_DIR/maps/map.yaml"
if [ "$TURTLEBOT3_MODEL" = "waffle" ]; then
    PARAMS_PATH="$WORKSPACE_DIR/params/waffle_params.yaml"
else
    PARAMS_PATH="$WORKSPACE_DIR/params/nav2_params.yaml"
fi
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

sleep 4
echo "[INFO] Launching RViz2..."
LIBGL_ALWAYS_SOFTWARE=1 ros2 run rviz2 rviz2 -d "$RVIZ_PATH" --ros-args -p use_sim_time:=True

wait $NAV2_PID
