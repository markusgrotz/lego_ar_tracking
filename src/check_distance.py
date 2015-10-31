#!/usr/bin/env python
from __future__ import print_function, division

import rospy
import tf
import numpy as np

import requests


def checkpoint_reached(user_id):
    payload = {'user': user_id, 'checkpoint': 0, 'lap_num': 0, 'race': 0}
    r = requests.put('http://localhost:5000/api/time', data=payload)
    return r.ok


def main():

    rospy.init_node('check_distance', anonymous=True, log_level=rospy.INFO)

    listener = tf.TransformListener()
    rate = rospy.Rate(10.0)

    while not rospy.is_shutdown():
        for user_id in range(9):
            try:
                translation, rotation = listener.lookupTransform('/camera', 'ar_marker_{}'.format(user_id), rospy.Time(0))
            except:
                continue

            rospy.loginfo('translation {} for marker ar_marker_{}'.format(translation, user_id))

            if np.linalg.norm(translation) < 0.2:
                if not checkpoint_reached(user_id):
                    rospy.logwarn('unable to access api')

        rate.sleep()

if __name__ == '__main__':
    main()
