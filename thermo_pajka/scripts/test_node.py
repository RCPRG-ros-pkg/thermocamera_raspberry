#!/usr/bin/env/ python3

import rospy

if __name__ == '__main__':
    rospy.init_node('test_node')
    rospy.loginfo("Node started")
    rospy.sleep(1)
    rospy.loginfo("Node ended")