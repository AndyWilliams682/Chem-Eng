def check_balance(reactants, products):

    # This function checks if an equation is balanced
    # assuming the input arguments are arrays where
    # each compound is a str in a different position

    import numpy as np
    import periodictable as ptable

    reactants_string = ''.join(compound for compound in reactants)
    products_string = ''.join(compound for compound in products)

    reactants_atoms = ptable.formula(reactants_string).atoms
    products_atoms = ptable.formula(products_string).atoms

    if reactants_atoms == products_atoms:
        balance = True

    else:
        balance = False

    return balance
