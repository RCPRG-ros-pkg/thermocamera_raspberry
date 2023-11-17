#!/bin/bash -e

cd $home
source /opt/ros/melodic/setup.bash
source /home/pi/pajka_ws/devel/setup.bash
export ROS_MASTER_URI="http://192.168.18.66:11311" 
export ROS_IP=`ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'
#export ROS_MASTER_URI=http://arp@arp-GF63-8RC:11311
#export ROS_HOSTNAME=raspberrypi

if rostopic list | grep "/rosout" &> /dev/null;
then
  roslaunch thermo_pajka thermo_pajka.launch
  exit 0
fi
exit 0
