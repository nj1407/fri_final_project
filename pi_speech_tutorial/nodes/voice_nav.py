#!/usr/bin/env python

"""
  voice_nav.py allows controlling a mobile base using simple speech commands.
  Based on the voice_cmd_vel.py script by Michael Ferguson in the pocketsphinx ROS package.
"""
import roslib
roslib.load_manifest('move_base')
import roslib; roslib.load_manifest('pi_speech_tutorial')
import rospy
import math
import collections
import actionlib
import tf
import re
import move_base_msgs.msg
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseArray

from geometry_msgs.msg import Twist
from std_msgs.msg import String
from math import copysign

goalQueue = collections.deque()
quaternionleft = tf.transformations.quaternion_from_euler(0,0,1.5708)
quaternionright = tf.transformations.quaternion_from_euler(0,0,-1.5708)
quaternionforward = tf.transformations.quaternion_from_euler(0,0,0)
quaternionbackward = tf.transformations.quaternion_from_euler(0,0,0)
#partydance = 0
publed = rospy.Publisher('five', String, queue_size=10)

class voice_cmd_vel:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        rospy.Subscriber('recognizer/output', String, self.speechCb)

        #self.max_speed = rospy.get_param("~max_speed", 0.4)
        #self.max_angular_speed = rospy.get_param("~max_angular_speed", 1.5)
        #self.speed = 3.0
        #self.angular_speed = rospy.get_param("~start_angular_speed", 0.5)
        
        #self.rate = rospy.get_param("~rate", 5)
        #self.rate = 5.0
        #r = rospy.Rate(self.rate)
        #self.paused = False

        # A mapping from keywords to commands.
        self.keywords_to_command = {'stop': ['stop'],
                                    'forward': ['forward'],
                                    'backward': ['backward'],
                                    'turn left': ['turn left'],
                                    'turn right': ['turn right'],
				    'dance': ['dance'],
				    'party': ['party']}

        

        rospy.loginfo("Ready to receive voice commands")

    def get_command(self, data):
        for (command, keywords) in self.keywords_to_command.iteritems():
            for word in keywords:
                if data.find(word) > -1:
                    return command
        
    def speechCb(self, msg):        
        command = self.get_command(msg.data)
        rospy.loginfo("Command: " + str(command))

        # Initialize the Twist message we will publish.
        goal = MoveBaseGoal()
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.header.frame_id = "/base_link"

        if command == 'forward':
            goal.target_pose.pose.position.x = 1.0
	    goal.target_pose.pose.orientation.x = quaternionforward[0]
	    goal.target_pose.pose.orientation.y = quaternionforward[1]
	    goal.target_pose.pose.orientation.z = quaternionforward[2]
	    goal.target_pose.pose.orientation.w = quaternionforward[3]
	    #if partydance == 0:
	    publed.publish("m")
            
        elif command == 'turn left':
            goal.target_pose.pose.orientation.x = quaternionleft[0]
	    goal.target_pose.pose.orientation.y = quaternionleft[1]
	    goal.target_pose.pose.orientation.z = quaternionleft[2]
	    goal.target_pose.pose.orientation.w = quaternionleft[3]
	    #if partydance == 0:
	    publed.publish("m")
                
        elif command == 'turn right':    
            goal.target_pose.pose.orientation.x = quaternionright[0]
	    goal.target_pose.pose.orientation.y = quaternionright[1]
	    goal.target_pose.pose.orientation.z = quaternionright[2]
	    goal.target_pose.pose.orientation.w = quaternionright[3]
	    #if partydance == 0:
	    publed.publish("m") 
                
        elif command == 'backward':
            goal.target_pose.pose.position.x = -1.0
            goal.target_pose.pose.orientation.x = quaternionbackward[0]
	    goal.target_pose.pose.orientation.y = quaternionbackward[1]
	    goal.target_pose.pose.orientation.z = quaternionbackward[2]
	    goal.target_pose.pose.orientation.w = quaternionbackward[3]
	    #if partydance == 0:
	    publed.publish("m")

        elif command == 'stop': 
            goalQueue.clear()

	elif command == 'dance':
	    #partydance = 1
	    publed.publish("d")
	    self.speechCb(String("forward"))
	    self.speechCb(String("backward"))
	    self.speechCb(String("forward"))
	    self.speechCb(String("turn right"))
	    self.speechCb(String("turn left"))
	    self.speechCb(String("turn left"))
    	    self.speechCb(String("turn left"))
	    self.speechCb(String("turn left"))
	    self.speechCb(String("turn left"))
	    #partydance = 0

	elif command == 'party':
	   # partydance = 1
	    publed.publish("p")
	    for i in xrange(0,20):
		self.speechCb(String("turn right"))
	    #partydance = 0

        else:
            rospy.loginfo("Command not recognized")
	    publed.publish("w")
            return

        goalQueue.append(goal)

    def cleanup(self):
        goalQueue.clear()

if __name__=="__main__":
    rospy.init_node('voice_nav')
    try:
        voice_cmd_vel()
        client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        client.wait_for_server()
        # We have to keep publishing the move_base message if we want the robot to keep moving.
        while not rospy.is_shutdown():
            try:
                if len(goalQueue) == 0:
		    publed.publish("i")
                    continue
                g = goalQueue.popleft()
                client.send_goal(g)
                client.wait_for_result(rospy.Duration.from_sec(2.0))
            except IndexError:
                pass
    except rospy.ROSInterruptException:
        pass

