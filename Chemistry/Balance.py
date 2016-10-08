# This program will balance chemical reactions hopefully
# THIS PROJECT IS BEING PUT ON HOLD
import numpy as np
import sympy as sp
import periodictable as ptable
from Chemistry.check_balance import check_balance

reactants_count = 0
reactants = []

products_count = 0
products = []

while True:
    reactants_count += 1
    compound_input = input('Input the formula of reactant {}: '.format(reactants_count))
    if compound_input == '':
        break
    reactants.append(compound_input)

while True:
    products_count += 1
    compound_input = input('Input the formula of product {}: '.format(products_count))
    if compound_input == '':
        break
    products.append(compound_input)

total_compounds = reactants + products
total_symbols = []

for count in range(len(total_compounds)):
    total_symbols.append(sp.Symbol(total_compounds[count]))

balance = check_balance(reactants, products)

if balance is False:
    total_elements_list = list(ptable.formula(''.join(str(compound) for compound in reactants)).atoms)

    rows = len(total_elements_list)
    cols = len(reactants) + len(products)
    equation_matrix = sp.zeros(rows, cols)

    y = 0

    for compound in reactants:
        x = 0
        composition = ptable.formula(compound).atoms

        for element in total_elements_list:

            if element not in composition:
                composition[element] = 0

            equation_matrix[x, y] = composition[element]

            x += 1

        y += 1

    for compound in products:
        x = 0
        composition = ptable.formula(compound).atoms

        for element in total_elements_list:

            if element not in composition:
                composition[element] = 0

            equation_matrix[x, y] = -composition[element]

            x += 1

        y += 1

    equation_matrix = sp.Matrix(equation_matrix)
    solution_vector = sp.Matrix(sp.zeros(rows, 1))

    solution = sp.linsolve((equation_matrix, solution_vector), total_symbols)
    print(solution)
