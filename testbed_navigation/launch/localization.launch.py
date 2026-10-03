import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():

    testbed_nav_dir = get_package_share_directory('testbed_navigation')
    amcl_yaml_path = os.path.join(testbed_nav_dir, 'config', 'amcl_parms.yaml')

    map_loader_node = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
      os.path.join(testbed_nav_dir, 'launch', 'map_loader.launch.py'),
    )
  ) 
  
    amcl = Node(
        package = 'nav2_amcl',
        executable = 'amcl',
        name = 'amcl',
        output = 'screen',
        parameters = [amcl_yaml_path]
    )

    lifecycle_manager_node = Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'autostart': True,
                'node_names': [
                        'map_server',
                        'amcl'
                    ]
                }]
            )


    return LaunchDescription([
        map_loader_node,
        amcl,
        lifecycle_manager_node
    ])