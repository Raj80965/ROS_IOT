# Antropi Robotics - Robotics Software Intern Assignment Submission Answers

This document contains detailed, structured answers prepared for the [Antropi Robotics Assignment Submission Form](https://forms.gle/fNGujekjhSPfc4KQ6).

---

## 1. Approach & Technical Implementation

### Question: Describe your approach to setting up the robot simulation and configuring the Nav2 stack for autonomous navigation.

**Answer:**
> For this assignment, I designed an end-to-end autonomous navigation pipeline using **ROS 2 Jazzy**, **Gazebo Sim (Harmonic)**, and the **Navigation2 (Nav2)** stack for a **TurtleBot3 Burger** mobile robot in an obstacle-populated environment.
>
> 1. **Simulation Environment & Robot Model:**
>    - Deployed the TurtleBot3 Burger in the `turtlebot3_world` environment containing bounding perimeter walls and 9 distinct cylindrical obstacle columns.
>    - Configured the robot's sensor suite: a 360° 2D LiDAR (LDS-01) publishing to `/scan` at 5 Hz, wheel encoders publishing odometry to `/odom`, and Gazebo bridge interfaces (`ros_gz_bridge`) bridging sensor data and motor actuation (`/cmd_vel`) seamlessly into ROS 2.
>
> 2. **Localization (AMCL):**
>    - Integrated **Adaptive Monte Carlo Localization (AMCL)** using a pre-generated 2D occupancy grid map (`map.yaml`).
>    - Automated initial pose convergence by configuring `set_initial_pose: true` with spawn coordinates `(-2.0, -0.5, 0.0)` in the parameter profile, ensuring robust immediate particle filter convergence and continuous `map -> odom` transform broadcasting.
>
> 3. **Costmap Configuration & Layering:**
>    - Configured **Global Costmap** (size matching map bounds) with Static Layer (pre-built obstacles) and Inflation Layer to maintain safety clearance from static obstacles.
>    - Configured rolling **Local Costmap** (3m x 3m window centered on robot) with Obstacle Layer (real-time 2D laser scan integration via `Obstacle2D` sensor plugin) and Inflation Layer (`inflation_radius: 0.55m`, `cost_scaling_factor: 3.0`) for real-time dynamic obstacle detection and avoidance.
>
> 4. **Path Planning & Trajectory Control:**
>    - **Global Planner:** Used `nav2_navfn_planner::NavfnPlanner` (Dijkstra / A* heuristic) to compute the global shortest path through free space around obstacles.
>    - **Local Controller:** Deployed the Model Predictive Path Integral (**MPPI**) / **DWB** controller to compute optimal velocity commands (`geometry_msgs/msg/TwistStamped` on `/cmd_vel`) adhering to kinematic constraints (max velocity 0.22 m/s, angular velocity 2.84 rad/s) while avoiding local obstacles.
>    - **Behavior Recovery:** Incorporated `nav2_behaviors` (Spin, BackUp, Wait) to handle edge cases or tight corridors.

---

## 2. Key Challenges Faced & Engineering Solutions

### Question: What challenges did you encounter during the setup/configuration, and how did you resolve them?

**Answer:**
> During the setup and execution, I encountered three key engineering challenges:
>
> 1. **Time Synchronization & TF Lookup Latency (`use_sim_time`):**
>    - *Problem:* Initially, Nav2 nodes were operating with system wall time while Gazebo published simulated time via `/clock`. This resulted in TF lookup failures (`Lookup would require extrapolation into the future/past`), preventing AMCL from publishing transforms and holding Costmap layers in an uninitialized state.
>    - *Solution:* Ensured consistent propagation of `use_sim_time:=true` across all Nav2 lifecycle nodes, TF broadcasters, and RViz2. Configured launch parameters so that all components synchronize with Gazebo's simulation clock.
>
> 2. **Lifecycle State Machine Synchronization & Autostart Management:**
>    - *Problem:* Nav2 relies on managed lifecycle nodes (`map_server`, `amcl`, `controller_server`, `planner_server`). Manual state transitions clashed with Nav2's automated lifecycle manager, causing `No transition matching 1 found for current state active` errors.
>    - *Solution:* Leveraged Nav2's native `lifecycle_manager_navigation` with `autostart: true` and pre-configured AMCL initial pose parameters. This guarantees an orderly transition sequence (Unconfigured -> Inactive -> Active) without race conditions or manual interventions.
>
> 3. **WSL2 GUI & Hardware Acceleration (WSLg):**
>    - *Problem:* Running Gazebo Sim and RViz2 with 3D rendering inside WSL2 requires proper Wayland/X11 socket binding and GPU passthrough.
>    - *Solution:* Configured WSLg environment variables (`DISPLAY=:0`, `WAYLAND_DISPLAY=wayland-0`) and verified software/hardware rasterization to ensure smooth 60 FPS visualization of costmaps and laser scans without rendering crashes.

---

## 3. Key Learnings & Takeaways

### Question: What were your major learnings from this exercise?

**Answer:**
> 1. **Modular Navigation Architecture:** Gained a deep hands-on understanding of how modern ROS 2 Nav2 architecture separates concerns across Global Planners, Local Controllers, Costmap Layers, and Behavior Trees (BT Navigator).
> 2. **Dynamic Obstacle Avoidance Tuning:** Learned how costmap inflation parameters directly impact navigation behavior: balancing safety margins (`inflation_radius`) against narrow navigation passage accessibility.
> 3. **Lifecycle Management in ROS 2:** Understood the importance of deterministic node states (LifecycleNode transitions), ensuring that planning and execution only trigger when localization and sensor feeds are confirmed healthy.
> 4. **Robotics Development Lifecycle:** Experienced first-hand how simulation environments (Gazebo + RViz) allow rapid prototyping and validation of autonomous mobile robot (AMR) algorithms before deployment on physical hardware.
