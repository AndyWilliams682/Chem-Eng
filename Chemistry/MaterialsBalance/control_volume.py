# These functions pertain to the setup of a control volume's dimensions, along with additional info tied to the volume

import sympy as sp


# This function takes no inputs and allows for the input of a control volume's properties to be organized into
# an array, where each position in the array contains a dict to represent the properties of that path, which are kept
# as sympy expressions for later
def setup(reaction_dict):
    # The user must provide the total number of paths into a control volume, and the total number oriented into the CV
    paths = int(input('Input the number of paths crossing the control volume boundary: '))
    paths_in = int(input('Input the number of paths entering the control volume: '))

    # compound_count allows for clearer input prompts
    compound_count = 0
    list_of_species = []

    # control_volume_dimensions[path number - 1] == {'Direction': 1/-1 (in or out), 'Total': total material in path,
    # 'compound 1/2/3...': fraction of material in path}
    #
    # control_volume_dimensions == [path 1, path 2, path 3, ..., path n, reactions]
    # control_volume_dimensions[-1] == {Reaction 1: {reactant: coefficient, product: coefficient, Extent: rxn extent}}
    #
    # Note that units of the total and the fractions must agree (Total = kg/s, fractions must be mass fractions)
    # Variables can simply be input as variables (n1, y2, x5, m8, xi1, etc)
    control_volume_dimensions = []

    # Each path and the reactions present are represented by dictionaries in the control_volume_dimensions list
    for path in range(paths + 1):
        control_volume_dimensions.insert(path, {})

    while True:
        reaction_key = str(input('Input the integer that represents a reaction present in this control volume: '))

        if reaction_key == '':
            break

        control_volume_dimensions[-1][reaction_key] = reaction_dict[reaction_key]

        for species in list(reaction_dict[reaction_key].keys()):
            if species != 'Extent':
                if species not in list_of_species:
                    list_of_species.append(species)
                    compound_count += 1

    # This loop takes inputs until an empty string is provided. Each new string is appended to the list_of_species
    while True:
        compound_count += 1
        compound_input = input('Input the formula of species {}: '.format(compound_count))
        if compound_input == '':
            break
        list_of_species.append(compound_input)

    path_counter = 1

    # This loop begins the construction of the control_volume_dimensions. Paths oriented in must be input first to
    # ensure their 'Direction' value matches up
    # The sympify function from sympy is used to evaluate strings into floating point or expressions
    for path in control_volume_dimensions[:-1]:
        path['Direction'] = 1

        # This loop covers all keys in a given path (the list of species plus direction and total)
        for value in range(len(list_of_species) + 2):

            # This statement checks if the path is oriented in or out and assigns +/- 1 for 'Direction' (in/out)
            if value == 0:
                if path_counter > paths_in:
                    path['Direction'] = -1

            # This statement prompts the user to input the total material through the given path
            elif value == 1:
                path['Total'] = sp.S(input('Input the total material going through path {}: '.format(path_counter)))

            # All other possibilities are fractions for different species in the species list; this prompts the user to
            # input the percentage of each compound in the given path
            else:
                material = list_of_species[value - 2]
                path[material] = sp.S(input('Input the fraction of {} going through path {}: '.format(material,
                                                                                                      path_counter)))
        # The path counter increases for clarity of input prompts
        path_counter += 1

    # The control_volume_dimensions are output for use in other functions
    return control_volume_dimensions


# This function is the final input function for the solving of a control volume. It creates a dictionary with keys
# 'Info 1', 'Info 2', etc until no more information is provided. Inputs must be expressions that are assumed to be set
# equal to zero (NOT x = 1, but x - 1). These expressions are stored with their respective keys for later use in the
# equations function.
def info():
    info_dict = {}
    info_count = 0

    while True:
        info_count += 1
        additional_info = input('Input additional information {}: '.format(info_count))
        if additional_info == '':
            return info_dict

        info_key = 'Info {}'.format(info_count)
        info_dict[info_key] = sp.sympify(additional_info)


if __name__ == '__main__':
    from Chemistry.MaterialsBalance import chemical_reactions as rxn
    reaction_dictionary = rxn.setup()
    print(setup(reaction_dictionary))
    print(info())
