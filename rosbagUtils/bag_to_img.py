import os
import argparse

import cv2

import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def main():
    """Extract a folder of images from a rosbag.
    """
    parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument("output_dir", help="Output directory.")
    parser.add_argument("image_topic", help="Image topic.")

    args = parser.parse_args()

    print("Extract images from %s on topic %s into %s" % (args.bag_file,
                                                          args.image_topic, args.output_dir))
    print("Timestamp saved to %s/timestamp.txt" % args.output_dir)
    

    bag = rosbag.Bag(args.bag_file, "r")
    bridge = CvBridge()
    count = 0
    
    ts_list = []
    for topic, msg, t in bag.read_messages(topics=[args.image_topic]):
        cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")

        cv2.imwrite(os.path.join(args.output_dir, "frame%06i.png" % count), cv_img)
        print("Wrote image %i" % count)

        count += 1
        ts_list.append(t.to_sec())

    bag.close()

    with open(args.output_dir+"/timestamp.txt", 'w') as f:
        f.writelines("%s\n" % ts for ts in ts_list)
    return

if __name__ == '__main__':
    main()
