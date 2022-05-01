import os
import argparse

import numpy as np
import rosbag

from nav_msgs.msg import Odometry

def q2R(w, x, y, z):
    return np.array([
        [1 - 2 * y**2 - 2 * z**2,
         2 * x * y - 2 * w * z,
         2 * z * x + 2 * w * y],
        [2 * x * y + 2 * w * z,
         1 - 2 * x**2 - 2 * z**2,
         2 * y * z - 2 * w * x],
        [2 * z * x - 2 * w * y,
         2 * y * z + 2 * w * x,
         1 - 2 * x**2 - 2 * y**2]])


def main():
    """Extract a folder of images from a rosbag.
    """
    parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument("output_dir", help="Output directory.")
    parser.add_argument("odom_topic", help="Odometry topic.")

    args = parser.parse_args()

    print("Extract odometry from %s on topic %s into %s" % (args.bag_file,
                                                          args.odom_topic, args.output_dir))
    print("Timestamp saved to %s/timestamp.txt" % args.output_dir)
    

    bag = rosbag.Bag(args.bag_file, "r")
    count = 0
    
    ts_list = []
    for topic, msg, tm in bag.read_messages(topics=[args.odom_topic]):
        pos = msg.pose.pose.position
        quat = msg.pose.pose.orientation

        R = q2R(quat.w, quat.x, quat.y, quat.z)
        t = np.array([pos.x, pos.y, pos.z]).reshape(3,1)

        mat = np.concatenate([R, t], axis=1)
        np.save(args.output_dir+f"/{count:05d}", mat)
        print(f"Save Odometry {count}")

        count += 1
        ts_list.append(tm.to_sec())

    bag.close()

    with open(args.output_dir+"/timestamp.txt", 'w') as f:
        f.writelines("%s\n" % ts for ts in ts_list)
    return

if __name__ == '__main__':
    main()
