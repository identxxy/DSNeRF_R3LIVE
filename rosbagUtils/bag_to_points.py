import os
import argparse
from turtle import pos

import numpy as np
import rosbag


def main():
    """Extract a folder of images from a rosbag.
    """
    parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument("output_dir", help="Output directory.")
    parser.add_argument("points_topic", help="laser point topic.")

    args = parser.parse_args()

    print("Extract points from %s on topic %s into %s" % (args.bag_file,
                                                          args.points_topic, args.output_dir))
    print("Timestamp saved to %s/timestamp.txt" % args.output_dir)
    

    bag = rosbag.Bag(args.bag_file, "r")
    count = 0
    
    ts_list = []
    for topic, msg, tm in bag.read_messages(topics=[args.points_topic]):
        data = msg.data
        point_step = msg.point_step
        length = msg.width
        buffer = b''
        for i in range(length):
            frame = data[point_step * i : point_step * i + point_step]
            xyz_bytes = frame[0:12]
            buffer += xyz_bytes
        pts_xyz = np.frombuffer(buffer, np.float32).reshape(-1,3)
        np.save(args.output_dir+ f"/{count:05d}", pts_xyz)
        print(f"Save Points {count}")

        count += 1
        ts_list.append(tm.to_sec())

    bag.close()

    with open(args.output_dir+"/timestamp.txt", 'w') as f:
        f.writelines("%s\n" % ts for ts in ts_list)
    return

if __name__ == '__main__':
    main()
