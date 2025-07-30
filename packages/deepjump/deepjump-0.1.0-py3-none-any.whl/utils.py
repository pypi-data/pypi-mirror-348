from biotite.structure import stack



def prepare_data(dataset, proteins):
    from data.md_cath import mdCATHDataset
    from data.fast_folding import FastFoldingDataset
    from torch.utils.data import DataLoader

    if dataset == 'mdCATH':
        dataset = mdCATHDataset(
            base_path = '/mnt/timebucket/molmach_db/mdCATH/',
            domains=proteins,
            size_multiplier=10,
        )
    elif dataset == 'fast-folding':
        ff_dataset_path = '/mas/projects/molecularmachines/db/fast-folding/'
        dataset = FastFoldingDataset(
            base_path=ff_dataset_path,
            tau=1,
            proteins=proteins,
        )
    elif dataset == 'atlas':
        dataset = ATLASDataset(
            proteins=proteins,
        )
    else:
        raise ValueError(f'Unknown dataset: {dataset}')

    return dataset


import io
import numpy as np
import biotite.structure as struc
import biotite.structure.io.pdb as pdb
import biotite.sequence as seq
from biotite.structure import AtomArray

# Two-residue template PDB string (only backbone atoms are used)


from moleculib.protein.alphabet import HELIX_ROTAMERS, HELIX_BACKBONE


HELIX_ATOM_ARRAYS = {
    k: pdb.get_structure(pdb.PDBFile.read(io.StringIO(v)), 1) for k, v in HELIX_ROTAMERS.items()
}

def parse_template():
    """
    Parse the two-residue template and extract backbone (N, CA, C, O) coordinates
    for residue 1 and residue 2.
    Returns:
        template_res1, template_res2: each a (4,3) numpy array.
    """
    pdb_file = io.StringIO(HELIX_BACKBONE)
    pdb_obj = pdb.PDBFile.read(pdb_file)
    atom_array = pdb.get_structure(pdb_obj, 1)
    
    # We use only the backbone atoms.
    res1 = atom_array[atom_array.res_id == 1]
    res2 = atom_array[atom_array.res_id == 2]

    return res1, res2

import biotite
from copy import deepcopy

def build_alpha_helix(sequence):
    n = len(sequence)
    template_res1, template_res2 = parse_template()
    
    residues = []
    residues.append(template_res1.copy())
    residues.append(template_res2.copy())

    # template_fragment = np.vstack([template_res1, template_res2])

    for i in range(2, n):
        _, transformation = struc.superimpose(
            residues[-1][np.isin(residues[-1].atom_name, ["N", "CA", "C", "O"])]._coord, 
            template_res1._coord
        )
        new_residue = transformation.apply(deepcopy(template_res2))
        new_residue.res_id = [i+1] * len(new_residue.res_id)
        residues.append(new_residue)

    for i in range(n):

        res = biotite.sequence.ProteinSequence.convert_letter_1to3(sequence[i])
        sidechain_atom_array = HELIX_ATOM_ARRAYS[res].copy()

        template_backbone = sidechain_atom_array[
            np.isin(sidechain_atom_array.atom_name, ["N", "CA", "C", "O"]) &
            ~np.isin(sidechain_atom_array.atom_name, ["OXT", "HXT"])  
        ]

        _, transformation = struc.superimpose(
            residues[i][np.isin(residues[i].atom_name, ["N", "CA", "C", "O"])]._coord, 
            template_backbone._coord
        )
        
        new_residue = transformation.apply(sidechain_atom_array)
        new_residue.res_id = [i+1] * len(new_residue.res_id)

        residues[i] = new_residue


    return sum(residues[1:], residues[0])