# These functions pertain to the setup and solving of general balance equations for a given control volume

import sympy as sp


# This function will set up a series of equations based on the control volume dimensions and information input in
# earlier functions. The output is a dictionary of equations tied to the material they are based on (or the info)
def setup(control_volume_dimensions, info_dict):

    equation_dict = {}
    total_volume_unknowns = []

    # compatibility is the measure of an info equations usefulness to the other equations in the path
    # compatibility goes up if the info and the control volume share a variable
    # When compatibility is at maximum (equal to the total symbols in an info equation) then the info can be used
    compatibility = 0

    # Creates a list of all non-info keys in a control volume
    key_list = control_volume_dimensions[0].keys()

    # This main loop creates general balance equations (g_b_e) for the total and all species in the control volume
    for key in key_list:
        g_b_e = 0

        # The direction has no balance equation associated with it, so it can be ignored
        if key != 'Direction':

            # Each path contributes to the g_b_es of the control volume
            for path in control_volume_dimensions:

                # The total balance is set up differently than the species balances
                # It is the sum of 'Total' * 'Direction' values for all paths
                if key == 'Total':
                    g_b_e = sp.Add(g_b_e, sp.Mul(path['Direction'], path[key]))

                # Species are handle similarly, but each total is also multiplied by the fraction for that species
                else:
                    if path[key] != 0:
                        g_b_e = sp.Add(g_b_e, sp.Mul(path['Direction'], sp.Mul(path['Total'], path[key])))

            # This dictionary holds the g_b_es for each material that is involved
            equation_dict[key] = g_b_e

    # This loop determines the total unknowns, in a list, that the control volume has
    for balance, equation in equation_dict.items():
        control_volume_unknowns = equation.atoms(sp.Symbol)

        for volume_unknown in control_volume_unknowns:
            if volume_unknown not in total_volume_unknowns:
                total_volume_unknowns.append(volume_unknown)

    # This loop compares the total_volume_unknowns to a list of unknowns from an info equation
    for info_number, info_equation in info_dict.items():
        info_equation_unknowns = info_equation.atoms(sp.Symbol)

        for info_unknown in info_equation_unknowns:
            if info_unknown in total_volume_unknowns:
                compatibility += 1

        # If an info equation shares all variables with the control volume, then the info equation can be grouped with
        # the other equations for this control volume
        if compatibility == len(info_equation_unknowns):
            equation_dict[info_number] = info_equation

        # compatibility is reset for the next info equation
        compatibility = 0

    # The output is a dictionary that contains all general balance equations and applicable info equations for the
    # control volume
    return equation_dict


# This function uses the equations dictionary from the equations_setup function to solve for all equations in that
# control volume, assuming there are no degrees of freedom. It outputs a dictionary of variables and their solved values
def solver(equations_dict):
    solutions_dict = {}
    solved_equations = 0

    # substitution is True when new variables have been solved for and ready to be implemented into other equations
    substitution = False

    # This loop will continue until all variables are solved
    while True:
        for key, equation in equations_dict.items():

            # A list of all unknowns in an equation is made
            equation_unknowns = [str(x) for x in equation.atoms(sp.Symbol)]

            # If the equation lacks unknowns, then the solved_equations counter is increased
            if len(equation_unknowns) == 0:
                solved_equations += 1

            # If the equation has only one unknown, then it can be easily solved for that unknown
            if len(equation_unknowns) == 1:
                for unknown in equation_unknowns:

                    # The solutions_dict stores the value for the unknown in the corresponding key
                    solutions_dict[unknown] = [value for value in sp.solveset(equation, sp.Symbol(unknown))]

                    # substitution is set to True so other equations can lose an unknown
                    substitution = True

                    # The substitution_unknown is set to the newly solved unknown value
                    sub_unknown = unknown

            # If the equation has two unknowns, then one can be solved in terms of the other
            elif len(equation_unknowns) == 2:
                for unknown in equation_unknowns:

                    # The solutions_dict will store the expression for the unknown in the corresponding key
                    solutions_dict[unknown] = [value for value in sp.solveset(equation, sp.Symbol(unknown))]

                    # substitution will again be set to true, and the sub_unknown is the expression for that unknown
                    substitution = True
                    sub_unknown = unknown

            # This statement sends the solver into the ending sequence if the solved_equations has reached the total
            # equations in the equations_dict
            if solved_equations == len(equations_dict.keys()):

                # This loop will run until the completion_counter has reached the solutions_dict length
                # This loop will solve for all expressions still left in the solutions_dict
                while True:
                    completion_counter = 0

                    # This loop checks every solution from the previous loop for variables
                    for unknown, eq in solutions_dict.items():
                        final_variable_list = [str(x) for x in eq[0].atoms(sp.Symbol)]

                        # If any variables are present, then they must be substituted from the solutions_dict
                        # Eventually, a substitution should occur with no extra variables being added
                        if len(final_variable_list) != 0:
                            sub_unknown = final_variable_list[0]
                            solutions_dict[unknown][0] = eq[0].subs(sp.S(sub_unknown), solutions_dict[sub_unknown][0])

                        # If the unknown is only float/int, then the completion_counter increases by 1
                        else:
                            completion_counter += 1

                    # If the completion_counter is equal to the total unknowns then the code can output the solutions
                    if completion_counter == len(solutions_dict.keys()):
                        return solutions_dict

            # If substitution is True, then sympy will substitute the sub_unknown into the other equations
            if substitution is True:
                for sub_key, sub_equation in equations_dict.items():
                    equations_dict[sub_key] = sub_equation.subs(sp.sympify(sub_unknown), solutions_dict[sub_unknown][0])

                # substitution is reset to False so new unknowns can be substituted
                substitution = False
