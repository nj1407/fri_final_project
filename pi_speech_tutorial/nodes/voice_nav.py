#!/usr/bin/env python

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
#global queue declaration
goalQueue = collections.deque()
#predefined quaternions for the movement commands so that they don't have to be recomputed within every iteration of speechCb 
quaternionleft = tf.transformations.quaternion_from_euler(0,0,1.5708)
quaternionright = tf.transformations.quaternion_from_euler(0,0,-1.5708)
quaternionforward = tf.transformations.quaternion_from_euler(0,0,0)
quaternionbackward = tf.transformations.quaternion_from_euler(0,0,0)
#partydance = 0
#publisher for led states
publed = rospy.Publisher('five', String, queue_size=10)

class voice_cmd_vel:
    def __init__(self):
        #if shutdown, need to clean up loose ends
        rospy.on_shutdown(self.cleanup)
        #instantiate subscriber to receive strings from the voice recognizer
        rospy.Subscriber('recognizer/output', String, self.speechCb)

        #mapping from keywords to commands.
        self.keywords_to_command = {'stop': ['stop'],
                                    'forward': ['forward'],
                                    'backward': ['backward'],
                                    'turn left': ['turn left'],
                                    'turn right': ['turn right'],
                                    'dance': ['dance'],
                                    'party': ['party']}
                                    
        rospy.loginfo("Ready to receive voice commands")
    
    #method to extract command string from msg
    def get_command(self, data):
        for (command, keywords) in self.keywords_to_command.iteritems():
            for word in keywords:
                if data.find(word) > -1:
                    return command
    #this is called for every message
    def speechCb(self, msg):
        command = self.get_command(msg.data)
        rospy.loginfo("Command: " + str(command))

        #initialize move base goal
        goal = MoveBaseGoal()
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.header.frame_id = "/base_link"

        #series of if statements that modify the goal data and publish states for the leds
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
        
        #clears all goals in queue so that further movement halts
        elif command == 'stop': 
            goalQueue.clear()

        #similiar to the other commands but instead calls itself with a sequence of psuedo commands
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
        
        #similiar to dance but utilizes a for loop
        elif command == 'party':
           # partydance = 1
            publed.publish("p")
            for i in xrange(0,20):
                self.speechCb(String("turn right"))
            #partydance = 0

        #if command does not fit any of the previous, update led status and print to terminal
        else:
            rospy.loginfo("Command not recognized")
            publed.publish("w")
            return
        
        #only reaches here if command is recognized
        #adds the new goal to the goal queue
        goalQueue.append(goal)

    #clears goal queue
    def cleanup(self):
        goalQueue.clear()

if __name__=="__main__":
    #instantiate node
    rospy.init_node('voice_nav')
    try:
        voice_cmd_vel()
        #create action client for move base action
        client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        #wait until action client is created before proceeding
        client.wait_for_server()
        #continually loop throught this while running and pop goals off of the queue to execute
        while not rospy.is_shutdown():
            try:
                #if there are goals in the goal queue, pop them off and send them in the action client
                if len(goalQueue) == 0:
                    publed.publish("i")
                    continue
                g = goalQueue.popleft()
                client.send_goal(g)
                #wait until the last sent goal is completed
                client.wait_for_result(rospy.Duration.from_sec(2.0))
            except IndexError:
                pass
    except rospy.ROSInterruptException:
        pass
