


from tensorclouds.nn.spatial_convolution import CompleteSpatialConvolution, kNNSpatialConvolution
# from tensorclouds.nn.self_interaction import SelfInteraction
from tensorclouds.nn.layer_norm import EquivariantLayerNorm
from tensorclouds.tensorcloud import TensorCloud

import einops as ein

from tensorclouds.nn.time_embed import OnehotTimeEmbed
from tensorclouds.nn.layer_norm import EquivariantLayerNorm

import functools
import math
from flax import linen as nn
import jax
import jax.numpy as jnp
import e3nn_jax as e3nn
from typing import List, Tuple

from .interpolant import ConditionalProteinTwoSidedInterpolant



class NormSelfInteraction(nn.Module):

    irreps: e3nn.Irreps
    norm: bool = True

    @nn.compact
    def __call__(self, state: TensorCloud) -> TensorCloud:
        features = res = state.irreps_array

        features = e3nn.flax.Linear(self.irreps)(features)

        # gate_ = []
        # for (_, ir), x in zip(features.irreps, features.list):
        #     norms_sqr = jnp.sum(x**2, axis=-1)
        #     norms_ = jnp.sqrt(jnp.where(norms_sqr == 0.0, 1.0, norms_sqr))
        #     norms_ = jnp.where(norms_sqr == 0.0, 0.0, norms_)
        #     gate = e3nn.flax.MultiLayerPerceptron([norms_.shape[-1]], act=jax.nn.sigmoid)(norms_)
        #     gate_.append(gate)
        # gate = jnp.concatenate(gate_, axis=-1)
        # features = (gate * features)

        feature_norms = []
        for (_, ir), x in zip(features.irreps, features.list):
            norms_sqr = jnp.sum(x**2, axis=-1)
            norms_ = jnp.sqrt(jnp.where(norms_sqr == 0.0, 1.0, norms_sqr))
            norms_ = jnp.where(norms_sqr == 0.0, 0.0, norms_)
            feature_norms.append(norms_)
        feature_norms = jnp.concatenate(feature_norms, axis=-1)

        gate = e3nn.flax.MultiLayerPerceptron(
            [feature_norms.shape[-1]], act=jax.nn.sigmoid
        )(feature_norms)
        features = (gate * features)

        assert features.irreps.num_irreps == gate.shape[-1]

        if res.irreps == features.irreps:
            features = res + features
        else:
            features = e3nn.concatenate([res, features])
            features = e3nn.flax.Linear(self.irreps)(features)

        if self.norm: 
            features = EquivariantLayerNorm()(features) 

        return state.replace(
            irreps_array=features,
            mask_irreps_array=jnp.ones_like(gate).astype(jnp.bool_),
        )


class FullTensorSquareSelfInteraction(nn.Module):

    irreps: e3nn.Irreps
    norm: bool = True

    @nn.compact
    def __call__(self, state: TensorCloud) -> TensorCloud:
        features = state.irreps_array
        channel_mix = e3nn.tensor_square(features)
        features = e3nn.concatenate((features, channel_mix), axis=-1).regroup()

        invariants = features.filter(keep="0e").regroup()
        features *= e3nn.flax.MultiLayerPerceptron(
            [invariants.irreps.dim, features.irreps.num_irreps], act=jax.nn.silu
        )(invariants)
        features = e3nn.flax.Linear(self.irreps)(features)

        return state.replace(irreps_array=features)


from functools import reduce



class ChannelWiseTensorSquareSelfInteraction(nn.Module):

    irreps: e3nn.Irreps
    norm: bool = True

    @nn.compact
    def __call__(self, state: TensorCloud) -> TensorCloud:
        features = res = state.irreps_array
        
        dims = [irrep.mul for irrep in features.irreps]
        channel_mix = e3nn.tensor_square(features.mul_to_axis(dims[0])).axis_to_mul()
        features = e3nn.concatenate((features, channel_mix), axis=-1).regroup()

        scalars = features.filter(keep="0e").regroup()
        features *= e3nn.flax.MultiLayerPerceptron(
            [scalars.irreps.dim, features.irreps.num_irreps], 
            act=jax.nn.silu,
        )(scalars)
        features = e3nn.flax.Linear(self.irreps)(features)

        if res.irreps == features.irreps:
            features = res + features
        else:
            features = e3nn.concatenate([res, features])
            features = e3nn.flax.Linear(self.irreps)(features)

        if self.norm: 
            features = EquivariantLayerNorm()(features) 

        return state.replace(irreps_array=features)


class SegmentedTensorSquareSelfInteraction(nn.Module):

    irreps: e3nn.Irreps
    norm: bool = True
    # num_heads: int = 
    segment_size = 2

    @nn.compact
    def __call__(self, state: TensorCloud) -> TensorCloud:
        features = state.irreps_array

        channel_mix = [e3nn.tensor_square(features.filter(keep=ir).mul_to_axis(mul // self.segment_size)).axis_to_mul() for (mul, ir) in features.irreps.filter(drop='0e')]
        features = e3nn.concatenate([features, *channel_mix], axis=-1).regroup()

        invariants = features.filter(keep="0e").regroup()
        features *= e3nn.flax.MultiLayerPerceptron(
            [invariants.irreps.dim, features.irreps.num_irreps], act=jax.nn.silu
        )(invariants)
        features = e3nn.flax.Linear(self.irreps)(features)

        if self.norm: 
            features = EquivariantLayerNorm()(features) 

        return state.replace(irreps_array=features)



class SelfInteraction(nn.Module):

    irreps: e3nn.Irreps
    irreps_out: e3nn.Irreps = None
    depth: int = 1
    norm_last: bool = True

    base: nn.Module = SegmentedTensorSquareSelfInteraction

    @nn.compact
    def __call__(self, state: TensorCloud) -> TensorCloud:
        irreps_out = self.irreps_out
        if irreps_out is None:
            irreps_out = self.irreps
            
        for _ in range(self.depth - 1):
            state = self.base(self.irreps)(state)
            
        state = self.base(irreps_out, norm=self.norm_last)(state)

        return state


class DeepJumpBlock(nn.Module):

    irreps: e3nn.Irreps
    k: int = 0
    k_seq: int = 0
    radial_cut: float = 24.0
    move: bool = False

    @nn.compact
    def __call__(self, x):
        res = x

        x = SelfInteraction(self.irreps)(x)
        x = kNNSpatialConvolution(
            irreps_out=self.irreps,
            k=self.k,
            k_seq=self.k_seq,
            radial_cut=self.radial_cut,
            radial_bins=42,
            radial_basis="gaussian",
            move=self.move,
        )(x)

        if res.irreps == x.irreps:
            x = x.replace(irreps_array=x.irreps_array + res.irreps_array)
        else:
            x = x.replace(
                irreps_array=e3nn.flax.Linear(self.irreps)(e3nn.concatenate([res.irreps_array, x.irreps_array]))
            )
        x = x.replace(irreps_array=EquivariantLayerNorm()(x.irreps_array))

        return x
    


class DeepJumpNetwork(nn.Module):

    irreps: e3nn.Irreps
    depth: int

    k: int = 0
    k_seq: int = 0
    radial_cut: float = 32.0

    headers: Tuple[e3nn.Irreps] = tuple()
    header_depth: int = 1

    timesteps: int = 100
    move: bool = False
    
    num_temp: int = 0

    @nn.compact
    def __call__(self, x, t=None, cond=None, seq=None, temp=None):

        if cond is not None:
            x = x.replace(
                irreps_array=e3nn.concatenate([x.irreps_array, cond], axis=-1).regroup()
            )
        
        if seq is not None:
            seq_embed = nn.Embed(
                num_embeddings=23,
                features=e3nn.Irreps(self.irreps).filter(keep='0e').num_irreps,
            )(seq)

            x = x.replace(
                irreps_array=e3nn.concatenate([x.irreps_array, seq_embed], axis=-1).regroup()
            )

        if temp is not None:
            temp = nn.Embed(num_embeddings=self.num_temp, features=e3nn.Irreps(self.irreps).filter(keep='0e').num_irreps)(temp)
            x = x.replace(
                irreps_array=e3nn.concatenate([x.irreps_array.filter('0e') + temp, x.irreps_array.filter(drop='0e')], axis=-1)
            )
            
        if t is not None:
            x = OnehotTimeEmbed(self.timesteps, (0.0, 1.0))(x, t)

        x = x.replace(irreps_array=e3nn.flax.Linear(self.irreps)(x.irreps_array))
        x = SelfInteraction(self.irreps)(x)

        for _ in range(self.depth):
            x = DeepJumpBlock(
                self.irreps,
                k=self.k,
                k_seq=self.k_seq,
                radial_cut=self.radial_cut,
                move=self.move,
            )(x)

        if self.headers:
            x = SelfInteraction(self.irreps, depth=self.header_depth, irreps_out=self.headers[-1], norm_last=False)(x)
            x = x.replace(irreps_array=x.irreps_array * jnp.array([1, 0] + 12 * [1])[None])
            return [ x ] 
        
        return SelfInteraction(self.irreps)(x)


class DeepJump(nn.Module):

    irreps: str
    depth: int
    cond_depth: int
    header_depth: int

    k: int
    k_seq: int
    radial_cut: float

    leading_shape: Tuple
    var_features: int
    var_coords: int
    timesteps: int

    def setup(self):

        cond_net = DeepJumpNetwork(
            irreps = e3nn.Irreps(self.irreps),
            depth = self.cond_depth,
            k = self.k,
            k_seq=self.k_seq,
            radial_cut=self.radial_cut,
            headers = [],
            move=False,
            num_temp = 6,
        )

        net = DeepJumpNetwork(
            irreps = e3nn.Irreps(self.irreps),
            depth = self.depth,
            k = self.k,
            k_seq=self.k_seq,
            radial_cut=self.radial_cut,
            header_depth = self.header_depth,
            headers = ['14x1e'] * 1,
            move=True,
        )

        self.interpolant = ConditionalProteinTwoSidedInterpolant(
            net=net,
            cond_net=cond_net,
            leading_shape=self.leading_shape,
            var_features=self.var_features,
            var_coords=self.var_coords,
            timesteps=self.timesteps,
        )

    def sample(self, prot, num_steps=None, eps=1.0, temp=None):
        return self.interpolant.sample(prot, num_steps=num_steps, eps=eps, temp=temp)

    def __call__(self, prot0, prot1, temp=None):
        return self.interpolant(prot0, prot1, temp=temp)
