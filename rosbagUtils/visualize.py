import numpy as np
import matplotlib.pyplot as plt
import os

odom_dir = 'data/hkust_5view_ros/ros/odom'
pts_dir = 'data/hkust_5view_ros/ros/points'
odom_files = sorted(os.listdir(odom_dir))
pts_files = sorted(os.listdir(pts_dir))

mat_ros2colmap = np.array([
        [0, -1, 0],
        [0, 0, -1],
        [1, 0, 0]
])

assert len(odom_files) == len(pts_files), 'length of odom and pts must equal'

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

odom_list = [mat_ros2colmap @ np.load(odom_dir + '/' + f) for f in odom_files]
pts_list = [np.load(pts_dir + '/' + f) for f in pts_files]
rst_pts_list = []
color_list = ['red', 'green', 'blue', 'yellow', 'orange']

for i in range(len(odom_list)):
    odom = odom_list[i]
    pts = pts_list[i] # N x 3
    depth = pts[:, 0]
    mask = depth < 20
    depth = depth[mask].reshape(-1,1)
    u = -pts[:, 1]
    u = u[mask].reshape(-1,1)
    v = -pts[:, 2]
    v = v[mask].reshape(-1,1)
    bottom = np.ones((depth.shape[0], 1))
    pts_bottom = np.concatenate([u, v, depth, bottom], 1).T # 4 x N
    rst_pts = odom @ pts_bottom
    #rst_pts = pts.T
    rst_pts_list.append(rst_pts) # 3 x N
    xs = rst_pts[0,:]
    ys = rst_pts[1,:]
    zs = rst_pts[2,:]
    ax.scatter(xs, ys, zs, s = 0.01, color=color_list[i])

plt.show()


