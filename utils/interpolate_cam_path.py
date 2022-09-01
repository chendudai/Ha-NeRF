import numpy as np
from datasets import dataset_dict
from scipy.spatial.transform import Rotation


def generate_camera_path(dataset, img_id_list=[16, 15], interpolate_times=[10, 10]):
    '''
    args:
        img_id_list: IDs of key-frame images
        interpolate_times: in each segment, how many frames should be interpolated
    '''
    N_keyframes = len(img_id_list)
    pose_list = []
    for index, id in enumerate(img_id_list):
        pose = dataset.poses_dict[id]
        # The camera pose is defined in 4x4 matrix.
        pose = np.concatenate((pose, np.array([[0, 0, 0, 1]])))  # (1, 4, 4)
        pose_list.append(pose)

    pose_interp_list = []
    for index in range(len(pose_list)):
        pose = pose_list[index]
        pose_next = pose_list[(index + 1) % N_keyframes]
        r = Rotation.from_matrix(pose[:3, : 3])
        r_n = Rotation.from_matrix(pose_next[:3, : 3])
        eulers = r.as_euler('xyz')
        eulers_n = r_n.as_euler('xyz')
        rx = np.linspace(eulers[0], eulers_n[0], num=interpolate_times[index], endpoint=False)
        ry = np.linspace(eulers[1], eulers_n[1], num=interpolate_times[index], endpoint=False)
        rz = np.linspace(eulers[2], eulers_n[2], num=interpolate_times[index], endpoint=False)
        eulers_list = np.concatenate((rx[:, np.newaxis], ry[:, np.newaxis], rz[:, np.newaxis]), axis=1)  # []
        r_list = Rotation.from_euler('xyz', eulers_list).as_matrix()

        positions = pose[:3, 3]
        positions_n = pose_next[:3, 3]
        px = np.linspace(positions[0], positions_n[0], num=interpolate_times[index], endpoint=False)
        py = np.linspace(positions[1], positions_n[1], num=interpolate_times[index], endpoint=False)
        pz = np.linspace(positions[2], positions_n[2], num=interpolate_times[index], endpoint=False)
        positions_list = np.concatenate((px[:, np.newaxis], py[:, np.newaxis], pz[:, np.newaxis]), axis=1)
        pose_l = np.concatenate((r_list, positions_list[:, :, np.newaxis]), axis=2)
        pose_interp_list.append(pose_l)

    pose_interp_list = np.concatenate(pose_interp_list, axis=0)
    return pose_interp_list