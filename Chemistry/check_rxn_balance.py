# This function checks if an equation is balanced
# assuming the input arguments are dictionaries where
# each compound (key) is a str and the values are
# Their respective coefficients

import periodictable as ptable


# Accepts dictionaries for products and reactants
# The keys are compounds (strings) and the values are coefficients for each compound in the reaction
def check_rxn_balance(reactants, products):
    # A giant string containing the appropriate amount of elements is created for both sides of the reaction
    reactants_string = ''.join(coefficient*compound for compound, coefficient in reactants.items())
    products_string = ''.join(coefficient*compound for compound, coefficient in products.items())

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
