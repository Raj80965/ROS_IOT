import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    tb3_gazebo_dir = get_package_share_directory('turtlebot3_gazebo')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    # Default paths
    default_map_path = os.path.join(pkg_dir, 'maps', 'map.yaml')
    default_params_path = os.path.join(pkg_dir, 'params', 'nav2_params.yaml')
    default_rviz_path = os.path.join(pkg_dir, 'rviz', 'tb3_nav2.rviz')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    map_yaml_file = LaunchConfiguration('map', default=default_map_path)
    params_file = LaunchConfiguration('params_file', default=default_params_path)
    rviz_config_file = LaunchConfiguration('rviz_config', default=default_rviz_path)

    # 1. Gazebo Simulation with TurtleBot3 World
    gazebo_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(tb3_gazebo_dir, 'launch', 'turtlebot3_world.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    # 2. Nav2 Bringup (AMCL, Planner, Controller, Costmaps, Lifecycle)
    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': map_yaml_file,
            'use_sim_time': use_sim_time,
            'params_file': params_file,
            'autostart': 'true',
        }.items()
    )

    # 3. RViz2 Visualization
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock'
        ),
        DeclareLaunchArgument(
            'map',
            default_value=default_map_path,
            description='Full path to map yaml file to load'
        ),
        DeclareLaunchArgument(
            'params_file',
            default_value=default_params_path,
            description='Full path to Nav2 parameter yaml file'
        ),
        DeclareLaunchArgument(
            'rviz_config',
            default_value=default_rviz_path,
            description='Full path to RViz configuration file'
        ),
        gazebo_sim,
        nav2_bringup,
        rviz_node
    ])
