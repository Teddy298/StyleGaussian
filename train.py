import subprocess
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, required=True, help='dataset dir')
    parser.add_argument('--wikiartdir', type=str, required=True, help='wikiart dir')
    parser.add_argument('--exp_name', type=str, default='default', help='experiment name')
    parser.add_argument('--camera', type=str, default='mirror', help='camera')
    parser.add_argument('--gs_type', type=str, default='amorphous', help='gs_type')
    parser.add_argument("--style_weight", type=float, default=10., help='style weight')


    args = parser.parse_args()

    if args.data[-1] == '/':
        args.data = args.data[:-1]

    dataset_name = os.path.basename(args.data)
    # reconstruction
    # subprocess.run(['python', 'train_reconstruction.py',
    #                '-s', args.data, '--exp_name', args.exp_name])
    path = f'output/{dataset_name}/reconstruction/{args.exp_name}'
    subprocess.run(['python', '../MiraGe/train.py',
                    '-s', args.data, '-m', path, '--camera', args.camera, '--gs_type', args.gs_type])

    # feature embedding
    ply_path = f'output/{dataset_name}/reconstruction/{args.exp_name}/point_cloud/iteration_30000/point_cloud.ply'
    subprocess.run(['python', 'train_feature.py',
                    '-s', args.data, '--ply_path', ply_path, '--exp_name', args.exp_name, '--camera', args.camera,
                    '--gs_type', args.gs_type])

    # style transfer
    ckpt_path = f'output/{dataset_name}/feature/{args.exp_name}/chkpnt/feature.pth'
    subprocess.run(['python', 'train_artistic.py',
                    '-s', args.data, '--ckpt_path', ckpt_path, '--exp_name', args.exp_name, '--wikiartdir',
                    args.wikiartdir, '--camera', args.camera, '--gs_type', args.gs_type, '--style_weight', str(args.style_weight)])

