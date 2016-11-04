# This program will balance (some) chemical reactions
import sympy as sp
import periodictable as ptable
from Chemistry.check_rxn_balance import check_rxn_balance

# Pre-defining variables that will change with some loops and user inputs
reactants_count = 0
reactants = {}
products_count = 0
products = {}
basis_compound = False

# A loop that takes string inputs and adds them as keys to the reactants dict
# All compound values (coefficient) are 1 initially
while True:
    reactants_count += 1
    compound_input = input('Input the formula of reactant {}: '.format(reactants_count))
    if compound_input == '':
        break
    reactants[compound_input] = 1

# Same as above, but for products
while True:
    products_count += 1
    compound_input = input('Input the formula of product {}: '.format(products_count))
    if compound_input == '':
        break
    products[compound_input] = 1

# While the basis_compound is still False, the user will be repeatedly shown an input prompt
# This format prevents invalid inputs and is extremely useful, implement this into other scripts to prevent...
# I N  P   U    T     H      E       L        L
while basis_compound is False:
    basis_compound = str(input('Input the desired compound (if there is one) with a coefficient of one: '))

    # If the user inputs no compound, an empty string, then the balance will be done with whole coefficients (default)
    if basis_compound == '':
        print('Balance will be completed with whole coefficients\n')

    # If the user inputs a non-empty string, the code will check if that compound exists in products or reactants
    # If the compound isn't present in the reaction, the prompt will repeat
    # If the compound is in the reaction, then it will be balanced with a coefficient of one
    elif type(basis_compound) == str:
        if basis_compound in reactants or products:
            print('{} will be balanced with a coefficient of one\n'.format(basis_compound))

        else:
            basis_compound = False
            print('Compound not present in reaction\n')

# A dict containing the total number of compounds used to obtain the total unknowns in the system in the following for
# loop
total_compounds_dict = {**reactants, **products}
total_compounds_int = len(total_compounds_dict)
total_symbols_list = []

# A list of symbols is a requirement for sp.linsolve to appropriately solve the system, and each one must be converted
# to sp.Symbol
for key in total_compounds_dict.keys():
    total_symbols_list.append(sp.Symbol(key))

# Checking if the system is balanced by calling the check_rxn_balance function from Chemistry
balance = check_rxn_balance(reactants, products)

# If the balance fails then the magic of sympy will solve it by setting up a system of linear equations and a matrix
if balance is False:
    # The total elements in the equation (H, C, O, etc) need to be obtained
    total_elements_list = list(ptable.formula(''.join(str(compound) for compound in reactants)).atoms)

    # The rows of the equation matrix is each element in the equation
    rows = len(total_elements_list)

    # The columns are the total compounds present in the equation
    cols = total_compounds_int

    # The equation matrix is defined using the zeros function, al slots are set to zero for easy manipulation
    equation_matrix = sp.zeros(rows, cols)

    # y is the counter variable for elements, it represents where the program is in the rows
    y = 0

    for compound in reactants:
        # x does the same thing as y, but for the columns
        x = 0
        composition = ptable.formula(compound).atoms

        for element in total_elements_list:
            # if the element is not present in the compound, it will be stored as a zero in the matrix
            if element not in composition:
                composition[element] = 0

            # The values are stored here, in the matrix and position (x, y). This repeats for each element and compound
            equation_matrix[x, y] = composition[element]

            # x is incremented for the next element
            x += 1

        # y is incremented for the next compound
        y += 1

    # The same loop as above is repeated for products, but the values are stored as negative for the purposes of
    # balancing the chemical equation
    for compound in products:
        x = 0
        composition = ptable.formula(compound).atoms

        for element in total_elements_list:
            if element not in composition:
                composition[element] = 0

            equation_matrix[x, y] = -composition[element]

            x += 1

        y += 1

    # Sympy converts the equation matrix to a sympy compatible matrix object, and creates the solution vector of all 0
    equation_matrix = sp.Matrix(equation_matrix)
    solution_vector = sp.Matrix(sp.zeros(rows, 1))

    # A sympy set object containing values is output by the linsolve function from sympy,
    # which solves the matrix in terms of one of the compounds present (usually the last compound)
    solution_set = sp.linsolve((equation_matrix, solution_vector), total_symbols_list)
    solution_list = []

    # A solution list is derived from the solution set, which is far easier to manipulate and index
    for answer in range(total_compounds_int):
        solution_list.append(next(iter(solution_set))[answer])

    # Whichever symbol is present is the symbol that all coefficients are dependent on
    basis_symbol = next(iter(solution_list[0].atoms(sp.Symbol)))

    # Assume the smallest coefficient is one
    smallest_coefficient = 1

    # The smallest fraction must be obtained to balance in whole coefficients
    for coefficient in range(total_compounds_int):
        # Assuming the basis_symbol is equal to one, it can simply be removed
        solution_list[coefficient] = solution_list[coefficient] / basis_symbol

        # If the coefficient that is left is smaller than the smallest coefficient stored, it will replace
        # the smallest coefficient
        if 0 < (solution_list[coefficient] % 1) < smallest_coefficient:
            smallest_coefficient = solution_list[coefficient] % 1

    # A multiplier will be obtained from the inverse of the smallest coefficient, and all other coefficients will be
    # scaled by that multiplier
    for coefficient in range(total_compounds_int):
        multiplier = smallest_coefficient ** (-1)

        solution_list[coefficient] *= multiplier

    # The coefficients return to the products/reactants dictionaries in their respective compound slots
    for coefficient_counter in range(len(solution_list)):
        if coefficient_counter >= len(reactants):
            products[list(products.keys())[coefficient_counter - len(reactants)]] = solution_list[coefficient_counter]

        else:
            reactants[list(reactants.keys())[coefficient_counter]] = solution_list[coefficient_counter]

    # Assume a divisor of one
    divisor = 1

    # If there is a basis_compound, all coefficients will be scaled by the coefficient of that compound (the divisor)
    if basis_compound != '':
        if basis_compound in reactants:
            divisor = reactants[basis_compound]

        else:
            divisor = products[basis_compound]

        for compound, coefficient in reactants.items():
            reactants[compound] = coefficient / divisor

        for compound, coefficient in products.items():
            products[compound] = coefficient / divisor

# Print reactants and products with an arrow in between
print('{} -> {}'.format(reactants, products))
