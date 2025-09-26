from setuptools import setup

package_name = "ros_reb1"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    package_dir={package_name: "ros_reb1"},
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/ros_reb1"]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools", "psutil", "reb1"],
    zip_safe=True,
    maintainer="Alex Doe",
    maintainer_email="alex@example.com",
    description="ROS 2 node for REB-1 power logging",
    license="MIT",
    entry_points={
        "console_scripts": ["power_logger_node = ros_reb1.power_logger_node:main"],
    },
)
