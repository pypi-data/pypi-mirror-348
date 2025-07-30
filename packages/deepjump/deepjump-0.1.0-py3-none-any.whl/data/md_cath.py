
TEMPERATURES = [320, 348, 379, 413, 450]
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

class mdCATHDataset:

    def __init__(
        self,
        # base_path = '/mas/projects/molecularmachines/db/mdCATH/',
        base_path = '/mnt/timebucket/molmach_db/mdCATH/',
        temperatures = None,
        domains = None,
        size_multiplier = 1,
        transform = None,
        max_seq_len = None,
        superpose = True,
    ):
        self.base_path = base_path
        self.data_path = os.path.join(base_path, 'data')
        self.memmap_path = os.path.join(base_path, 'memmaped_data/')
        self.size_multiplier = size_multiplier

        if temperatures == None:
            temperatures = TEMPERATURES
        else:
            assert all([temp in TEMPERATURES for temp in temperatures])
        self.temperatures = temperatures

        if domains == None:
            # open mdCATH_domains.txt
            with open(opj(base_path, 'mdCATH_domains.txt'), 'r') as f:
               domains = f.readlines()
               domains = [domain.strip() for domain in domains]

        print("Loading Atom Arrays")
        with open(opj(self.base_path, 'atom_arrays.pyd'), 'rb') as f:
            atom_arrays = pickle.load(f)

        self.seq_len = {key: get_residue_count(atom_array) for key, atom_array in list(atom_arrays.items())}

        if max_seq_len:
            domains = [domain for domain in domains if self.seq_len[domain] <= max_seq_len]
            atom_arrays = {key: atom_array for key, atom_array in atom_arrays.items() if self.seq_len[key] <= max_seq_len}

        self.transform = transform
        self.domains = domains
        self.atom_arrays = atom_arrays
        self.superpose = superpose

        # # check that domain files exist
        # accepted_domains = []
        # for domain in domains:
        #     samples = [(temp, rep) for temp in self.temperatures for rep in range(5)]
        #     sample_exists = [os.path.exists(opj(self.memmap_path, domain, str(temp), f"rep{rep}.memmap")) for temp, rep in samples]

        #     if os.path.exists(opj(self.memmap_path, f"{domain}")) and all(sample_exists):
        #         accepted_domains.append(domain)
            # else:
                # print(f"Skipping {domain}, not all samples exist. Missing {len(sample_exists) - sum(sample_exists)} samples")

        # print(f"Found {len(accepted_domains)} out of {len(domains)} domains")
        # print(f'Missing Domains: {set(domains) - set(accepted_domains)}')


    @classmethod
    def split(cls, base_path, factor, **kwargs):
        with open(opj(base_path, 'mdCATH_domains.txt'), 'r') as f:
            domains = f.readlines()
            domains = [domain.strip() for domain in domains]

        domains = list(np.random.permutation(domains))
        train_domains = domains[:int(len(domains) * factor)]
        val_domains = domains[int(len(domains) * factor):]

        return cls(domains=train_domains, **kwargs), cls(domains=val_domains, **kwargs)


    @staticmethod
    def download_domain(domain_id, data_path):
        if os.path.exists(opj(data_path, f"data/mdcath_dataset_{domain_id}.h5")):
            print(f"File {domain_id} already exists")
            return
        try:
            domain_path = hf_hub_download(
                repo_id="compsciencelab/mdCATH",
                repo_type='dataset',
                filename=f"mdcath_dataset_{domain_id}.h5",
                subfolder='data',
                local_dir=data_path
            )
            print(domain_path)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"Error downloading {domain_id}: {e}")


    @classmethod
    def download(cls, data_path, domain_ids=None,num_workers=0):
        # Output directory
        os.makedirs(data_path, exist_ok=True)

        # Download the ids file
        if domain_ids is None:
            ids_path = hf_hub_download(
                repo_id="compsciencelab/mdCATH",
                repo_type='dataset',
                filename='mdCATH_domains.txt',
                local_dir=data_path
            )
            with open(ids_path, 'r') as f:
                domain_ids = f.read().splitlines()[::-1]
        print(f"Downloading {len(domain_ids)} domains")
        if num_workers == 0:
            for domain_id in domain_ids:
                cls.download_domain(domain_id, data_path)
        else:
            process_map(
                partial(
                    cls.download_domain,
                    data_path=data_path
                ),
                domain_ids,
                max_workers=num_workers
            )

        return cls(base_path=data_path, domains=domain_ids)

    def write_memmap(self, domain_id,):
        memmap_data_path = opj(self.memmap_path, domain_id)
        if not os.path.exists(memmap_data_path):
            os.makedirs(memmap_data_path)

        # if (all([os.path.exists(opj(memmap_data_path, str(temp), f"rep{rep}.memmap")) for temp in self.temperatures for rep in range(5)])
        #     and os.path.exists(opj(memmap_data_path, "reference.pdb")) and os.path.exists(opj(memmap_data_path, "reference.pyd"))):
        #     print(f"Skipping {domain_id}, already exists")
        #     atom_array_pth = opj(memmap_data_path, "reference.pyd")
        #     with open(atom_array_pth, 'rb') as file:
        #         atom_array = pickle.load(file)
        #     return (domain_id, atom_array)

        with h5.File(opj(self.data_path, f"mdcath_dataset_{domain_id}.h5"), 'r') as f:

            pdb = f[domain_id]['pdbProteinAtoms']
            pdb = np.array(pdb).item().decode('utf-8')

            pdb_path = opj(memmap_data_path, "reference.pdb")
            with open(pdb_path, 'w') as file:
                file.write(pdb)

            file = PDBFile.read(pdb_path)
            atom_array = file.get_structure()[0]

            filter_ = atom_array.element != 'H'

            atom_array_path = opj(memmap_data_path, "reference.pyd")
            with open(atom_array_path, 'wb') as file:
                pickle.dump(atom_array[filter_], file)

            for temp in self.temperatures:
                if not os.path.exists(opj(memmap_data_path, str(temp))):
                    os.makedirs(opj(memmap_data_path, str(temp)), exist_ok=True)

                for rep in range(5):
                    memmap_path = opj(memmap_data_path, str(temp), f"rep{rep}.memmap")

                    # if os.path.exists(memmap_path):
                    #     print(f"Skipping {memmap_path}, already exists")
                    #     continue

                    coords = f[domain_id][str(temp)][str(rep)]["coords"][:]
                    coords = coords[:, filter_]
                    memmap_coord = open_memmap(memmap_path, mode='w+', dtype=np.float32, shape=coords.shape)
                    memmap_coord[:] = coords

        return (domain_id, atom_array)

    def merge_atom_arrays(self):
        atom_arrays = {}
        for domain_id in tqdm(self.domains):
            memmap_data_path = opj(self.memmap_path, domain_id)
            atom_array_path = opj(memmap_data_path, "reference.pyd")
            with open(atom_array_path, 'rb') as file:
                atom_array = pickle.load(file)
            atom_arrays[domain_id] = atom_array
        return atom_arrays


    def verify(self):
        # verify that all memmaps are valid
        errors = []
        for domain_id in tqdm(self.domains):
            memmap_data_path = opj(self.memmap_path, domain_id)

            for temp in self.temperatures:
                for rep in range(5):
                    memmap_path = opj(memmap_data_path, str(temp), f"rep{rep}.memmap")
                    try:
                        open_memmap(memmap_path, mode='r', dtype=np.float32)
                    except KeyboardInterrupt:
                        raise
                    except:
                        errors.append(memmap_path)

            reference_path = opj(memmap_data_path, "reference.pyd")
            try:
                with open(reference_path, 'rb') as file:
                    pickle.load(file)
            except KeyboardInterrupt:
                raise
            except:
                errors.append(reference_path)

        return errors

    def preprocess(self, num_workers=0):
        # organizes dataset into following structure
        # /domain_id
        #   reference.pdb
        #   /temp1 all-atom coords
        #     rep1.memmap
        #     rep2.memmap
        #     ...
        if num_workers == 0:
            arrays = []
            for domain_id in tqdm(self.domains):
                arr = self.write_memmap(domain_id)
                arrays.append(arr)
        else:
            arrays = process_map(self.write_memmap, self.domains, max_workers=num_workers)

        arrays = dict(arrays)
        with open(opj(self.base_path, 'atom_arrays.pyd'), 'wb') as f:
            pickle.dump(arrays, f)

    def __len__(self):
        return self.size_multiplier * len(self.domains)

    def __getitem__(self, idx):
        domain_id = self.domains[idx % len(self.domains)]
        random_temperature = np.random.choice(self.temperatures)
        random_replica = np.random.choice(range(5))

        atom_array = self.atom_arrays[domain_id]

        aa1 = deepcopy(atom_array)
        aa2 = deepcopy(atom_array)

        memmap_data_path = opj(self.memmap_path, domain_id)
        memmap_path = opj(memmap_data_path, str(random_temperature), f"rep{random_replica}.memmap")

        try:
            coord = open_memmap(memmap_path, mode='r', dtype=np.float32)
            num_frames = coord.shape[0]
        except:
            print(f"Error loading {memmap_path}")
            return self.__getitem__(idx + 1)

        random_frame_idx = np.random.choice(num_frames - 1)

        coord1 = coord[random_frame_idx]
        coord2 = coord[random_frame_idx + 1]

        coord2, _ = superimpose(coord1, coord2)

        aa1._coord = coord1
        aa2._coord = coord2

        dat1 = ProteinDatum.from_atom_array(aa1, header=dict(idcode=domain_id, resolution=None))
        dat2 = ProteinDatum.from_atom_array(aa2, header=dict(idcode=domain_id, resolution=None))

        if self.transform:
            for t in self.transform:
                (dat1, dat2) = t.transform([dat1, dat2])

        temp_token = TEMPERATURES.index(random_temperature) + 1 # we 1-index the temperature

        return [dat1, dat2, np.array([temp_token])]


    def get_trajectory(self, domain_id, temperature, replica):
        memmap_data_path = opj(self.memmap_path, domain_id)
        memmap_path = opj(memmap_data_path, str(temperature), f"rep{replica}.memmap")
        coord = open_memmap(memmap_path, mode='r', dtype=np.float32)

        data = []
        for i in range(coord.shape[0]):
            coords = coord[i]
            aa = deepcopy(self.atom_arrays[domain_id])
            aa._coord = coords
            data.append(aa)
        return stack(data)

    def get_crystal(self, domain_id):
        # atom_array = self.atom_arrays[domain_id]
        pdbfile = PDBFile.read(opj(self.base_path + '../experimental_structures', f"{domain_id}.pdb"))
        atom_array = pdbfile.get_structure()[0]
        dat = ProteinDatum.from_atom_array(atom_array, header=dict(idcode=domain_id, resolution=None))
        return dat
