# These functions handle balancing a reaction, and checking if said reaction is balanced.

import periodictable as ptable
import sympy as sp


# This function checks if an equation is balanced
# The input argument is a dictionary where each compound (key) is a str and the values are
# their respective coefficients
# Reactants must have negative values in the dictionary, while products have positive values
def reaction_check(reaction):
    products_string = ''
    reactants_string = ''

    # A giant string containing the appropriate amount of elements is created for both sides of the reaction
    for compound, coefficient in reaction.items():
        if compound != 'Extent':
            if coefficient > 0:
                products_string += compound*coefficient

            else:
                reactants_string += compound*-coefficient

    # The periodictable library will convert the giant strings to a formula and identify how many atoms of each
    # element are present
    reactants_atoms = ptable.formula(reactants_string).atoms
    products_atoms = ptable.formula(products_string).atoms

    # If these sets of elements are equivalent, then the reaction is balanced, and balance is set to True
    # If not, the reaction needs to be balanced still, balance is set to False
    if reactants_atoms == products_atoms:
        balance = True

    else:
        balance = False

    return balance


# This function uses the same dictionary input as the previous function
# It will balance the reaction and update the dictionary with the new coefficients
def reaction_balance(reaction):
    # A dict containing the total number of compounds used to obtain the total unknowns in the system in the following
    # for loop
    reaction_terms = len(reaction)
    total_symbols_list = []

    # A list of symbols is a requirement for sp.linsolve to appropriately solve the system, and each one must be
    # converted to sp.Symbol
    for key in reaction.keys():
        total_symbols_list.append(sp.Symbol(key))

    # Checking if the system is balanced by calling the check_rxn_balance function from Chemistry
    balance = reaction_check(reaction)

    # If the balance fails then the magic of sympy will solve it by setting up a system of linear equations and a matrix
    if balance is False:
        total_elements_str = ''

        # The total elements in the equation (H, C, O, etc) need to be obtained
        for compound in reaction:
            if compound != 'Extent':
                total_elements_str = total_elements_str.join(str(compound))

        total_elements_list = list(ptable.formula(total_elements_str).atoms)

        # The rows of the equation matrix is each element in the equation
        rows = len(total_elements_list)

        # The columns are the total compounds present in the equation
        cols = reaction_terms - 1

        # The equation matrix is defined using the zeros function, al slots are set to zero for easy manipulation
        equation_matrix = sp.zeros(rows, cols)

        # y is the counter variable for elements, it represents where the program is in the rows
        y = 0
        compound_order = []

        for compound in reaction:
            if compound != 'Extent':
                compound_order.append(compound)
                # x does the same thing as y, but for the columns
                x = 0
                composition = ptable.formula(compound).atoms

                for element in total_elements_list:
                    # if the element is not present in the compound, it will be stored as a zero in the matrix
                    if element not in composition:
                        composition[element] = 0

                    # The values are stored here, in the matrix and position (x, y). This repeats for each element and
                    # compound
                    if reaction[compound] > 0:
                        equation_matrix[x, y] = composition[element]

                    else:
                        equation_matrix[x, y] = -composition[element]

                    # x is incremented for the next element
                    x += 1

                # y is incremented for the next compound
                y += 1

        # Sympy converts the equation matrix to a sympy compatible matrix object, and creates the solution vector of
        # all 0
        equation_matrix = sp.Matrix(equation_matrix)
        solution_vector = sp.Matrix(sp.zeros(rows, 1))

        # A sympy set object containing values is output by the linsolve function from sympy,
        # which solves the matrix in terms of one of the compounds present (usually the last compound)
        solution_set = sp.linsolve((equation_matrix, solution_vector), total_symbols_list)
        solution_list = []

        # A solution list is derived from the solution set, which is far easier to manipulate and index
        for answer in range(reaction_terms - 1):
            solution_list.append(next(iter(solution_set))[answer])

        # Whichever symbol is present is the symbol that all coefficients are dependent on
        basis_symbol = next(iter(solution_list[0].atoms(sp.Symbol)))

        # Assume the smallest coefficient is one
        smallest_coefficient = 1

        # The smallest fraction must be obtained to balance in whole coefficients
        for coefficient in range(reaction_terms - 1):
            # Assuming the basis_symbol is equal to one, it can simply be removed
            solution_list[coefficient] = solution_list[coefficient] / basis_symbol

            # If the coefficient that is left is smaller than the smallest coefficient stored, it will replace
            # the smallest coefficient
            if 0 < (solution_list[coefficient] % 1):
                smallest_coefficient = solution_list[coefficient] % 1

        # A multiplier will be obtained from the inverse of the smallest coefficient, and all other coefficients will be
        # scaled by that multiplier
        for coefficient in range(reaction_terms - 1):
            multiplier = smallest_coefficient ** (-1)

            solution_list[coefficient] *= multiplier

        compound_count = 0

        for compound in compound_order:
            if reaction[compound] > 0:
                reaction[compound] = solution_list[compound_count]

            else:
                reaction[compound] = -solution_list[compound_count]

            compound_count += 1

    # Return the balanced reaction
    return reaction
