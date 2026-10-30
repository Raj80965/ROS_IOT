@echo off
title TurtleBot3 Nav2 Master Launch
echo ==========================================================
echo Starting Gazebo Sim + Nav2 + RViz2 on your screen...
echo ==========================================================
wsl -d Ubuntu-24.04 bash -lc "cd '/mnt/c/Users/RAJ RAJGURU/OneDrive/Desktop/ROS_IOT' && bash scripts/launch_master.sh burger"
pause
