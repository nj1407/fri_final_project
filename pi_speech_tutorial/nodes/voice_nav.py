#!/usr/bin/env python

"""
  voice_nav.py allows controlling a mobile base using simple speech commands.
  Based on the voice_cmd_vel.py script by Michael Ferguson in the pocketsphinx ROS package.
"""

import roslib; roslib.load_manifest('pi_speech_tutorial')
import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import String
from math import copysign

class voice_cmd_vel:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        self.max_speed = rospy.get_param("~max_speed", 0.4)
        self.max_angular_speed = rospy.get_param("~max_angular_speed", 1.5)
        self.speed = rospy.get_param("~start_speed", 0.1)
        self.angular_speed = rospy.get_param("~start_angular_speed", 0.5)
        self.linear_increment = rospy.get_param("~linear_increment", 0.05)
        self.angular_increment = rospy.get_param("~angular_increment", 0.4)
        self.rate = rospy.get_param("~rate", 5)
        r = rospy.Rate(self.rate)
        self.paused = False
        
        # Initialize the Twist message we will publish.
        self.msg = Twist()

        # Publish the Twist message to the cmd_vel topic
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)
        
        # Subscribe to the /recognizer/output topic to receive voice commands.
        rospy.Subscriber('/recognizer/output', String, self.speechCb)
        
       # A mapping from keywords to commands.
        self.keywords_to_command = {'stop': ['stop'],
                                    'forward': ['forward'],
                                    'backward': ['backward'],
                                    'turn left': ['turn left'],
                                    'turn right': ['turn right']}
        
        rospy.loginfo("Ready to receive voice commands")
        
        # We have to keep publishing the cmd_vel message if we want the robot to keep moving.
        while not rospy.is_shutdown():
            self.cmd_vel_pub.publish(self.msg)
            r.sleep()                       
            
    def get_command(self, data):
        for (command, keywords) in self.keywords_to_command.iteritems():
            for word in keywords:
                if data.find(word) > -1:
                    return command
        
    def speechCb(self, msg):        
        command = self.get_command(msg.data)
        
        rospy.loginfo("Command: " + str(command))
        
        if command == 'forward':    
            self.msg.linear.x = self.speed
            self.msg.angular.z = 0
            
        elif command == 'turn left':
            if self.msg.linear.x != 0:
                self.msg.angular.z += self.angular_increment
            else:        
                self.msg.angular.z = self.angular_speed
                
        elif command == 'turn right':    
            if self.msg.linear.x != 0:
                self.msg.angular.z -= self.angular_increment
            else:        
                self.msg.angular.z = -self.angular_speed
                
        elif command == 'backward':
            self.msg.linear.x = -self.speed
            self.msg.angular.z = 0
                
        else:
            return

        self.msg.linear.x = min(self.max_speed, max(-self.max_speed, self.msg.linear.x))
        self.msg.angular.z = min(self.max_angular_speed, max(-self.max_angular_speed, self.msg.angular.z))

    def cleanup(self):
        # When shutting down be sure to stop the robot!  Publish a Twist message consisting of all zeros.
        twist = Twist()
        self.cmd_vel_pub.publish(twist)

if __name__=="__main__":
    rospy.init_node('voice_nav')
    try:
        voice_cmd_vel()
    except:
        pass

