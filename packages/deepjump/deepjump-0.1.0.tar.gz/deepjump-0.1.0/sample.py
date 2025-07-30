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
from jax.tree_util import tree_map
import einops as ein

from functools import partial
import jax.numpy as jnp

def prepare_model(
    weights,
    temp,
    config,
    init_data,
):
    from build import build_model, build_dataset

    # config.model.leading_shape = dataset.pad.pad_size
    config.model.leading_shape = len(init_data[0])
    batch_size = len(init_data)

    if temp != 0:
        temp = config.data.temperatures.index(temp) + 1

    model = build_model(config)
    params = { 'params': weights }

    @partial(jax.pmap, in_axes=(0, 0))
    def _sample_pmap(keys, prots):
        return jax.vmap(
            lambda k, p: model.apply(
                params, p, temp=jnp.array([temp]), rngs={'params': k}, method='sample', num_steps=150,
            )
        )(keys, prots)

    device_count = jax.device_count()

    def _sample(key, batch):
        batch = tree_map(lambda v: ein.rearrange(v, '(p q) ... -> p q ...', p=device_count, q=batch_size // device_count) if not (v is None) else v, batch)
        keys = ein.rearrange(jax.random.split(key, batch_size), '(p q) ... -> p q ...', p=device_count, q=batch_size // device_count)

        out = _sample_pmap(keys, batch)
        out = tree_map(lambda v: ein.rearrange(v, 'p q ... -> (p q) ...'), out)
        return out

    init_key = jax.random.PRNGKey(42)
    print(f'Compiling Sampling...')
    _sample(init_key, tree_stack(init_data))

    return _sample


def rollout(sampler, key, init_data, num_steps):
    traj = [init_data]
    out = tree_stack(init_data)
    for _ in tqdm(range(num_steps)):
        key, subkey = jax.random.split(key)
        out, _ = sampler(subkey, out)
        traj.append(tree_unstack(out))
    return list(zip(*traj))


import os
from utils import prepare_data, build_alpha_helix

import biotite
from biotite.structure import stack
from moleculib.protein.datum import ProteinDatum


def main(argv):
    config = OmegaConf.load(FLAGS.config)

    import pprint
    pprint.pprint(OmegaConf.to_container(config))

    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  # see issue #152
    os.environ["CUDA_VISIBLE_DEVICES"] = config.env.device
    os.environ["XLA_PYTHON_CLIENT_PREALLOCATE"] = "true"  # add this
    os.environ["XLA_PYTHON_CLIENT_ALLOCATOR"] = "platform"

    id, checkpoint = config.model.id, config.model.checkpoint
    temp = config.model.temperature

    seed = config.sample.seed
    batch_size, num_steps = config.sample.batch_size, config.sample.num_steps
    repeat, mode = config.sample.repeat, config.sample.mode


    run = Registry('deepjump').fetch_run(id)
    model_config = run.get_config()
    weights = run.get_weights(checkpoint)

    for protein in config.data.proteins:
        print(f'Sampling {protein}')

        dataset = prepare_data(config.data.dataset, [protein])

        if mode == 'crystal':
            init_data = [ProteinDatum.from_atom_array(dataset.get_crystal(protein))] * batch_size
            loader = [ init_data ] * num_steps


        elif mode == 'chain':
            from torch.utils.data import DataLoader            
            # with open(f'.metrics_cache/{protein}/tica.pyd', 'rb') as file:
            #     metrics = pickle.load(file)
            metrics = dataset.get_metrics(protein)
            helix_cluster = metrics['clusters'][128]['helix_cluster']
            dataset.clusters[protein] = { 128: {0: dataset.clusters[protein][128][int(helix_cluster.item())]} }
            loader = DataLoader(dataset, batch_size=batch_size, collate_fn=lambda x:[x_[0] for x_ in x], num_workers=0)

            # aa = dataset.atom_arrays[protein]
            # _, seq = biotite.structure.get_residues(aa)
            # seq = ''.join([biotite.sequence.ProteinSequence.convert_letter_3to1(seq_).upper() for seq_ in seq])
            # chain = ProteinDatum.from_atom_array(build_alpha_helix(seq))
            # init_data = [ chain ] * batch_size
            # loader = [ init_data ] * num_steps    

        elif mode == 'default':
            from torch.utils.data import DataLoader            
            loader = DataLoader(dataset, batch_size=batch_size, collate_fn=lambda x:[x_[0] for x_ in x], num_workers=0)
        

        sampler = prepare_model(weights, temp, model_config, loader.__iter__().__next__())

        key = jax.random.PRNGKey(seed)
        trajs = []

        loader = iter(loader)
        for _ in range(repeat):
            data = next(loader)
            trajs.extend(rollout(sampler, key, data, num_steps))

        import numpy as np

        random_name_gen = lambda: ''.join([chr(np.random.randint(65, 91)) for _ in range(6)])
        run.clear_dir(f'samples/{checkpoint}/{protein}/{mode}')

        for traj in trajs:
            samples_path = f'samples/{checkpoint}/{protein}/{mode}/{id}_{random_name_gen()}_traj.pyd'
            atom_array = stack([p.to_atom_array() for p in traj])
            run.save(samples_path, atom_array)
            print(f'saved {samples_path}')

    print('Done.')

flags.DEFINE_string('config', './sample_config.yml', 'config yml file')

if __name__ == "__main__":
    app.run(main)
