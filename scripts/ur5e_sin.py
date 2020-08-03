#!/usr/bin/env python

import rospy
import math
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import numpy as np

# cycles per seconds = RESOLUTION / FREQUENCY,
# 50 / 10 = 5 seconds per cycle.
RESOLUTION = 10  # number of points on 0 - 2pi
MULTIPLIER = 1.25
SHIFT = 0.0
FREQUENCY = 10
SECONDS_PER_MOVE = 1  # doesn't need to be accurate, will accelerate to catch up and smooth its movement

NODE_NAME = "ur5e_sin_publisher"
PUBLISHER = "/scaled_pos_joint_traj_controller/command"


RADIANS = np.linspace(0, 2 * math.pi, RESOLUTION)
JOINT_NAMES = ['elbow_joint', 'shoulder_lift_joint', 'shoulder_pan_joint',
               'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']


def launch():
    while not rospy.is_shutdown():
        for radian in RADIANS:
            msg = get_msg(radian)
            pub.publish(msg)
            rate.sleep()


def get_msg(radian):
    msg = JointTrajectory()
    msg.header.stamp = rospy.Time.now()
    # rospy.loginfo(rospy.Time.now().to_sec())
    msg.joint_names = JOINT_NAMES
    joint_trajectory_point = JointTrajectoryPoint()
    joint_trajectory_point.positions = [1.57, -1.57, -3.14, -1.57, math.sin(radian) * MULTIPLIER + SHIFT, 0.0]
    joint_trajectory_point.time_from_start.secs = SECONDS_PER_MOVE
    msg.points.append(joint_trajectory_point)
    return msg


if __name__ == '__main__':
    rospy.init_node(NODE_NAME)
    pub = rospy.Publisher(PUBLISHER, JointTrajectory, queue_size=10)
    publish_frequency = FREQUENCY
    rate = rospy.Rate(publish_frequency)

    rospy.loginfo("Initialized. %.2f seconds per cycle."
                  % round((float(RESOLUTION) / FREQUENCY), 2))
    launch()
