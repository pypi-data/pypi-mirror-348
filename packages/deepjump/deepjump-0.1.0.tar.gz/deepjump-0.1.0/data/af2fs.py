

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
import biotite
import random

class AF2FSDB:

    def __init__(
        self,
        base_path = '/mas/projects/molecularmachines/deepjump/AF2_foldseek',
        proteins=None,
        transform = []
    ):
        self.base_path = base_path

        dir = self.base_path
        if proteins == None:
            proteins = glob.glob(os.path.join(dir, "*.pdb"))
        self.proteins = proteins
        self.transform = transform

    def __len__(self):
        return len(self.proteins)

    def __getitem__(self, idx):
        file = PDBFile.read(self.proteins[idx])
        struct = file.get_structure(model=1)
        datum = ProteinDatum.from_atom_array(struct)
        if self.transform:
            for t in self.transform:
                datum = t.transform(datum)

        return [datum, datum, np.array([0])]
