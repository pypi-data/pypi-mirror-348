from typing import Optional, Tuple

import chex
import jax
import jax.numpy as jnp
from flax import linen as nn
import e3nn_jax as e3nn

from tensorclouds.tensorcloud import TensorCloud
from tensorclouds.random.normal import NormalDistribution

from typing import Tuple
from functools import partial

from tensorclouds.data.protein import protein_to_tensor_cloud, tensor_cloud_to_protein


@chex.dataclass
class DriftPrediction:
    prediction: TensorCloud
    target: TensorCloud


class TensorCloudTwoSidedInterpolant(nn.Module):

    network: nn.Module # must output two tensorclouds
    leading_shape: Tuple[int]
    var_features: float = 1.0
    var_coords: float = 1.0


    def sample(
        self,
        x0=None,
        cond=None,
        eps: float = 1.0,
        num_steps: int = 1000,
    ) -> Tuple[TensorCloud, TensorCloud]:
        dt = 1.0 / num_steps

        def update_one_step(
            network: nn.Module, zt: TensorCloud, t: float
        ) -> TensorCloud:
            x1_hat = network(zt, t, cond=cond)[0]
            s = t + dt
            coeff = (1 / (1 - t + 1e-4))
            next_zt = coeff * (s - t) * x1_hat + coeff * (1 - s) * zt
            next_zt = next_zt.centralize()
            return next_zt, next_zt

        z = NormalDistribution(
            irreps_in=x0.irreps,
            irreps_mean=e3nn.zeros(x0.irreps),
            irreps_scale=self.var_features,
            coords_mean=jnp.zeros(3),
            coords_scale=self.var_coords,
        ).sample(
            self.make_rng(),
            leading_shape=self.leading_shape,
            mask_coord=x0.mask_coord,
            mask_features=x0.mask_irreps_array,
        )
        x0 = (x0 + z)

        return nn.scan(
            update_one_step,
            variable_broadcast="params",
            split_rngs={"params": True},
        )(self.network, x0, jnp.arange(0, 1, dt))

    def compute_xt(
        self, t: float, x0: TensorCloud, x1: TensorCloud, eps: float = 1e-4
    ) -> TensorCloud:
        """Computes xt at time t."""
        z = NormalDistribution(
            irreps_in=x1.irreps,
            irreps_mean=e3nn.zeros(x1.irreps),
            irreps_scale=self.var_features,
            coords_mean=jnp.zeros(3),
            coords_scale=self.var_coords,
        ).sample(
            self.make_rng(),
            leading_shape=self.leading_shape,
            mask_coord=x1.mask_coord,
            mask_features=x1.mask_irreps_array,
        )
        x0 = (x0 + z)
        interpolant = (1 - t) * x0 + t * x1
        return interpolant, (x1 + (-x0))

    def __call__(
        self,
        x0: TensorCloud,
        x1: TensorCloud,
        is_training=False,
        cond: TensorCloud = None,
        eps: float = 1e-4,
    ):
        # Sample time.
        t = jax.random.uniform(self.make_rng(), minval=0.0 + eps, maxval=1.0 - eps)
        x0 = x0.centralize()
        x1 = x1.centralize()

        # Compute xt at time t.
        xt, b = self.compute_xt(t, x0, x1)
        # drift = self.dtIt(x0, x1) + self.gamma_dot(t) * z

        # Compute the predicted velocity ut(xt) at time t and location xt.
        x1_hat = self.network(xt, t, cond=cond)[0]
        # x1_hat = x1_hat.replace(coord=x1_hat.coord + x0.coord)

        return DriftPrediction(prediction=x1_hat, target=x1)
        




class ProteinTwoSidedInterpolant(nn.Module):

    net: nn.Module

    leading_shape: Tuple[int]
    var_features: float
    var_coords: float
    timesteps: int


    def setup(self):
        self.interpolant = TensorCloudTwoSidedInterpolant(
            network=self.net,
            leading_shape=self.leading_shape,
            var_features=self.var_features,
            var_coords=self.var_coords,
        )

    def sample(
        self,
        prot,
        eps=1.0,
        num_steps=1000,
    ):
        x0 = protein_to_tensor_cloud(prot)
        vecs = x0.replace(irreps_array=x0.irreps_array.filter('1e'))
        cond = x0.irreps_array.filter('0e')
        out, traj = self.interpolant.sample(
            vecs,
            eps=eps,
            cond=cond,
            num_steps=num_steps
        )
        prot.atom_coord = tensor_cloud_to_protein(out, protein=prot).atom_coord
        return prot, traj


    def __call__(self, prot0, prot1, is_training=False):
        x0 = protein_to_tensor_cloud(prot0)
        x1 = protein_to_tensor_cloud(prot1)
        scalars = x0.irreps_array.filter('0e')
        vecs0 = x0.replace(irreps_array=x0.irreps_array.filter('1e'))
        vecs1 = x1.replace(irreps_array=x1.irreps_array.filter('1e'))
        return self.interpolant(vecs0, vecs1, cond=scalars)




class ConditionalProteinTwoSidedInterpolant(ProteinTwoSidedInterpolant):

    net: nn.Module
    cond_net: nn.Module

    leading_shape: Tuple
    var_features: int
    var_coords: int
    timesteps: int

    def make_conditional(self, x0, **kwargs):
        return self.cond_net(x0, seq=x0.label, **kwargs).irreps_array

    def sample(
        self,
        prot,
        num_steps = None,
        eps = 1.0,
        temp = None,
    ):
        if num_steps == None:
            num_steps = self.timesteps
        x0 = protein_to_tensor_cloud(prot)
        vecs = x0.replace(irreps_array=x0.irreps_array.filter('1e'))
        out, traj = self.interpolant.sample(
            vecs,
            cond=self.make_conditional(x0, temp=temp),
            num_steps=num_steps,
            eps=eps,
        )
        out = out.replace(label=x0.label)
        new_prot = tensor_cloud_to_protein(out)
        return new_prot, traj

    def __call__(self, prot0, prot1, temp=0):
        x0 = protein_to_tensor_cloud(prot0)
        x1 = protein_to_tensor_cloud(prot1)
        vec_cloud0 = x0.replace(irreps_array=(x0.irreps_array.filter("1e")))
        vec_cloud1 = x1.replace(irreps_array=x1.irreps_array.filter("1e"))
        cond = self.make_conditional(x0, temp=temp)

        maybe_mask = (temp > 0).astype(jnp.float32)
        cond = e3nn.concatenate(
            [cond.filter(keep="0e"), cond.filter(keep="1e") * maybe_mask],
            axis=-1
        )

        return self.interpolant(vec_cloud0, vec_cloud1, cond=cond)


