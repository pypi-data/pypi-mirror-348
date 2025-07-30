import os
import sys

from absl import app
from absl import flags
from absl.flags import FLAGS

# import sys
# sys.path.append('..')

from omegaconf import OmegaConf
import pickle
import jax

from tqdm import tqdm

from learnax.registry import Registry
from learnax.utils import tree_stack, tree_unstack

import os

from biotite.structure import superimpose, rmsd, gyration_radius

import numpy as np

CA_INDEX = 1

def crystal_rmsd(crystal, traj):
    ca_traj = traj[:, traj.atom_name == 'CA']
    crystal_ca = crystal.atom_coord[:, CA_INDEX]
    aligned_ca_traj = superimpose(crystal_ca, ca_traj)[0]
    return rmsd(crystal_ca, aligned_ca_traj)

def radius_of_gyration(traj):
    return gyration_radius(traj)

from utils import prepare_data
from collections import defaultdict

def main(argv):

    # LOAD DATASET
    from dataset import mdCATHDataset
    checkpoint = FLAGS.checkpoint

    dataset = prepare_data(FLAGS.dataset, FLAGS.protein)

    protein = FLAGS.protein
    dataset = mdCATHDataset(
        base_path = '/mnt/timebucket/molmach_db/mdCATH/',
        domains=[protein],
        size_multiplier=10,
    )
    crystal = dataset.get_crystal(protein)

    ref_trajs = []
    print('Loading Reference Trajectory')
    for replica in range(5):
        ref_traj = dataset.get_trajectory(protein, 348, replica)
        ref_trajs.append(ref_traj)

    run = Registry('deepjump').fetch_run(FLAGS.id)
    trajs = run.read_all(f'samples/{checkpoint}/{protein}/*.pyd')
    trajs.update({
        f'ref_{i}': ref_traj for i, ref_traj in enumerate(ref_trajs)
    })

    metrics = defaultdict(dict)

    for traj_path, traj in trajs.items():
        traj_name = os.path.basename(traj_path)
        metrics[traj_name].update({
            'crystal_rmsd': crystal_rmsd(crystal, traj),
            'gyradius': radius_of_gyration(traj),
        })

    metrics_ = {}
    for k,v in metrics.items():
        for kk, vv in v.items():
            metrics_.setdefault(kk, {})[k] = vv

    metrics_path = f'samples/{checkpoint}/{protein}/metrics.pyd'
    run.save(metrics_path, metrics_)

    print('Done.')

flags.DEFINE_string('id', 'exqzy4av', 'model wandb id')
flags.DEFINE_string('dataset', None, 'dataset to fetch protein from')
flags.DEFINE_string('protein_ids', 'ids/fast_folding.txt', 'proteins to evaluate')
flags.DEFINE_integer('checkpoint', -1, 'checkpoint step index')

if __name__ == "__main__":
    app.run(main)
