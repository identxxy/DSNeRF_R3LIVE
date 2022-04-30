import os
import argparse
from turtle import pos

import numpy as np
import rosbag

cam = np.array([
    [863, 0 , 640],
    [0, 863, 518],
    [0, 0, 1]
])

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
        u, v, depth = -pts_xyz[:,1], -pts_xyz[:,2], pts_xyz[:,0]
        pts_uvd = np.stack([u, v, depth]) # 3 x N
        pts = cam @ pts_uvd # 3 x N
        valid  = (pts[2:] > 0).reshape(-1)
        pts = pts[:,valid]
        pts = pts / pts[2,:]
        uvd = np.stack([pts[0,:], pts[1,:], depth[valid]]).transpose() # N x 3
        np.save(args.output_dir+ f"/{count: 05d}", uvd)
        print(f"Save Points {count}")

        count += 1
        ts_list.append(tm.to_sec())

    bag.close()

    with open(args.output_dir+"/timestamp.txt", 'w') as f:
        f.writelines("%s\n" % ts for ts in ts_list)
    return

if __name__ == '__main__':
    main()
