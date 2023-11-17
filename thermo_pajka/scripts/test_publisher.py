#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

if __name__ == '__main__':
    rospy.init_node('transmitter')
    pub=rospy.Publisher("/thermo_data", String, queue_size=10)
    rate=rospy.Rate(2)

    while not rospy.is_shutdown():
        msg=String()
        msg.data="hello there"
        pub.publish(msg)
        rate.sleep()

rospy.loginfo("Publisher stopped")