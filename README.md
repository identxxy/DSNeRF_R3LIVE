# DSNeRF + ROS

A quick hack to combine [DSNeRF](https://github.com/dunbar12138/DSNeRF) with [R3LIVE](https://github.com/hku-mars/r3live).  
The idea of the project is to provide depth-supervision from **dense point clouds** for a NeRF.

This is the DSNerf [tutorial](https://github.com/dunbar12138/DSNeRF/blob/main/resources/tutorial.md) about how to use depth-supervison(sparse point cloud using COLMAP).

## ROS bag data extraction

Use the files in `rosbagUtils/` to extract data from a ROS bag. Details sees [there](rosbagUtils/README.md)

An example R3LIVE bag is [Here](https://hkustconnect-my.sharepoint.com/:u:/g/personal/xxuat_connect_ust_hk/EYaosGcTZLVLm11kJtCNhLoBnMl4GNRfpuYHrIVSFE0J7w?e=mT294M). It is a 5 senconds segment from R3LIVE dataset with all the ouputs from R3LIVE.

## Data preparation

Create a dataset under `data/<exp_name>`. After extract data from rosbag, we should have `<img_dir>, <points_dir>, <poses_dir>`. Put the images, points and poses(odom) files into the folder like below. 

```
├── data
│   └── hkust_2view_ros
│       ├── images
│       │   ├── frame000001.jpg
│       │   └── frame000075.jpg
│       ├── ros
│       │   ├── odom
│       │   │   ├── 0001.npy
│       │   │   └── 0075.npy
│       │   └── points
│       │       ├── 0001.npy
│       │       └── 0051.npy
```

**NOTE**  
Because the LiDAR scanned points and images captured by the camera are not synchronized, we need to **manually** select the proper data frame according to the timestamp provided in `timestamp.txt`.

## Pose generation

```
python ros2poses.py data/<exp_name>
``` 

It will create a file `poses_bounds.npy` under `data/<exp_name>` which can be loaded as llff datatype.

## Training args

In `config/<config_file>`, be sure to set `ros_depth=True`, then run 

```
python run_nerf.py --config config/<config_file>
```