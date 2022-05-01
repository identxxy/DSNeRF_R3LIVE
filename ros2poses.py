import os
import numpy as np

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('scenedir', type=str,
                    help='input scene directory')
args = parser.parse_args()


def load_ros_data(base_dir):
    # x-front, y-left, z-up (ROS)
    # x-right, y-down, z-front (COLMAP)
    mat_ros2colmap = np.array([
        [0, -1, 0],
        [0, 0, -1],
        [1, 0, 0]
    ])
    cam_hwf = np.array([1024, 1280, 863]).reshape((3,1))

    points_dir = os.path.join(base_dir, 'ros/points')
    poses_dir = os.path.join(base_dir, 'ros/odom')

    # save near far point
    bds_list = []
    points_files = os.listdir(points_dir)
    points_files.sort()
    for f in points_files:
        pts = np.load(os.path.join(points_dir, f))
        pts_depth = pts[:, 2]
        bds_list.append((pts_depth.min(), pts_depth.max()))

    c2w_list = []
    poses_files = os.listdir(poses_dir)
    poses_files.sort()
    for f in poses_files:
        pose = np.load(os.path.join(poses_dir, f))
        c2w_list.append(mat_ros2colmap @ pose)
    c2w_mats = np.stack(c2w_list)  # N x 3 x 4

    assert len(bds_list) == len(c2w_list), "ROS points frame# != poses frame#."
    poses = c2w_mats[:, :3, :4].transpose([1,2,0])
    poses = np.concatenate([poses, np.tile(cam_hwf[..., np.newaxis], [1,1,poses.shape[-1]])], 1)

    poses = np.concatenate([poses[:, 1:2, :], poses[:, 0:1, :], -poses[:, 2:3, :], poses[:, 3:4, :], poses[:, 4:5, :]], 1)

    save_arr = []
    for i in range(len(c2w_list)):
        save_arr.append(np.concatenate([poses[..., i].ravel(), np.array([bds_list[i][0], bds_list[i][1]])], 0))
    save_arr = np.array(save_arr)
    np.save(os.path.join(base_dir, 'poses_bounds.npy'), save_arr)
    print("generate file ")

if __name__=='__main__':
    load_ros_data(args.scenedir)