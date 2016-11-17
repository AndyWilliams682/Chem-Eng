# These functions handle quantifying unknowns and determining the degrees of freedom for a given control volume

import sympy as sp


# This function uses the output of the setup function to determine how many unknown values exist in the control volume
def count_unknowns(control_volume_dimensions):
    list_of_unknowns = []

    # This series of loops checks each path in the control volume. It checks for symbols (variables) in each key, value
    # pair, and if the variable isn't already accounted for, it will be appended to the list_of_unknowns
    for path in control_volume_dimensions[:-1]:
        for key, value in path.items():
            for variable in sp.sympify(value).atoms(sp.Symbol):
                if variable not in list_of_unknowns:
                    list_of_unknowns.append(variable)

    if control_volume_dimensions[-1] != {}:
        for reaction in control_volume_dimensions[-1]:
            if control_volume_dimensions[-1][reaction] != {}:
                for variable in sp.S(control_volume_dimensions[-1][reaction]['Extent']).atoms(sp.Symbol):
                    list_of_unknowns.append(variable)

    unknowns = len(list_of_unknowns)

    return unknowns


# This function uses the dof_unknowns, along with the setup matrix and an info counter to determine how many degrees of
# freedom a given control volume has
def analysis(control_volume_dimensions, unknowns, info_counter):

    balances = len(control_volume_dimensions[0]) - 2

    # The info_counter can change during the process of solving a control volume, keep that in mind when setting this up
    information = info_counter

    # The unknowns can also change depending on the control volume and which variables have been solved for
    dof = unknowns - balances - information

    # The output is the degrees of freedom (int), if this value is zero, then the control volume can be solved
    return dof

if __name__ == '__main__':
    from Chemistry.MaterialsBalance import control_volumes as cv
    
    CV = cv.setup()
    Info_Dict = cv.info()
    Info_Number = len(Info_Dict)
    
    cv_unknowns = count_unknowns(CV)
    print(cv_unknowns)
    print(analysis(CV, cv_unknowns, Info_Number))
