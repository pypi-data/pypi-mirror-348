import os
import sys

from absl import app
from absl import flags
from absl.flags import FLAGS

import sys
sys.path.append('..')

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


from collections import defaultdict
from utils import prepare_data


FAST_FOLDERS = [
    # 'chignolin',
    # 'trpcage', 
    # 'bba',
    # 'wwdomain',
    # 'villin',
    # 'ntl9',
    # 'proteinb',
    # 'bbl',
    'homeodomain',
    # 'proteing',
    # 'a3D',
    # 'lambda',
]


def flip_dict(dict_):
    flipped = {}
    for k,v in dict_.items():
        for kk, vv in v.items():
            flipped.setdefault(kk, {})[k] = vv
    return flipped

import biotite
from deeptime.util.validation import implied_timescales
from measure import get_clusters, compute_msm, embed_traj

def main(argv):
    # LOAD DATASET
    checkpoint = FLAGS.checkpoint
    # with open(FLAGS.protein_ids) as f:
        # arr = f.read().splitlines()
    # dataset, proteins = arr[0], arr[1:]
    ids = ['k76lu3f8']#, 'mwxf79u9', 'zr3x0ui1', 'opgxy06w']

    for id in ids:
        run = Registry('deepjump').fetch_run(id)
        
        dataset = prepare_data('fast-folding', FAST_FOLDERS)
        proteins = FAST_FOLDERS

        for protein in proteins:
            print(f'Benchmarking {protein}, model {id}...')

            ref_metrics = dataset.get_metrics(protein)
            tica_model = ref_metrics['tica_model']

            trajs = run.read_all(f'samples/{checkpoint}/{protein}/{FLAGS.mode}/*_traj.pyd')
            names, trajs = zip(*trajs.items())
            # print(run.path + f'/samples/{checkpoint}/{protein}/{FLAGS.mode}/*_traj.pyd')
            print('Loaded trajs:', len(trajs))

            tica_feats = [tica_model.transform(embed_traj(traj)) for traj in trajs]

            cluster_metrics = dict()
            for k, clust_metrics in ref_metrics['clusters'].items():
                kmeans = clust_metrics['kmeans']
                clusters = [kmeans.transform(feats) for feats in tica_feats]
                
                lags, msms, GSs = compute_msm(clusters, num_clusters=k)
                clusters_cat = np.concatenate(clusters, axis=0)
                cluster_w = GSs[-1]/np.bincount(clusters_cat, minlength=k)

                weights = [cluster_w[clust] for clust in clusters]
                cluster_metrics[k] = {
                    'msms': msms,
                    'clusters': clusters,
                    'weights': weights,
                    'timescales': implied_timescales(msms),

                }

            metrics = {
                'tics': tica_feats,
                'clusters': cluster_metrics,
            }

            metrics_path = f'samples/{checkpoint}/{protein}/{FLAGS.mode}/tica_metrics.pyd'
            print('Saving metrics... ', metrics_path)
            run.save(metrics_path, metrics)

    print('Done.')

# flags.DEFINE_string('id', 'zcun2wc3', 'model wandb id')
# flags.DEFINE_string('id', 'k76lu3f8', 'model wandb id')
flags.DEFINE_string('mode', 'chain', 'protein to simulate')
# 
flags.DEFINE_integer('checkpoint', -1, 'checkpoint step index')
if __name__ == "__main__":
    app.run(main)
