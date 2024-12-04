import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.linalg import expm
import scipy.integrate as integrate
from scipy.stats import entropy

plt.style.use('dark_background')

class AndersonGraph:
    '''
    Construct a graph to time-evolve the Anderson hamiltonian on. 
    We represent all operators and state vectors in the lattice site basis. 

    Attributes
        graph (periodic networkx graph): underlying graph, representing lattice sites we simulate on.
        psi_0 (1D nd array): initial wavefunction in the site basis.
        eps_range (array-like): range to draw random values of epsilon from to create a random diagonal on the hamiltonian.
        t_hop (float): hopping parameter.
        num_sites (int): number of lattice sites.
        alpha: strength of the anharmonic term 
        binding (2D nd array): binding term of the hamiltonian (ie. not the hoppoing term).
        pos (dict): dict with nodes of self.graph as keys and positions as values.
    '''

    def __init__(self, graph, psi_0, eps_range, t_hop,alpha):
        self.graph = graph
        self.psi_0 = psi_0

        self.num_sites = self.graph.number_of_nodes()
        
        # Checks if number of nodes on graph matches number of nodes for wave function
        if self.num_sites != len(self.psi_0):
            raise ValueError("Number of nodes on the graph does not match the length of the wave function")

        self.eps_range = eps_range
        self.t_hop = t_hop
        self.alpha=alpha
        self.binding = np.diagflat(np.random.uniform(*self.eps_range, size=self.num_sites))
        self.pos = nx.spring_layout(self.graph)


    def _static_hamiltonian(self):
        '''
        Construct the the static hamiltonian for the Anderson tight-binding model. 

        Returns
            hamiltonian (2d ndarray): matrix representation of the hamiltonian in the lattice site basis.
        '''
        adjacency = nx.to_numpy_array(self.graph)
        hopping = -self.t_hop * adjacency

        return self.binding + hopping
        
    
    def _static_time_evolution_operator(self, time):
        '''
        Calculate the unitary time evolution operator for the given hamiltonian.

        Args
            time (float): time when time evolution operator is calculated

        Returns
            U(t) (ndarray of size num_sites x num_sites): unitary time evolution operator. 
        '''

        return expm(-1j * self._static_hamiltonian() * time)

    def _time_depent_evolution_part(self, time):
         # Initialize the wavefunction list
         psi_t = []
    
         # Define the function to integrate
         def u(t):
            return (self.alpha * np.cos(t))**3
    
            # Perform the integration over time
         delx, _ = integrate.quad(lambda t: np.real(u(t)), 0, time)  # Example: taking real part
    
         # Get the number of sites
         n = self.num_sites

         # Initialize psi_t with some initial values (e.g., zeros or random complex numbers)
         psi_t = [0] * n  # Or use np.zeros(n, dtype=complex) for complex initialization

         # Fill psi_t with new values based on evolution
         for i in range(n):
            # Update psi_t[i] with some evolution logic (e.g., depending on delx)
            psi_t[i] = psi_t[i] + delx  # Example logic

         return psi_t
 
    
    def _psi_at_t(self, time):
        '''
        Returns the wavefucntion, in the lattice site basis, at a given time t. 

        Args
            time (float): time at which the wavefunction is calculated.
        
        Returns
            psi (1D ndarray of size num_sites): wavefunction at given time.
        '''

        return (self._static_time_evolution_operator(time) @ self.psi_0)+self._time_depent_evolution_part(time)
    

    def simulate(self, t_max, nt): #t_steps):
        '''
        Calculate psi(t) for a sequence of times. 

        Args
            t_max (float): final time.
            nt (int): number of time steps.

        Returns
            history (ndarray of size nt x num_sites): wavefunctions as a function of time from 0 to t_max.
        '''        

        times = np.linspace(0, t_max, nt)
        
        history = []

        for time in times:
            #self._time_evolution_operator(time) @ self.psi_0
            history.append((self._static_time_evolution_operator(time) @ self.psi_0)+self._time_depent_evolution_part(time))
        return history
    

    def plot_graph(self):
        '''
        Draw graph attribute, using the networkx draw method.
        '''
        
        return nx.draw(self.graph)


    def plot_density(self, t, node_size=10, line_width=2, layout=None):# axisstabilized = False):
        '''
        Plot the probability density, aka |psi(t)|^2

        Args
            t (float): time when the probability density is plotted
        '''
        
        #fig = plt.figure(figsize = (12,10))
        #psi_t = self._time_evolution(t) @ self.psi_0
        plt.style.use('dark_background')
        psi_t = self._psi_at_t(t)
        density = np.real(np.multiply(psi_t.conj(), psi_t))
        
        #plt.title("Wave function probability density at time " + str(t) + "\n p = " + str(self.p)) 
        if layout == None:
            self.pos=nx.spring_layout(self.graph)
        else:
            self.pos = layout
        nx.draw(self.graph, self.pos, node_color = density, cmap = plt.cm.cividis, node_size = node_size, width = line_width)
        
        plt.show()


    def calculate_entropy(self, state):
        # Normalize the state
        state = state / np.linalg.norm(state)
        # Compute the density matrix
        rho = np.outer(state, np.conj(state))
        # Compute eigenvalues of the density matrix
        eigenvalues = np.linalg.eigvalsh(rho)
        # Compute von Neumann entropy
        return -np.sum(eigenvalues * np.log2(eigenvalues + 1e-12))     

            
    def entropy_times(self,t_max,nt):

       times = np.linspace(0, t_max, nt)
       H=[]
       for i in range(len(times)):
           state=self._psi_at_t(times[i])
           H.append(self.calculate_entropy(state))
       plt.scatter(times,H)
