import math
import sys
import tempfile

import atropy_core_pybind11
import numpy as np
import sympy as sp
from atropy_core.grid import GridParms
from atropy_core.index_functions import incrVecIndex
from atropy_core.initial_condition import InitialCondition
from atropy_core.reaction import Reaction, ReactionSystem
from atropy_core.tree import Tree


def species(symbol_string: str):
    """
    Generate sympy variables for species.

    The species of a rection network can be defined as sympy variables, 
    which is needed for model generation.
    The type of output is dependent on the properties of input arguments.

    Parameters
    ----------
    symbol_string : str
        Names of species inside a string, seperated by a comma.

    See Also
    --------
    sympy.symbols : Transform strings into instances of `Symbol` class.

    Examples
    --------
    >>> from atropy.src.generator import species
    >>> S0, S1, S2, S3, S4 = species("S0, S1, S2, S3, S4")
    """
    return sp.symbols(symbol_string)


class Model:
    """
    Represent model for reaction system.

    For a reaction system we can set up the model.
    Before initialization, the species need to be defined using `atropy.src.generator.species`.

    Parameters
    ----------
    _species : tuple
        Species from `atropy.src.generator.species`.

    Returns
    -------
    Model
        Model for the reaction system.

    See Also
    --------
    atropy.src.generator.species : Generate sympy variables for species.
    atropy.src.generator.Model.add_reaction : Add single reaction to `Model`.
    atropy.src.generator.Model.add_reactions : Add multiple reactions to `Model`.
    atropy.src.generator.Model.generate_reaction_system : Generate the reaction system.

    Examples
    --------
    >>> from atropy.src.generator import Model
    >>> model = Model((S0, S1, S2, S3, S4))
    """
    def __init__(self, _species):
        self.reactions = []
        self.species = _species

    # Different functions to add single or multiple reactions to our model
    def add_reaction(self, reactants, products, propensities):
        """
        Add single reaction to `Model`.

        For translating a single chemical reaction to implementation.

        Parameters
        ----------
        reactants
            `Sympy` equation of reactants.
        products
            `Sympy` equation of products.
        propensities : dict, float or int
            Propensity for specific reaction. Type of float or int can only be used 
            if propensity described by mass action.

        See Also
        --------
        atropy.src.generator.Model : Represent model for reaction system.
        atropy.src.generator.Model.add_reactions : Add multiple reactions to `Model`.
        atropy.src.generator.Model.generate_reaction_system : Generate the reaction system.

        Examples
        --------
        >>> from atropy.src.generator import Model
        >>> model = Model((S0, S1, S2, S3, S4))

        Adding a reaction using a dictionary for propensity:

        >>> model.add_reaction(0, S1, {S0: 0.6 / (0.6 + S0), S4: 1.0 + S4})

        Adding a reaction using a float value for propensity:

        >>> model.add_reaction(S0, 0, 0.0025)
        """
        num_symbols = len(self.species)
        eq_sp = products - reactants

        nu_vec = np.zeros(num_symbols)
        for i, sym in enumerate(self.species):
            nu_vec[i] = eq_sp.coeff(sym)

        prop_dict = {}
        # Test if we only have coefficient as variable,
        # if so, generate propensity in non factorised form
        if type(propensities) is int or type(propensities) is float:
            for sym in self.species:
                for i in range(reactants.coeff(sym)):
                    propensities *= sym - i
                propensities /= math.factorial(reactants.coeff(sym))

        # If propensites in non factorised form, factorise it and generate a dictionary
        if isinstance(propensities, sp.Expr):
            propensities = sp.simplify(propensities)

            n, d = sp.fraction(propensities)

            after_factor_n = sp.factor_list(n)
            after_factor_d = sp.factor_list(d)

            propensities = {}

            num_factors_n = len(after_factor_n[1])
            num_factors_d = len(after_factor_d[1])

            if num_factors_n != 0:
                coefficient_n = after_factor_n[0] ** (1.0 / num_factors_n)

                for i in range(num_factors_n):
                    factor = sp.Pow(after_factor_n[1][i][0], after_factor_n[1][i][1])
                    elements = list(factor.atoms(sp.Symbol))

                    if len(elements) != 1:
                        print("ERROR: Propensity non factorizable")
                        sys.exit()

                    if elements[0] in propensities:
                        propensities[elements[0]] *= factor * coefficient_n
                    else:
                        propensities[elements[0]] = factor * coefficient_n

            if num_factors_d != 0:
                coefficient_d = after_factor_d[0] ** (1.0 / num_factors_d)

                for i in range(num_factors_d):
                    factor = sp.Pow(after_factor_d[1][i][0], after_factor_d[1][i][1])
                    elements = list(factor.atoms(sp.Symbol))

                    if len(elements) != 1:
                        print("ERROR: Propensity non factorizable")
                        sys.exit()

                    if elements[0] in propensities:
                        propensities[elements[0]] *= 1 / (factor * coefficient_d)
                    else:
                        propensities[elements[0]] = 1 / (factor * coefficient_d)

        # Using the dictionary, generate the lambda functions to append the reactions
        for key, value in list(propensities.items()):
            for i, sym in enumerate(self.species):
                if key == sym:
                    prop_dict[i] = sp.lambdify(sym, value)

        self.reactions.append(Reaction(prop_dict, nu_vec))

    def add_reactions(self, reactants_list, products_list, propensities_list):
        """
        Add multiple reactions to `Model`.

        For translating multiple chemical reactions to implementation.

        Parameters
        ----------
        reactants_list : list
            List of `Sympy` equations of reactants.
        products_list : list
            List of `Sympy` equations of products.
        propensities_list : list of dict, list of float or list of int
            List of propensities for specific reactions. Type of list of 
            float or list of int can only be used if propensities described by mass action.

        See Also
        --------
        atropy.src.generator.Model : Represent model for reaction system.
        atropy.src.generator.Model.add_reaction : Add single reaction to `Model`.
        atropy.src.generator.Model.generate_reaction_system : Generate the reaction system.

        Examples
        --------
        >>> from atropy.src.generator import Model
        >>> model = Model((S0, S1, S2, S3, S4))
        >>> model.add_reactions([S0, S1], [0, 0], [0.0025, 0.0007])
        """
        for reactants, products, propensities in zip(
            reactants_list, products_list, propensities_list, strict=False
        ):
            self.add_reaction(reactants, products, propensities)

    def generate_reaction_system(self):
        """
        Generate the reaction system.

        After the `Model` was initialized and the reactions were added using 
        `atropy.src.generator.Model.add_reaction`, the reaction system can be generated.

        See Also
        --------
        atropy.src.generator.Model : Represent model for reaction system.
        atropy.src.generator.Model.add_reaction : Add single reaction to `Model`.

        Examples
        --------
        >>> from atropy.src.generator import Model
        >>> model = Model((S0, S1, S2, S3, S4))
        >>> model.add_reaction(S0, 0, 0.0025)
        >>> model.generate_reaction_system()
        """
        species_names = [str(species_name) for species_name in self.species]
        self.reaction_system = ReactionSystem(self.reactions, species_names)


class Partitioning:
    """
    Generate partitioning for the reaction system.

    To reduce computational complexity of the low rank solver a good partition is needed.
    Note that cuts should be chosen in a way that tightly coupled
    species are together in the same partition.

    Parameters
    ----------
    _partition : str
        Partitioning of the species. Each partition is inside a set of brackets.
    _r : numpy.ndarray
        Ranks for each level of the partitioning.
    _model : atropy.src.generator.Model
        Model for the reaction system.

    See Also
    --------
    atropy.src.generator.Partitioning.add_grid_params : Add grid parameters to `Partitioning`.
    atropy.src.generator.Partitioning.generate_tree : Generate tree structure for reaction system.
    atropy.src.generator.Partitioning.generate_initial_condition : Initialize the initial condition.
    atropy.src.generator.Partitioning.set_initial_condition : Set values for inital condition.

    Examples
    --------
    >>> from atropy.src.generator import Model, Partitioning

    Set up the parameters (for model reactions can be added using 
    `atropy.src.generator.Model.add_reaction`):

    >>> model = Model((S0, S1, S2, S3, S4))
    >>> r = np.array([5, 4])
    >>> p0 = "(S0 S1)((S2 S3)(S4))"

    Initialize the partitioning:

    >>> partitioning = Partitioning(p0, r, model)
    """
    def __init__(self, _partition: str, _r: np.ndarray, _model: Model):
        self.r = _r
        self.model = _model
        self.partition = _partition
        for i, sym in enumerate(self.model.species):
            self.partition = self.partition.replace(str(sym), str(i))

    def add_grid_params(self, n: np.ndarray, binsize: np.ndarray, liml: np.ndarray):
        """
        Add grid parameters to `Partitioning`.

        Parameters
        ----------
        n : numpy.ndarray
            Amount of gridpoints for each species.
        binsize : numpy.ndarray
            
        liml : numpy.ndarray
            Lower limits of the population numbers.

        See Also
        --------
        atropy.src.generator.Partitioning : Generate partition for the reaction system.
        atropy.src.generator.Partitioning.generate_tree : Generate tree structure for reaction system.
        atropy.src.generator.Partitioning.generate_initial_condition : Initialize the initial condition.
        atropy.src.generator.Partitioning.set_initial_condition : Set values for inital condition.

        Examples
        --------
        >>> from atropy.src.generator import Partitioning
        >>> partitioning = Partitioning(p0, r, model)

        Define parameters and add grid parameters:

        >>> n = np.array([16, 41, 11, 11, 11])
        >>> d = n.size
        >>> binsize = np.ones(d, dtype=int)
        >>> liml = np.zeros(d)
        >>> partitioning.add_grid_params(n, binsize, liml)
        """
        self.grid = GridParms(n, binsize, liml)

    def generate_tree(self):
        """
        Generate tree structure for reaction system.

        The tree should be generated after setting up the `Model` and adding the grid parameters to the `Partitioning`.

        See Also
        --------
        atropy.src.generator.Partitioning : Generate partition for the reaction system.
        atropy.src.generator.Partitioning.add_grid_params : Add grid parameters to `Partitioning`.
        atropy.src.generator.Partitioning.generate_initial_condition : Initialize the initial condition.
        atropy.src.generator.Partitioning.set_initial_condition : Set values for inital condition.
        
        Examples
        --------
        >>> from atropy.src.generator import Partitioning
        >>> partitioning = Partitioning(p0, r, model)
        >>> partitioning.add_grid_params(n, binsize, liml)

        Generate the tree structure:

        >>> partitioning.generate_tree()
        """
        self.tree = Tree(self.partition, self.grid)
        self.tree.initialize(self.model.reaction_system, self.r)

    def generate_initial_condition(self, n_basisfunctions: np.ndarray):
        """
        Initialize the initial condition.

        Parameters
        ----------
        n_basisfunctions : numpy.ndarray
            Number of basis functions.

        See Also
        --------
        atropy.src.generator.Partitioning : Generate partition for the reaction system.
        atropy.src.generator.Partitioning.add_grid_params : Add grid parameters to `Partitioning`.
        atropy.src.generator.Partitioning.generate_tree : Generate tree structure for reaction system.
        atropy.src.generator.Partitioning.set_initial_condition : Set values for inital condition.

        Examples
        --------
        >>> from atropy.src.generator import Partitioning
        >>> partitioning = Partitioning(p0, r, model)
        >>> partitioning.add_grid_params(n, binsize, liml)
        >>> partitioning.generate_tree()

        Initialize the initial condition:

        >>> partitioning.generate_initial_condition(r)
        """
        self.initial_conditions = InitialCondition(self.tree, n_basisfunctions)

    def set_initial_condition(self, polynomials_dict):
        """
        Set values for inital condition.

        Only possible for rank 1 inital condition, which can be split into a product of functions, 
        each depending only on one species

        Parameters
        ----------
        polynomials_dict : dict
            Dictionary containing a function for each species.

        See Also
        --------
        atropy.src.generator.Partitioning : Generate partition for the reaction system.
        atropy.src.generator.Partitioning.add_grid_params : Add grid parameters to `Partitioning`.
        atropy.src.generator.Partitioning.generate_tree : Generate tree structure for reaction system.
        atropy.src.generator.Partitioning.generate_initial_condition : Initialize the initial condition.

        Examples
        --------
        >>> from atropy.src.generator import Partitioning
        >>> partitioning = Partitioning(p0, r, model)
        >>> partitioning.add_grid_params(n, binsize, liml)
        >>> partitioning.generate_tree()
        >>> partitioning.generate_initial_condition(n_basisfunctions)

        Assign a function to each species:

        >>> polynomials_dict = {
        ...     S0: sp.exp(-S0**2),
        ...     S1: sp.exp(-S1**2),
        ...     S2: sp.exp(-S2**2),
        ...     S3: sp.exp(-S3**2),
        ...     S4: sp.exp(-S4**2),
        ... }

        Set values for the initial condition:

        >>> partitioning.set_initial_condition(polynomials_dict)
        """
        polynomials = []
        for sym in self.model.species:
            for key, value in list(polynomials_dict.items()):
                if key == sym:
                    polynomials.append(sp.lambdify(sym, value))

        for Q in self.initial_conditions.Q:
            Q[0, 0, 0] = 1.0

        species_idx = 0
        for node in range(self.tree.n_external_nodes):
            vec_index = np.zeros(self.initial_conditions.external_nodes[node].grid.d())
            for i in range(self.initial_conditions.external_nodes[node].grid.dx()):
                self.initial_conditions.X[node][i, :] = 1
                for j in range(self.initial_conditions.external_nodes[node].grid.d()):
                    self.initial_conditions.X[node][i, :] *= polynomials[
                        species_idx + j
                    ](vec_index[j])
                incrVecIndex(
                    vec_index,
                    self.initial_conditions.external_nodes[node].grid.n,
                    self.initial_conditions.external_nodes[node].grid.d(),
                )
            species_idx += len(vec_index)


def run(partitioning: Partitioning, output: str, tau: float, tfinal: float | int, snapshot: int = 2, substeps: int = 1, method: str = "RK4"):
    """
    Run the low rank simulation.

    Generate multiple NetCDF output files, which simulate the reaction system described in partitioning.

    Parameters
    ----------
    partitioning : Partitioning
        `Partitioning` of the reaction system.
    output : str
        Name of the generated output files.
    tau : float
        Timestep size for the simulation.
    tfinal: float or int
        Final time for the simulation.
    snapshot : int, default 2
        Number of generated output files.
    substeps : int, default 1

    method : str, default "RK4"
        Time integration method for the simulation. 
        The 4 possible values are: "implicit_Euler", "explicit_Euler", "Crank_Nicolson" and "RK4".

    See Also
    --------
    atropy.src.generator.species : Generate sympy variables for species.
    atropy.src.generator.Model : Represent model for reaction system.
    atropy.src.generator.Partitioning : Generate partition for the reaction system.

    Examples
    --------
    After setting up `Model` and `Partitioning` one can run the simulation:

    >>> run(partitioning, "output", 1e-3, 10, snapshot=10, method="implicit_Euler")
    """
    with tempfile.NamedTemporaryFile(suffix=".nc", delete=True) as temp_file:
        file_name = temp_file.name
        partitioning.tree.write(fname=file_name)
        snap = int(np.floor((tfinal / tau) / snapshot))
        if method == "implicit_Euler":
            m = "i"
        elif method == "explicit_Euler":
            m = "e"
        elif method == "Crank_Nicolson":
            m = "c"
        elif method == "RK4":
            m = "r"
        else:
            print(
                "Possible inputs for method: "
                "implicit_Euler, explicit_Euler, Crank_Nicolson, RK4"
            )
        atropy_core_pybind11.IntegrateTTN(
            file_name, output, snap, tau, tfinal, substeps, m
        )
