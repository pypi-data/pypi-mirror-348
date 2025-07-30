


import time


from numpy.lib.format import open_memmap
from tqdm.contrib.concurrent import process_map
from tqdm import tqdm

import os
import matplotlib
import h5py as h5
import numpy as np
import pandas as pd
import glob
from os.path import join as opj
import matplotlib.pyplot as plt
import pickle


from copy import deepcopy

from biotite.structure.io.pdb import PDBFile
from moleculib.protein.datum import ProteinDatum
from huggingface_hub import HfApi
from huggingface_hub import hf_hub_download
from huggingface_hub import hf_hub_url

from functools import partial

from biotite.structure import get_residue_count
from biotite.structure import superimpose, stack


from biotite.structure import filter_amino_acids
import biotite.structure as struc
from biotite.structure.io.pdb import PDBFile

from collections import defaultdict
import itertools 

SOURCE_FOLDER_URL = "http://pub.htmd.org/protein_thermodynamics_data/reference_trajectories/"

FAST_FOLDERS = [
    'chignolin', 
    'trpcage', 
    'bba',
    # 'villin', # REMOVED BECAUSE IT HAS NON-STANDARD RESIDUES
    'wwdomain', 
    'ntl9', 
    'bbl',
    'proteinb', 
    'bba', 
    'homeodomain', 
    'proteing', 
    'a3D', 
    'lambda'
]

CLUSTERS_SIZES = [16, 32, 64, 128]

import biotite
import random

import sys
sys.path.append('..')

from deeptime.util.validation import implied_timescales

from measure import compute_tica, get_clusters, compute_msm, embed_traj
from utils import build_alpha_helix


class FastFoldingDataset:

    def __init__(
        self,
        base_path = '/mas/projects/molecularmachines/db/fast-folding',
        proteins=None,
        tau=1,
        shuffle=True,
        epoch_size=10000000,
        pad=None,
        defaults=None,
        fetch_crystal=False,
        superimpose=False,
    ):
        if proteins == None:
            proteins = FAST_FOLDERS

        self.base_path = base_path
        self.memmap_path = os.path.join(base_path, 'memmaped_data/')
        
        self.proteins = proteins
        self.tau = tau
        self.time_sort = True
        self.epoch_size = epoch_size
        self.fetch_crystal = fetch_crystal
        self.superimpose = superimpose

        self.atom_arrays = {
            protein: PDBFile.read(
                self.memmap_path + protein + "/template.pdb"
            ).get_structure()[0] for protein in tqdm(proteins)
        }

        self.files = {
            p: list(filter(lambda x: x.endswith('.mmap'), os.listdir(self.memmap_path + p))) for p in proteins
        }

        for k, v in self.files.items():
            random.shuffle(self.files[k])

        self.clusters = {}
        for p in self.proteins:
            cluster_path = f'{self.base_path}/clusters/{p}.pyd'
            if os.path.exists(cluster_path):
                with open(cluster_path, 'rb') as f:
                    cluster_to_file = pickle.load(f)
                    self.clusters[p] = cluster_to_file
                print (f"Loaded {len(self.clusters[p])} clusters for {p}")

    def __len__(self):
        return self.epoch_size
    

    def write_memmap(self, file, protein, template, downsample=10):
        try:
            source_dir = self.base_path + '/untar'
            memmap_data_path = opj(self.memmap_path, protein)

            file_name = file.split('/')[-1]
            if file_name == 'output.filtered.xtc':
                # for some reason this file of ntl9 is broken
                return

            memmap_file_name = file_name.split('.')[0] + '.mmap'
            memmap_path = opj(memmap_data_path, memmap_file_name)

            file = biotite.structure.io.xtc.XTCFile.read(file)
            traj_aa = file.get_structure(template)

            coords = traj_aa._coord[::downsample, filter_amino_acids(template) & (template.element != 'H')]
            memmap_coord = open_memmap(memmap_path, mode='w+', dtype=np.float32, shape=coords.shape)
            memmap_coord[:] = coords
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"Error writing memmap for {file}: {e}")
            # print(coords.shape)

        # return None

    def preprocess(self, num_workers=32):
        source_dir = self.base_path + '/untar'
        crystal_dir = self.base_path + '/experimental_structures'

        for protein in self.proteins:
            
            print(f"Processing {protein}")
            
            memmap_data_path = opj(self.memmap_path, protein)
            if not os.path.exists(memmap_data_path):
                os.makedirs(memmap_data_path)

            with open(os.path.join(crystal_dir, f"{protein}.pdb"), 'r') as f:
                file = PDBFile.read(f)
                crystal = file.get_structure()[0]

            dirs = os.listdir(source_dir)
            dirs = [dir for dir in dirs if protein in dir]

            for dir in dirs:
                print(f"Processing {dir}")

                xtc_patt = source_dir + f"/{dir}/**/*.xtc"
                # xtc_files = glob.glob(xtc_patt, recursive=True)

                xtc_files = []
                # limit = 1
                # xtc_files = list(itertools.islice(glob.iglob(xtc_patt, recursive=True), limit))
                
                pdb_patt = source_dir + f"/{dir}/**/filtered.pdb"
                pdb_template = list(itertools.islice(glob.iglob(pdb_patt, recursive=True), 1))[0]

                with open(pdb_template, 'r') as f:
                    file = PDBFile.read(f)
                    template = file.get_structure()[0]
                    template.res_name[template.res_name == 'HSE'] = ['HIS'] * len(template[template.res_name == 'HSE'])
                    template.res_name[template.res_name == 'HSD'] = ['HIS'] * len(template[template.res_name == 'HSD'])

                from biotite.structure import filter_amino_acids

                filt_crystal = crystal[filter_amino_acids(crystal) & (crystal.element != 'H')]
                crystal_cas = filt_crystal[filt_crystal.atom_name == 'CA']
                filt_template = template[filter_amino_acids(template) & (template.element != 'H')]
                template_cas = filt_template[filt_template.atom_name == 'CA']

                assert len(crystal_cas) == len(template_cas)

                if num_workers == 0:
                    out = []
                    for file in tqdm(xtc_files):
                        out_ = self.write_memmap(
                            file,
                            protein,
                            template=template
                        )
                        out.append(out_)
                else:
                    process_map(
                        partial(
                            self.write_memmap,
                            protein=protein,
                            template=template
                        ),
                        xtc_files,
                        max_workers=num_workers
                    )
            # save template 
            with open(opj(memmap_data_path, 'template.pdb'), 'w') as f:
                pdbfile = PDBFile()
                pdbfile.set_structure(filt_template)
                pdbfile.write(f)

    @staticmethod
    def untar_file(file, tar_path, untar_path):
        if file.endswith('.tar.gz'):
            filename = file.split('/')[-1] 
            filename = file.split('.')[0]
            os.makedirs(f"{untar_path}/{filename}", exist_ok=True)
            os.system(f"tar -xvzf {tar_path}/{file} -C {untar_path}/{filename}")


    def download(self, num_workers=16):
        tar_path = opj(self.base_path, 'tar')
        # os.system(f"mkdir -p {tar_path}")
        # os.system(f"wget --verbose --recursive --no-parent {SOURCE_FOLDER_URL} -P {tar_path}")

        untar_path = opj(self.base_path, 'untar')
        os.system(f"mkdir -p {untar_path}")
        files = os.listdir(tar_path)
        
        from tqdm.contrib.concurrent import process_map
        process_map(partial(self.untar_file, tar_path=tar_path, untar_path=untar_path), files, max_workers=num_workers)
        print(f"Untarred files to {untar_path}")

    def get_trajectories(self, protein, max_trajs=None, get_names=False):
        from biotite.structure import AtomArrayStack
        if max_trajs == None:
            max_trajs = len(self.files[protein])

        trajectories = []
        template = self.atom_arrays[protein]

        for idx in range(min(max_trajs, len(self.files[protein]))):
            filename = self.files[protein][idx]
            mmap_path = opj(self.memmap_path, protein, filename)
            coord = open_memmap(mmap_path, mode='r', dtype=np.float32)

            if len(coord) > 10:
                atom_array_stack = AtomArrayStack(0, template.shape[0])
                atom_array_stack._annot = template._annot
                atom_array_stack._coord = np.copy(coord)
                if get_names:
                    trajectories.append((filename, atom_array_stack))
                else:
                    trajectories.append(atom_array_stack)
        
        return trajectories

    def get_crystal(self, protein):
        pdbfile = PDBFile.read(opj(self.base_path + '/experimental_structures', f"{protein}.pdb"))
        atom_array = pdbfile.get_structure()[0]
        return atom_array

    def compute_metrics(self):
        
        for protein in self.proteins:
            print(f"Computing metrics for {protein}")

            ref_trajs = self.get_trajectories(protein, max_trajs=None, get_names=True)
            names, ref_trajs = zip(*ref_trajs)

            tica_model = compute_tica(ref_trajs, 10, 2)
            os.makedirs(f'.metrics_cache/{protein}', exist_ok=True)

            tica_feats = [tica_model.transform(embed_traj(traj)) for traj in ref_trajs]
            
            samp = ref_trajs[0]
            seq = samp.res_name[samp.atom_name == 'CA']

            seq = [biotite.sequence.ProteinSequence.convert_letter_3to1(seq_) for seq_ in seq]
            
            helix = build_alpha_helix(seq)
            helix_tics = tica_model.transform(embed_traj([helix])[0])
            
            crystal = self.get_crystal(protein)
            crystal = crystal[crystal.element != 'H']
            crystal = crystal[biotite.structure.filter_amino_acids(crystal)]
            crystal_tics = tica_model.transform(embed_traj([crystal])[0])

            cluster_metrics = defaultdict(dict)
            file_maps = defaultdict(dict)

            for k in CLUSTERS_SIZES:

                kmeans = get_clusters(tica_feats, k)
                clusters = [kmeans.transform(feats) for feats in tica_feats]
                
                lags, msms, GSs = compute_msm(clusters, num_clusters=k)

                clusters_cat = np.concatenate(clusters, axis=0)
                cluster_w = GSs[-1]/np.bincount(clusters_cat)
                weights = cluster_w[clusters_cat]

                cluster_to_file = defaultdict(list)
                for traj_name, traj_cluster in zip(names, clusters):
                    for idx, cluster in enumerate(traj_cluster):
                        cluster_to_file[cluster].append((traj_name, idx))

                helix_cluster = kmeans.transform(helix_tics[None]) 
                crystal_cluster = kmeans.transform(crystal_tics[None])

                cluster_metrics[k] = {
                    'msms': msms,
                    'timescales': implied_timescales(msms),
                    'lags': lags,
                    'kmeans': kmeans,
                    'weights': weights,
                    'GSs': GSs,
                    'crystal_cluster': crystal_cluster,
                    'helix_cluster': helix_cluster,
                }

                file_maps[k] = cluster_to_file
                    

            metrics_path = os.path.join(self.base_path, f'metrics/{protein}.pyd')
            os.makedirs(os.path.dirname(metrics_path), exist_ok=True)

            file_maps_path = os.path.join(self.base_path, f'clusters/{protein}.pyd')
            os.makedirs(os.path.dirname(file_maps_path), exist_ok=True)
            with open(file_maps_path, 'wb') as file:
                pickle.dump(file_maps, file)

            with open(metrics_path, 'wb') as file:
                pickle.dump(
                    {
                        'tica_model': tica_model,
                        'feats': tica_feats,
                        'crystal_tics': crystal_tics,
                        'helix_tics': helix_tics,
                        'clusters': cluster_metrics,
                    }, 
                    file,
                )

    def get_metrics(self, protein):
        metrics_path = os.path.join(self.base_path, f'metrics/{protein}.pyd')
        with open(metrics_path, 'rb') as file:
            metrics = pickle.load(file)
        return metrics

    def __getitem__(self, idx):
        protein = self.proteins[idx % len(self.proteins)]
        cluster_k = 128

        while True:
            random_clust = random.choice(list(self.clusters[protein][cluster_k].keys()))
            random_file, random_idx = random.choice(self.clusters[protein][cluster_k][random_clust])

            mmap_path = opj(self.memmap_path, protein, random_file)
            coord = open_memmap(mmap_path, mode='r', dtype=np.float32)
            template = self.atom_arrays[protein]

            if random_idx < len(coord) - self.tau - 1:
                break

        idx1 = random_idx
        aa1 = deepcopy(template)
        aa1._coord = coord[idx1]

        p1 = ProteinDatum.from_atom_array(
            aa1,
            header=dict(
                idcode=protein,
                resolution=None,
            ),
        )

        idx2 = idx1 + self.tau
        aa2 = deepcopy(template)
        aa2._coord = coord[idx2]
        p2 = ProteinDatum.from_atom_array(
            aa2,
            header=dict(
                idcode=protein,
                resolution=None,
            ),
        )

        return [p1, p2]



if __name__ == '__main__':
    fast_folding_ds = FastFoldingDataset('/mas/projects/molecularmachines/db/fast-folding')

    fast_folding_ds.compute_metrics()


    # fast_folding_ds.download()
    # fast_folding_ds.preprocess(num_workers=0)
    # for protein in proteins:
    #     trajs = fast_folding_ds.get_trajectories(protein, 10)
    #     for traj in trajs:
    #         print(traj.shape)

    # fast_folding_ds.preprocess()
    # for i in range(20):
    #     p1, p2 = fast_folding_ds[i]
    #     print(p1)
    #     print(p2)

    # atlas_db = ATLASDataset(min_seq_len=80, max_seq_len=90)
    # print(list(atlas_db.atom_arrays.keys())[:10])

    # lens = []
    # for prot in atlas_db.atom_arrays:
    #     aa = atlas_db.atom_arrays[prot]
    #     ca = aa[aa.atom_name == 'CA']
    #     lens.append(len(ca))
    # import matplotlib.pyplot as plt
    # plt.hist(lens, bins=100)
    # plt.savefig('hist.png')

    # domains = ['1yn3A00', '2jzvA00', '2qyoA02']
    # dataset = mdCATHDataset.download(domain_ids=domains, data_path='/mnt/timebucket/molmach_db/mdCATH/')
    # dataset.preprocess(num_workers=0)
    

    # dataset = mdCATHDataset(base_path='/mnt/timebucket/molmach_db/mdCATH/')

    # for atom_array in tqdm(list(dataset.atom_arrays.values())):
    #     datum = ProteinDatum.from_atom_array(atom_array)


    # import matplotlib.pyplot as plt
    # sequence_lengths = [len(np.unique(aa.res_id)) for aa in list(dataset.atom_arrays.values())]

    # _ = plt.hist(sequence_lengths, bins=100)
    # plt.savefig('./sequence_lengths.png')
