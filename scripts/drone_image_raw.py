#!/usr/bin/env python



# AirSim Python API
import setup_path 
import airsim

import rospy

# ROS Image message
from sensor_msgs.msg import Image

def airpub():
    pub = rospy.Publisher("airsim/image_raw", Image, queue_size=1)
    rospy.init_node('image_raw', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    # connect to the AirSim simulator 
    client = airsim.MultirotorClient()
    client.confirmConnection()

    while not rospy.is_shutdown():
        
        responses = client.simGetImages([
            airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)])

        for response in responses:
            img_rgba_string = response.image_data_uint8

        # Populate image message
        msg=Image() 
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "frameId"
        msg.encoding = "rgba8"
        msg.height = 360  
        msg.width = 640
        msg.data = img_rgba_string
        msg.is_bigendian = 0
        msg.step = msg.width * 4

        # log time and size of published image
        rospy.loginfo(len(response.image_data_uint8))
        # publish image message
        pub.publish(msg)
        # sleep until next cycle
        rate.sleep()


if __name__ == '__main__':
    try:
        airpub()
    except rospy.ROSInterruptException:
        pass
