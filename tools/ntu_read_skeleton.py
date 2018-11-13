import numpy as np
import os

ori_index = [(1, 2), (2, 21), (3, 21), (4, 3), (5, 21), (6, 5), (7, 6),
                    (8, 7), (9, 21), (10, 9), (11, 10), (12, 11), (13, 1),
                    (14, 13), (15, 14), (16, 15), (17, 1), (18, 17), (19, 18),
                    (20, 19), (22, 8), (23, 8), (24, 12), (25, 12)]


def read_skeleton(file):
    with open(file, 'r') as f:
        skeleton_sequence = {}
        skeleton_sequence['numFrame'] = int(f.readline())
        skeleton_sequence['frameInfo'] = []
        for t in range(skeleton_sequence['numFrame']):
            frame_info = {}
            frame_info['numBody'] = int(f.readline())
            frame_info['bodyInfo'] = []
            for m in range(frame_info['numBody']):
                body_info = {}
                body_info_key = [
                    'bodyID', 'clipedEdges', 'handLeftConfidence',
                    'handLeftState', 'handRightConfidence', 'handRightState',
                    'isResticted', 'leanX', 'leanY', 'trackingState'
                ]
                body_info = {
                    k: float(v)
                    for k, v in zip(body_info_key, f.readline().split())
                }
                body_info['numJoint'] = int(f.readline())
                body_info['jointInfo'] = []
                for v in range(body_info['numJoint']):
                    joint_info_key = [
                        'x', 'y', 'z', 'depthX', 'depthY', 'colorX', 'colorY',
                        'orientationW', 'orientationX', 'orientationY',
                        'orientationZ', 'trackingState'
                    ]
                    joint_info = {
                        k: float(v)
                        for k, v in zip(joint_info_key, f.readline().split())
                    }
                    body_info['jointInfo'].append(joint_info)
                frame_info['bodyInfo'].append(body_info)
            skeleton_sequence['frameInfo'].append(frame_info)
    return skeleton_sequence


# def read_xyz(file, max_body=2, num_joint=25):
#     seq_info = read_skeleton(file)
#     data = np.zeros((3, seq_info['numFrame'], num_joint, max_body))
#     for n, f in enumerate(seq_info['frameInfo']):
#         for m, b in enumerate(f['bodyInfo']):
#             for j, v in enumerate(b['jointInfo']):
#                 if m < max_body and j < num_joint:
#                     data[:, n, j, m] = [v['x'], v['y'], v['z']]
#                 else:
#                     pass
#     return data

def read_xyz(file, max_body=2, num_joint=24):
    seq_info = read_skeleton(file)
    data = np.zeros((3, seq_info['numFrame'], num_joint, max_body))
    for n, f in enumerate(seq_info['frameInfo']):
        for m, b in enumerate(f['bodyInfo']):
            # for j, v in enumerate(b['jointInfo']):
            #     if m < max_body and j < num_joint:
                for i, o_i in enumerate(ori_index):
                    if m < max_body and i < num_joint:
                        xi = b['jointInfo'][o_i[0]-1]['x']-b['jointInfo'][o_i[1]-1]['x']
                        yi = b['jointInfo'][o_i[0]-1]['y']-b['jointInfo'][o_i[1]-1]['y']
                        zi = b['jointInfo'][o_i[0]-1]['z']-b['jointInfo'][o_i[1]-1]['z']
                        if not(xi==0 and yi==0 and zi==0):
                            length = pow((xi**2+yi**2+zi**2),0.5)
                            data[:, n, i, m] = [xi/length, yi/length, zi/length]
                        # data[3+i, n, i, m] =1
    return data


if __name__ == '__main__':
    data_path = 'D:/dataSet/NTU-D-New/nturgb+d_skeletons'
    test_skeleton = 'S014C002P037R002A050.skeleton'

    data = read_xyz(os.path.join(data_path, test_skeleton))
    print(data)
