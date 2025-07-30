
from deeptime.decomposition import TICA
from deeptime.clustering import KMeans
from deeptime.markov import TransitionCountEstimator, pcca
from deeptime.markov.msm import MaximumLikelihoodMSM

import numpy as np 

def embed_traj(traj):
    ca = [step._coord[step.atom_name == 'CA'] for step in traj]
    num_ca = len(ca[0])
    # if p=='trpcage':
        # num_ca -= 4
    inds = np.triu_indices(num_ca,1)
    feats = np.asarray([np.linalg.norm(c[:,np.newaxis,:]-c[np.newaxis,:,:],axis=2)[inds] for c in ca])
    return feats

def compute_tica(trajs, lagtime, numTIC):
    tica = TICA(dim=numTIC)
    trajs = [embed_traj(traj) for traj in trajs]
    for traj in trajs:
        tica.partial_fit((traj[:-lagtime], traj[lagtime:]))
    return tica.fetch_model()

def get_clusters(feats, Nclust):
  clusters = KMeans(
      n_clusters=Nclust, 
      init_strategy='uniform',
      n_jobs=8
  ).fit(feats)
  return clusters.fetch_model()


from deeptime.markov import TransitionCountEstimator, pcca
from deeptime.markov.msm import MaximumLikelihoodMSM


def compute_msm(clusters_traj, num_clusters):
  lags = []
  models = []
  GSs = []
  for l in range(5, 35 + 1, 5):
    counts = TransitionCountEstimator(lagtime=l, count_mode='sliding', n_states=num_clusters).fit_fetch(clusters_traj)
    model = MaximumLikelihoodMSM(allow_disconnected=True).fit_fetch(counts)
    # This can skip unconnected, we then reintroduce them
    GS = np.zeros(num_clusters)

    np.add.at(GS, model.state_symbols(), model.stationary_distribution)
    lags.append(l)
    models.append(model)
    GSs.append(GS)
  return lags, models, GSs


CA_INDEX = 1

def crystal_rmsd(crystal, traj):
    ca_traj = traj[:, traj.atom_name == 'CA']
    crystal_ca = crystal.atom_coord[:, CA_INDEX]
    aligned_ca_traj = superimpose(crystal_ca, ca_traj)[0]
    return rmsd(crystal_ca, aligned_ca_traj)

def radius_of_gyration(traj):
    return gyration_radius(traj)
