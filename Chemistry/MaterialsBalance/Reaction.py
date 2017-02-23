import periodictable as ptable
import sympy as sp

# The ability to add reactions for heat calculations or for other purposes


class Reaction(object):

    """The Reaction object is used to describe a chemical reaction. It requires a dictionary input with
    {compound:coefficient} format. Products should have a positive coefficient value and reactants should have a
    negative coefficient value. If the balanced coefficients are unknown, then inputs of +/- 1 are acceptable, as the
    reaction will balance itself. This is done using the periodictable and sympy packages."""

    def __init__(self, species_dict, basis_compound='', extent_of_reaction=None, heat_of_reaction=None):

        """The species_info input must be a dictionary in {compound:coefficient} format. It will be set to self.species
        for the reaction. As the reaction balances itself it will manipulate that dictionary. The first optional input
        is the basis_compound, which guarantees that the compound will have a coefficient of 1. The extent_of_reaction
        and heat_of_reaction are optional inputs for when they are relevant."""

        # A dictionary in {compound:coefficient} format
        # The base of the reaction representation
        self.species = species_dict

        # The total elements (C, H, O, etc) in the system is required to balance it
        self.elements = []

        # The compound in the reaction with a guaranteed coefficient of 1
        self.basis = basis_compound

        # The total change in moles for the reaction
        self.molar_change = 0

        # The extent (in moles) of the reaction
        self.extent = sp.S(extent_of_reaction)

        # The heat (per mole) of the reaction
        self.heat = sp.S(heat_of_reaction)

        # This runs for the cases in which the input coefficients are not whole numbers
        # check_balance requires that the coefficients be whole and of the integer type
        self.set_coefficients_whole()

        # This method will check to see if the reaction is properly balanced
        self.check_balance()

        # If a basis is set then this will modify the balanced equation to accommodate
        self.set_basis()

        # The total molar change for a reaction is useful for materials balances
        self.determine_molar_change()

    def check_balance(self):

        """The check_balance method identifies the totals of each element in both the products and the reactants and
        compares them using the periodictable package. If the reaction is not balanced, then the balance_reaction
        method will run."""

        # Empty strings for products/reactants formulas
        products_atoms = ''
        reactants_atoms = ''

        # Each formula is scaled by the coefficient and appended to the appropriate string
        for chemical, coefficient in self.species.items():
            if coefficient > 0:
                products_atoms += coefficient * chemical

            else:
                reactants_atoms += -coefficient * chemical

        # The periodictable library will convert the strings to a formula object using ptable.formula()
        # The atoms method is used to identify the quantity of each element in the products and reactants
        reactants_atoms = ptable.formula(reactants_atoms).atoms
        products_atoms = ptable.formula(products_atoms).atoms

        # The elements are stored in self.elements for use in reaction_balance if necessary
        for element in products_atoms:
            self.elements.append(element)

        # If these sets of elements are equivalent, then the reaction is balanced and __init__ will continue
        # If not, the reaction needs to be balanced still, and the reaction_balance method will run
        if reactants_atoms != products_atoms:
            self.balance_reaction()

    def balance_reaction(self):

        """The balance_reaction method will generate a sympy matrix with rows that correspond to each element in the
        reaction and columns that correspond to each compound. Using the sympy linsolve function it will begin to solve
        the matrix for each coefficient in terms of of of the compounds. This compound can be assumed to equal 1 in the
        next method which will allow for scaling of the coefficients while keeping the reaction balanced."""

        # The rows of the reaction matrix is each element in the reaction
        # The columns are the total compounds present in the equation
        # The equation matrix is defined using the sympy zeros function, all slots are set to zero for easy manipulation
        reaction_matrix = sp.zeros(len(self.elements), len(self.species))

        # The symbols_list contains every compound in the reaction as a sympy symbol so that it can solve the matrix
        symbols_list = []

        # Every compound in the reaction is checked for elements
        for compound in self.species.keys():

            # The periodictable method atoms is called on the compound formula
            # This identifies how many of each element are present in the compound
            composition = ptable.formula(compound).atoms

            # The compound is made into a symbol and stored in the symbols_list
            symbols_list.append(sp.sympify(compound))

            # Every element in the reaction must be considered, even if they are not all present in the compound
            for element in self.elements:

                # if the element is not present in the compound, it will be stored as a zero in the composition
                if element not in composition:
                    composition[element] = 0

                # The reaction matrix for the compound and element is set to the compound amount of that element
                # self.elements.index(element) returns an integer number for the element position in the matrix
                # list(self.species.keys()).index(compound) returns an integer number for the compound position
                reaction_matrix[self.elements.index(element),
                                list(self.species.keys()).index(compound)] = composition[element]

        # Sympy converts the equation matrix to a sympy compatible matrix object
        # It also creates the solution vector of all 0
        reaction_matrix = sp.Matrix(reaction_matrix)
        solution_vector = sp.Matrix(sp.zeros(len(self.elements), 1))

        # A sympy set object containing values is output by the linsolve function from sympy,
        # which solves the matrix in terms of one of the compounds present (usually the last compound)
        solution_set = sp.linsolve((reaction_matrix, solution_vector), symbols_list)

        # This converts the solution_set to usable coefficients
        self.interpret_balance(symbols_list, solution_set)

    def interpret_balance(self, symbols_list, solution_set):

        """The interpret_balance method will take the solution set output by the sympy linsolve function and the symbols
        list from the previous reaction_balance method. It will modify the solutions as necessary and store them into
        self.species. This method will leave self.species with properly scaled coefficients that are not whole and are
        not set to a specific basis compound."""

        # A solution list is derived from the solution set, which allows it to be manipulated
        for answer in range(len(self.species)):

            # In the linsolve process, some signs can be switched depending on the compound that is remaining
            # If the original coefficient and the solution have different signs, then the solution is fixed and stored
            if sp.S(self.species[str(symbols_list[answer])]).could_extract_minus_sign() != \
                    next(iter(solution_set))[answer].could_extract_minus_sign():

                # The solution multiplied by negative one is stored in self.species
                self.species[str(symbols_list[answer])] = -1 * next(iter(solution_set))[answer]

            # If the solution and the original have the same sign, then the solution is stored with no modifications
            else:
                self.species[str(symbols_list[answer])] = next(iter(solution_set))[answer]

        # Whichever symbol is present is the symbol that all coefficients are dependent on
        # Since coefficients must be purely numbers, this symbol must be identified and then removed
        basis_symbol = next(iter(self.species[list(self.species.keys())[0]].atoms(sp.Symbol)))

        # All solved coefficients will have the symbol, so it can be divided out leaving the coefficient behind
        for compound in self.species:
            self.species[compound] = self.species[compound] / basis_symbol

        # This method will set the coefficients whole
        self.set_coefficients_whole()

    def set_coefficients_whole(self):

        """The set_coefficients_whole method converts all coefficients to whole integers by identifying the smallest
        coefficient between 0 and 1 and then multiplying each coefficient by the inverse. This is repeated until all
        coefficients are whole numbers."""

        # Placeholder for the while loop condition
        whole_coefficients = None

        # This continues until every coefficient has been made whole
        while whole_coefficients != len(self.species):

            # Assume the smallest coefficient is one, which will have no effect on the coefficient values
            smallest_coefficient = 1

            # The whole_coefficients value is now set to zero to allow for integer addition
            whole_coefficients = 0

            # The smallest fraction must be obtained to balance in whole coefficients
            for compound in self.species:

                # Modulo will only return zero when the number is whole
                # Otherwise, the fraction is saved as the smallest_coefficient if it is smaller than the previous value
                if 0 < (self.species[compound] % 1) < smallest_coefficient:
                    smallest_coefficient = self.species[compound] % 1

                # If the coefficient is whole, then the total number of whole_coefficients can increase
                else:
                    whole_coefficients += 1

            # All other coefficients will be scaled by a multiplier obtained using the smallest_coefficient
            for compound in self.species:

                # A multiplier will be obtained from the inverse of the smallest_coefficient
                multiplier = smallest_coefficient ** (-1)

                # This guarantees that at least 1 coefficient will become whole
                self.species[compound] *= multiplier

            # This converts each coefficient to an integer so that coefficient*formula operation is valid
            for compound in self.species:
                self.species[compound] = int(self.species[compound])

    def set_basis(self):

        """The set_basis method allows the user to set one coefficient in the reaction to 1 scaling all other chemicals
        appropriately. This may be important in determining how many moles of CO2 or H2O are generated from 1 mole of
        fuel in a combustion reaction. If no compound is set, then this method will have no effect."""

        # If the compound isn't present in the reaction then the reaction will remain untouched
        if self.basis not in self.species:
            return

        # The divisor is the basis_compound coefficient
        divisor = self.species[self.basis]

        # Dividing any number by itself equals 1, so the basis_compound coefficient will always be set to one
        # Other coefficients will be scaled appropriately using the same division
        for chemical in self.species:
            self.species[chemical] /= divisor

        self.molar_change /= divisor

    def determine_molar_change(self):

        """The determine_molar_change method is useful for a materials balance problem. It is used to determine the
        total moles that the reaction adds or removes from a system."""

        # The molar_change is just an addition of all coefficients present in the reaction
        for compound in self.species.keys():
            self.molar_change += self.species[compound]
