import sympy as sp


def solve(control_volume_list):

    """The solve() function takes a list of ControlVolume objects as inputs and, assuming it is possible, solve the
    system for all unknowns. The solutions will be output in the variables_dict with key:value pairs in the form of
    unknown:solution."""

    # The variables_dict is the output of the function
    variables_dict = {}

    # The remove list is used to take solved volumes out of the system
    remove_list = []

    # initial is only True for the first loop
    initial = True

    # This is set to None to prevent the len() of the empty variables_dict from ending the while loop
    solved_variables = None

    # This loop continues until the total number of solved solutions is equal to the unknowns present in the system
    while solved_variables != len(variables_dict):

        # This loop manipulates the variables_dict for each volume in the system
        for volume in control_volume_list:

            # If the volume has zero degrees of freedom, it's solved variables will be added the the variables_dict
            if volume.degrees_of_freedom == 0:
                variables_dict.update(volume.dict_of_variables)

                # Solved volumes provide no more useful information, so they are to be removed in the remove loop
                remove_list.append(volume)

            # If the system still needs to be solved...
            else:

                # ...and if this is the first run through the loop, the unsolved variables are added to
                # the variables_dict
                if initial is True:
                    for unknown, symbol in volume.dict_of_variables.items():
                        if unknown not in variables_dict.keys():
                            variables_dict[unknown] = symbol

        # Once the first loop above has finished, initial is set to False and left untouched
        if initial is True:
            initial = False

        # This is the remove loop, all solved volumes get removed from the control_volume_list
        for volume in remove_list:
            control_volume_list.remove(volume)

        # The remove_list is reset for the next iteration
        remove_list = []

        # Now the remaining, unsolved volumes must use the newly gathered information to reduce their degrees of freedom
        # This is done using the ControlVolume method subs()
        for volume in control_volume_list:
            volume.subs(variables_dict)

        # The solved variables can now be set to zero as the variables_dict has a length greater than zero
        solved_variables = 0

        # Each variable is checked in the variables_dict
        for variable, solution in variables_dict.items():

            # If the variable lacks sympy symbols (unknowns) then it is a solved variable and the counter can increase
            if len(solution.atoms(sp.Symbol)) < 1:
                solved_variables += 1

    # Once every variable has been solved, the function will return the variables_dict with all solutions
    return variables_dict
