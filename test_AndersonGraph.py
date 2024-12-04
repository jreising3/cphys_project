import pytest
import numpy as np
import networkx as nx
from AndersonGraph import AndersonGraph

@pytest.fixture
def setup_anderson_graph():
    # Create a simple graph for testing
    graph = nx.path_graph(4)
    psi_0 = np.array([1, 0, 0, 0], dtype=complex)
    eps_range = (0, 1)
    t_hop = 1.0
    anderson_graph = AndersonGraph(graph, psi_0, eps_range, t_hop)
    return anderson_graph

def test_initialization(setup_anderson_graph):
    anderson_graph = setup_anderson_graph
    assert anderson_graph.num_sites == 4
    assert len(anderson_graph.psi_0) == 4
    assert anderson_graph.t_hop == 1.0
    assert anderson_graph.binding.shape == (4, 4)

def test_hamiltonian(setup_anderson_graph):
    anderson_graph = setup_anderson_graph
    hamiltonian = anderson_graph._hamiltonian()
    assert hamiltonian.shape == (4, 4)
    assert np.allclose(hamiltonian, hamiltonian.T.conj())  # Hamiltonian should be Hermitian

def test_time_evolution_operator(setup_anderson_graph):
    anderson_graph = setup_anderson_graph
    time = 1.0
    U_t = anderson_graph._time_evolution_operator(time)
    assert U_t.shape == (4, 4)
    assert np.allclose(U_t @ U_t.T.conj(), np.eye(4))  # U_t should be unitary

def test_psi_at_t(setup_anderson_graph):
    anderson_graph = setup_anderson_graph
    time = 1.0
    psi_t = anderson_graph.psi_at_t(time)
    assert psi_t.shape == (4,)
    assert np.isclose(np.linalg.norm(psi_t), 1.0)  # Wavefunction should be normalized

def test_simulate(setup_anderson_graph):
    anderson_graph = setup_anderson_graph
    t_max = 10.0
    nt = 100
    history = anderson_graph.simulate(t_max, nt)
    assert len(history) == nt
    assert history[0].shape == (4,)

def test_calculate_entropy(setup_anderson_graph):
    anderson_graph = setup_anderson_graph
    state = np.array([1, 0, 0, 0], dtype=complex)
    entropy = anderson_graph.calculate_entropy(state)
    assert np.isclose(entropy, 0.0)

def test_entropy_times(setup_anderson_graph):
    anderson_graph = setup_anderson_graph
    t_max = 10.0
    nt = 100
    anderson_graph.entropy_times(t_max, nt)