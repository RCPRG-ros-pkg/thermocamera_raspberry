#!/usr/bin/env python3
import time
import board
import busio
import adafruit_mlx90640
import matplotlib.pyplot as plt
import numpy as np
import rospy
from thermocamera_msgs.msg import thermoinfo
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray
from itertools import islice


if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
    mlx = adafruit_mlx90640.MLX90640(i2c)
    print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])

    rospy.init_node('transmitter')
    pub=rospy.Publisher("/thermo_data", thermoinfo, queue_size=10)
    pub2=rospy.Publisher("/thermo_data2", Int32MultiArray, queue_size=10)

    rate=rospy.Rate(2)


    # if using higher refresh rates yields a 'too many retries' exception,
    # try decreasing this value to work with certain pi/camera combinations
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
    frame = [0] * 768
    newframe = [0] * 768 
    temp_list = []
    index = 1
    message = "0"
    while not rospy.is_shutdown():
        try:
            mlx.getFrame(frame)
        except ValueError:
            # these happen, no biggie - retry
            continue
        #for h in range(24):
        #    temp = []
        #    for w in range(32):
        #        t = frame[h*32 + w]
        #        temp.append(t)
        #    temp_list.append(temp)
        print("Numer obrazu ", index)
        index = index + 1
        max_temp = frame[0]
        min_temp = max_temp
        msg = thermoinfo()
        msg.tempf = frame
        for h in range(len(frame)):
            if frame[h] > max_temp:
                max_temp = frame[h]
                msg.highest_temp = max_temp
                msg.highest_temp_id = h
            elif frame[h] < min_temp:
                min_temp = frame[h]
                msg.lowest_temp = min_temp
                msg.lowest_temp_id = h
        przedzial = max_temp - min_temp
        delta = przedzial/256
        newframe = np.array(frame)
        newframe = newframe - min_temp
        newframe = newframe*255/przedzial
        newframe = newframe.astype(int)
        msg.tempui = newframe
        msg2 = Int32MultiArray()
        msg2.data = newframe
        pub2.publish(msg2)
        msg.tempui = newframe
        print("Message is  ", msg2.data)

        
        print("Max temp and min temp is ", max_temp, " and ", min_temp)
        # if max_temp > 32:
        #     message = "1"
        # elif min_temp < 20:
        #     message = "-1"
        # else:
        #     message = "0"

        # msg=String()
        # msg.data=message
        pub.publish(msg)
        rate.sleep()
            
        #print("The new 2D list is: ", temp_list)
        #plt.imshow(temp_list, cmap='seismic', interpolation='nearest')
        #plt.show()
rospy.loginfo("Publisher stopped")
