import jax
from data.md_cath import mdCATHDataset
import os

from moleculib.protein.transform import ProteinTransform
from tensorclouds.loss.losses import LossPipe, StochasticInterpolantLoss, TensorCloudMatchingLoss

from nn.deepjump import DeepJump, DeepJumpEnsemble
import optax
import wandb


from learnax.trainer import Trainer

from tensorclouds.loss.losses import LossFunction
from tensorclouds.tensorcloud import TensorCloud

import einops as ein
from tensorclouds.nn.utils import safe_norm
import jax.numpy as jnp


def build_model(cfg):
    if cfg.model.type == 'ensemble':
        return DeepJumpEnsemble(
            irreps=cfg.model.irreps,
            depth=cfg.model.depth,
            cond_depth=cfg.model.cond_depth,
            header_depth=cfg.model.header_depth,
            k=cfg.model.k,
            k_seq=cfg.model.k_seq,
            radial_cut=cfg.model.radial_cut,
            leading_shape=(cfg.model.leading_shape,),
            var_features=cfg.model.var_features,
            var_coords=cfg.model.var_coords,
            timesteps=cfg.model.timesteps,
        )
    elif cfg.model.type == 'dynamics':
        return DeepJump(
            irreps=cfg.model.irreps,
            depth=cfg.model.depth,
            cond_depth=cfg.model.cond_depth,
            header_depth=cfg.model.header_depth,
            k=cfg.model.k,
            k_seq=cfg.model.k_seq,
            radial_cut=cfg.model.radial_cut,
            leading_shape=(cfg.model.leading_shape,),
            var_features=cfg.model.var_features,
            var_coords=cfg.model.var_coords,
            timesteps=cfg.model.timesteps,
        )


from data.af2fs import AF2FSDB
from data.md_cath import mdCATHDataset
from data.hybrid import HybridDataset

from moleculib.protein.transform import ProteinCrop, ProteinPad

from data.misato import MISATO
import numpy as np

def build_dataset(cfg):

    transforms = [
        ProteinCrop(cfg.data.crop_size),
        ProteinPad(cfg.data.crop_size),
    ]
    
    if cfg.data.dataset == 'mdCATH':
        return mdCATHDataset.split(
            factor=0.9,
            base_path ='/mnt/timebucket/molmach_db/mdCATH/',
            size_multiplier=40,
            transform=transforms,
            temperatures=cfg.data.temperatures,
            max_seq_len=cfg.data.crop_size,
            tau=cfg.data.tau,
        )
    
    elif cfg.data.dataset == 'misato':
        return MISATO(
            max_num_chains = cfg.data.max_num_chains,
            max_seq_len = cfg.data.crop_size,
            max_lig_len = cfg.data.lig_crop_size,
            filter_unk = True,
            transform=transforms,
        ), None
    
    # elif cfg.data.dataset == 'hybrid':
        # return HybridDataset(
        #     [
        #         AF2FSDB(transform=transforms),
        #         mdCATHDataset(
        #             base_path ='/mnt/timebucket/molmach_db/mdCATH/',
        #             size_multiplier=20,
        #             transform=transforms,
        #             temperatures=cfg.data.temperatures,
        #             max_seq_len=cfg.data.crop_size,
        #         )
        #     ],
        #     weights=[0.2, 0.8],
        #     epoch_size=cfg.train.batch_size * 500
        # ), None



class VectorMapLoss(LossFunction):
    def __init__(
        self,
        weight=1.0,
        start_step=0,
        max_radius: float = 32.0,
        max_error: float = 800.0,
        norm_only=False,
    ):
        super().__init__(weight=weight, start_step=start_step)
        self.norm_only = norm_only
        self.max_radius = max_radius
        self.max_error = max_error

    def _call(
        self, rng_key, prediction: TensorCloud, ground: TensorCloud
    ):
        # gotta fix this eventually
        ground = prediction.target
        prediction = prediction.prediction

        def all_atom_coord(tc):
            base_coord = tc.coord
            vector_coord = tc.irreps_array.filter("1e").array
            vector_coord = ein.rearrange(vector_coord, "... (a c) -> ... a c", c=3)
            all_atom_coords = base_coord[..., None, :] + vector_coord
            return all_atom_coords

        all_pred = all_atom_coord(prediction)
        all_ground = all_atom_coord(ground)

        all_atom_coords = ein.rearrange(all_pred, "... a c -> (... a) c")
        all_atom_coords_ground = ein.rearrange(all_ground, "... a c -> (... a) c")

        all_atom_mask = ground.mask_coord
        all_atom_mask = ein.repeat(all_atom_mask, 'i -> i c', c=ground.irreps_array.filter("1e").shape[-1] // 3)
        all_atom_mask = ein.rearrange(all_atom_mask, "... a -> (... a)")

        vector_map = lambda x: ein.rearrange(x, "i c -> i () c") - ein.rearrange(
            x, "j c -> () j c"
        )

        cross_mask = ein.rearrange(all_atom_mask, "i -> i ()") & ein.rearrange(
            all_atom_mask, "j -> () j"
        )

        vector_maps = vector_map(all_atom_coords)
        vector_maps_ground = vector_map(all_atom_coords_ground)
        cross_mask = cross_mask & (safe_norm(vector_maps_ground) < self.max_radius)

        if self.norm_only:
            vector_maps = safe_norm(vector_maps)[..., None]
            vector_maps_ground = safe_norm(vector_maps_ground)[..., None]

        error = optax.huber_loss(vector_maps, vector_maps_ground, delta=1.0).mean(-1)
        if self.max_error > 0.0:
            error = jnp.clip(error, 0.0, self.max_error)

        error = (error * cross_mask.astype(error.dtype)).sum((-1, -2)) / (
            cross_mask.sum((-1, -2)) + 1e-6
        )
        error = error.mean()
        error = error * (cross_mask.sum() > 0).astype(error.dtype)

        metrics = dict(
            vector_map_loss=error,
        )

        return prediction, error, metrics



def build_loss(cfg):
    # loss = TensorCloudMatchingLoss(weight=1)
    loss = VectorMapLoss(weight=1)
    return [loss]

def build_pipeline(cfg, run):

    train_ds, val_ds = build_dataset(cfg)
    # print('train_ds:', len(train_ds.domains))
    # print('val_ds:', len(val_ds.domains))

    cfg.model.leading_shape = cfg.data.crop_size

    model = build_model(cfg)
    losses = build_loss(cfg)
    jax.config.update("jax_disable_jit", cfg.env.disable_jit)
    jax.config.update("jax_debug_nans", cfg.env.debug_nans)

    learning_rate = optax.linear_schedule(
        init_value=cfg.train.lr_start,
        end_value=cfg.train.lr_end,
        transition_steps=cfg.train.lr_steps,
        transition_begin=1
    )

    trainer = Trainer(
        model=model,
        learning_rate=learning_rate,
        losses=LossPipe(loss_list=losses),
        seed=cfg.train.seed,
        train_dataset=train_ds,
        num_epochs=cfg.train.num_epochs,
        batch_size=cfg.train.batch_size,
        num_workers=cfg.train.num_workers,
        save_every=cfg.train.save_every,
        run=run,
        save_model=None,
        single_datum=cfg.train.single_datum,
        registry='deepjump',
        val_dataset=val_ds,
        val_every=cfg.train.val_every,
    )

    return trainer
