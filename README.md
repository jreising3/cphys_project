# Tight Binding and Anderson Localization on Arbitrary Graphs with Anharmonic Time Dependence 






# Introduction
This project adds to the prior work "Tight Binding and Anderson Localization on Arbitrary Graphs", which implemented the tight binding model for an electron on an arbitrary graph structure. Here we incorprate a anharmonic time dependence term into our hamilitonian, while also including [Anderson Localization](https://en.wikipedia.org/wiki/Anderson_localization) in the same manner as the prior work. We calculate the thermodynamic quanties like [Von Neumann entropy] (https://en.wikipedia.org/wiki/Entropy_(information_theory))

# Numerical Approach


## Tight Binding Model

The tight binding model is a way calculating electronic band structure. In this model the wave function is written for free atoms i.e LACO (Linear Combination of Atomic Oribtials) that satify Bloch's Thoerem. 

## The Tight Binding Hamiltonian

The Hamiltonian for the tight binding model for a single electron can be written as follows:

```math
\langle n | H | m \rangle = H_{n,m} = \underbrace{\epsilon \delta_{n,m}}_\textrm{binding} \underbrace{- t(\delta_{n+1,m} + \delta_{n-1,m} )}_\textrm{hopping}
```

where $H$ is the electron Hamiltonian, $\epsilon$ is the binding energy, $\delta$ is the Kronecker delta, and $t$ is the hopping parameter. $n$ and $m$ refer to states associated with a particular site as in the tight binding formalism.

Anderson localization can be demonstrated on this model when the diagonal of the Hamiltonian $H$ is randomized and if values of $\epsilon$ are randomly sampled from a uniform distribution on $[-W, W]$ where $W$ is known as the disorder parameter. In this case, larger $W$ correlates with increased localization.
## Time Evoultion

In the time indepent picture the using is evolved using the time evolution operator $U(t)$

$$ | \psi(t) \rangle = \exp(-i H t / \hbar) | \psi(0) \rangle $$

However in our model we add in a time depent term into our hamilitoian. In order to deal with this we split the hamilitonian up into the static and time depent part. The static part is update via the equation above. For the time depent part we time-depenet perturbation theory to calculate coffects for the time depent state using the following formula. Note in our model the only time depent terms contribute to the diagonal part of the tightbinding chain.

$$ c(t)= -\frac{i}{\hbar} \int^{t}_{0} dt'\langle n |H('t)| n\rangle $$

# Basic Use
code examples can be found in [summary.ipynb](summary.ipynb).

One can create a instance of the AndersonGraph object and then make a ring using NetworkX graph. Then feed the ring in as one of the arguments in the AndersonGraph constructor. Below we show a simple example. 

```python
import AndersonGraph as ag # The exact form of this may change based on the relative location of AndersonGraph.py

N = 80 # Define number of sites
psi_0 = np.zeros(N)
psi_0[N//2] = 1 # Create wave function

ring = nx.grid_graph(dim=[N], periodic=True) # Create ring

anderson_ring = ag.AndersonGraph(graph=ring, psi_0=psi_0, eps_range=[-1, 1], alpha = 0.5) # Construct AndersonGraph object

anderson_ring.plot_density(t=17) # Plot the time evolution of the system
```


# Getting Started

To use the notebooks here, create a `conda` environment using [qgraph_env.yml](qgraph_env.yml).

Instructions for creating a `conda` environment from a yaml file are located [here](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file). This will automatically create an `conda` environment named `qgraph`, which you should use as your Jupyter kernel. 






