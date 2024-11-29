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

Anderson localization can be demonstrated on this model when the diagonal of the Hamiltonian $H$ is randomized and if values of $\epsilon$ are randomly sampled from a uniform distribution on $[-W, \, W]$ where $W$ is known as the disorder parameter. In this case, larger $W$ correlates with increased localization.
