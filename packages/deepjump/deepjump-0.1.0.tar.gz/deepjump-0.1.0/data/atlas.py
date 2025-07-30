
class ATLASDataset:
    
    def __init__(
        self, 
        base_path='/mas/projects/molecularmachines/db/ATLAS_db/',
        min_seq_len=0, max_seq_len=500,
        proteins=None,
    ):
        self.base_path = base_path
        # self.data_path = os.path.join(base_path, 'data')
        
        # proteins = os.listdir(self.base_path)
        # proteins = [protein for protein in proteins if os.path.exists(os.path.join(self.base_path, protein, f"{protein}.pdb"))]
        # self.proteins = proteins

        with open(os.path.join(self.base_path, 'atom_arrays.pyd'), 'rb') as f:
            self.atom_arrays = pickle.load(f)
            self.atom_arrays = {
                k: v for k, v in self.atom_arrays.items() if min_seq_len <= len(v[v.atom_name == 'CA']) <= max_seq_len
            }
        
        if proteins != None:
            self.atom_arrays = {k: v for k, v in self.atom_arrays.items() if k in proteins}

        self.proteins = list(self.atom_arrays.keys())


    def get_crystal(self, protein):
        return self.atom_arrays[protein]

    def get_trajectories(self, protein):
        trajs = []
        template = self.atom_arrays[protein]
        for i in range(3):
            replica_path = f'{protein}_prod_R{i}_fit.xtc'
            replica_path = os.path.join(self.data_path, protein, replica_path)
            traj = biotite.structure.io.xtc.XTCFile.read(replica_path)
            traj = traj.get_structure(template)
            trajs.append(traj)
        return trajs
