#!/usr/bin/env python
import rospy
import cv2
from apriltags.msg import AprilTagDetections
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

import pdb

class AprilTagMarker:

  def __init__(self):
    
    # Initialize image converter
    self.bridge = CvBridge()
    
    # Initialize raw image subscriber
    self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.imageCb)
    self.image = []

    # Initialize april tag publisher
    self.marker_pub = rospy.Publisher("/marked_april_tag", Image, queue_size = 1)
    self.marked_image = []
    self.pub_image = 0

    # Initialize detection subscriber
    self.detection_sub = rospy.Subscriber("/apriltags/detections",AprilTagDetections,self.detectionCb)
    self.detection_result = AprilTagDetections()

  # Grab detection result, published from apriltag identifier
  def detectionCb(self,data):
    self.detection_result = data

  # Grab image and convert from Image message to openCV image
  def imageCb(self,data):
    try:
      self.image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

  # Publish modified ariltag image
  def publishImage(self):
    try:
      self.marker_pub.publish(self.bridge.cv2_to_imgmsg(self.image, "bgr8"))
    except CvBridgeError as e:
      print(e)    

  # Draw marker on the center of the apriltag
  def drawMarker(self):

    if len(self.detection_result.detections) == 0:
      return -1
    
    ########################
    ### INSERT CODE HERE ###
    ########################

    self.publishImage()



if __name__ == '__main__':

  # Init Node
  rospy.init_node('AprilTagMarker')
  # Initialize april tag class
  marker = AprilTagMarker()
  
  # Spin ROS
  rate = rospy.Rate(120) #hz
  while not rospy.is_shutdown():
    marker.drawMarker()
    rate.sleep()
