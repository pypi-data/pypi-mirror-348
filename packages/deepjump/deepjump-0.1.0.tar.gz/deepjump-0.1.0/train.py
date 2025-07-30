import sys

sys.path.append('../')


from absl import app
from omegaconf import OmegaConf

import numpy as np

import wandb
import os

import wandb

from absl.flags import FLAGS
from absl import flags

flags.DEFINE_string('hash', None, 'wandb hash')
flags.DEFINE_string('iter', None, '#iteration in restarting cycles')
flags.DEFINE_string('device', None, 'CUDA device to run on')

from learnax.registry import Registry

import pprint
# import jax
# jax.config.update('jax_disable_jit', True)

def main(argv):
    print("""\n
    _________                 ________
    ___  __ \_______________________  /___  ________ ___________
    __  / / /  _ \  _ \__  __ \__  / /_  / / /_  __ `__ \__  __
    _  /_/ //  __/  __/_  /_/ / /_/ / / /_/ /_  / / / / /_  /_/ /
    /_____/ \___/\___/_  .___/\____/  \__,_/ /_/ /_/ /_/_  .___/
                    /_/                               /_/
    \n""")

    hash = FLAGS.hash
    device = FLAGS.device

    os.environ['CUDA_VISIBLE_DEVICES'] = str(device)
    os.environ['XLA_PYTHON_CLIENT_PREALLOCATE'] = 'true'
    os.environ['XLA_PYTHON_CLIENT_MEM_FRACTION'] = '.99'

    project = 'deepjump'
    entity = 'molecular-machines'


    from build import build_pipeline

    if hash == None:
        cfg = OmegaConf.load(f'./train_config.yml')
        run = Registry(project).new_run(cfg)
    else:
        config_path = f'{os.environ.get("TRAINAX_REGISTRY_PATH")}/{project}/{hash}/config.yml'
        cfg = OmegaConf.load(config_path)
        run = Registry(project).restore_run(hash)

    pprint.pp(OmegaConf.to_container(cfg))
    trainer = build_pipeline(cfg, run=run)

    if hash == None:
        trainer.init()
    else:
        state_path = f'{os.environ.get("TRAINAX_REGISTRY_PATH")}/{project}/{trainer.run.id}/checkpoints/state_latest.pyd'
        if not os.path.exists(state_path):
            raise FileNotFoundError(f'NO LATEST TRAINER STATE FOUND AT {state_path}')
        print('LOADING LATEST TRAINER STATE!')
        train_state = run.get_train_state()
        trainer.init(train_state)

    trainer.train()


if __name__ == "__main__":
    app.run(main)
