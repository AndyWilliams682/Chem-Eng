# This library entails a plethora of functions that lead to the solving of a multi-unit process materials balance
# problem. It can perform a degree of freedom analysis, setup equations and control volume, solve equations and control
# volumes, determine the average molar mass of a system, and identify if a system is in steady state.
#
# Next implementations:
# PyQt UI to avoid ALL THESE INPUTS
# The ability to handle chemical reactions within a unit process

import numpy as np
import periodictable as ptable
import sympy as sp


# Given the fraction type (mole/mass) and a dict relating formula strings to their fraction amounts, this function
# will determine the average molar mass
def det_avg_molar_mass(fraction_type, fractions_dict):
    avg_molar_mass = 0

    for species, fraction in fractions_dict.items():
        molar_mass = ptable.formula(species).mass

        if fraction_type == 'mole':
            avg_molar_mass += fraction * molar_mass

        else:
            avg_molar_mass += fraction / molar_mass

    if fraction_type == 'mass':
        avg_molar_mass = 1 / avg_molar_mass

    return avg_molar_mass


# This function takes no inputs and allows for the creation of a control volume's properties to be organized into
# an array, where each position in the array contains a dict to represent the properties of that path, which are kept
# as sympy expressions for later.
# The lowest arrays are formatted in direction (+1 for in, -1 for out), amount (total moles, mass or
# rates of each, and fractions of said amounts for each compound in the mixture
def control_volume_setup():
    paths = int(input('Input the number of paths crossing the control volume boundary: '))
    paths_in = int(input('Input the number of paths entering the control volume: '))

    compound_count = 0
    species_list = []

    while True:
        compound_count += 1
        compound_input = input('Input the formula of species {}: '.format(compound_count))
        if compound_input == '':
            break
        species_list.append(compound_input)

    control_volume_matrix = []

    for path in range(paths):
        control_volume_matrix.insert(path, {})

    path_counter = 1

    for path in control_volume_matrix:
        path['Direction'] = 1

        for value in range(len(species_list) + 2):
            if value == 0:
                if path_counter > paths_in:
                    path['Direction'] = -1

            elif value == 1:
                path['Total'] = input('Input the total material going through path {}: '.format(path_counter))
                path['Total'] = sp.sympify(path['Total'])

            else:
                material = species_list[value - 2]

                path[material] = input('Input the percentage of {} going through path {}: '.format(material,
                                                                                                   path_counter))
                path[material] = sp.sympify(path[material])

        path_counter += 1

    return control_volume_matrix


def cv_additional_info():
    info_dict = {}
    info_count = 0

    while True:
        info_count += 1
        additional_info = input('Input additional information {}: '.format(info_count))
        if additional_info == '':
            return info_dict

        info_key = 'Info {}'.format(info_count)
        info_dict[info_key] = sp.sympify(additional_info)


# This function uses the control volume setup from the previous function to determine how many unknown values exist
def dof_unknowns(control_volume_dimensions):
    unknown_list = []

    for path in control_volume_dimensions:
        for equation_key, equation_value in path.items():
            for variable in sp.sympify(equation_value).atoms(sp.Symbol):
                if variable not in unknown_list:
                    unknown_list.append(variable)

    unknowns = len(unknown_list)

    return unknowns


# This function uses the dof_unknowns, along with the setup matrix from the first function
# to determine how many degrees of freedom exist in a given control volume
def dof_analysis(control_volume_dimensions, unknowns, info_counter):

    balances = len(control_volume_dimensions[0]) - 2
    information = info_counter
    dof = unknowns - balances - information

    return dof


# This function uses the control volume setup to determine if there is any accumulation in the system
def steady_check(control_volume_dimensions):
    mat_in = 0
    mat_out = 0

    for path in control_volume_dimensions:
        if path[0] > 0:
            mat_in += path[1]

        else:
            mat_out += path[1]

    accumulation = mat_in + mat_out

    if accumulation == 0:
        steady_state = True

    else:
        steady_state = False

    return steady_state


# This code will attempt to solve a materials balance problem given the setup matrix
def cv_equations(control_volume_dimensions, info_dict):
    key_list = control_volume_dimensions[0].keys()
    equation_dict = {}
    variable_list = []
    compatibility = 0

    for key in key_list:
        balance_eq = 0

        if key != 'Direction':
            for path in control_volume_dimensions:
                if key == 'Total':
                    balance_eq = sp.Add(balance_eq, sp.Mul(path['Direction'], path[key]))

                else:
                    if path[key] != 0:
                        balance_eq = sp.Add(balance_eq, sp.Mul(path['Direction'], sp.Mul(path['Total'], path[key])))

            equation_dict[key] = balance_eq

    for key_eq, eq in equation_dict.items():
        variable_count = eq.atoms(sp.Symbol)

        for var in variable_count:
            if var not in variable_list:
                variable_list.append(var)

    for info_number, info_equation in info_dict.items():
        info_equation_variables = info_equation.atoms(sp.Symbol)

        for variable in info_equation_variables:
            if variable in variable_list:
                compatibility += 1

        if compatibility == len(info_equation_variables):
            equation_dict[info_number] = info_equation

        compatibility = 0

    return equation_dict


def cv_equation_solver(equations_dict):
    solutions_dict = {}
    substitution = False
    solved_equations = 0

    while True:
        for key, equation in equations_dict.items():
            variables_list = [str(x) for x in equation.atoms(sp.Symbol)]

            if len(variables_list) == 1:
                for symbol in variables_list:
                    solutions_dict[symbol] = [value for value in sp.solveset(equation)]
                    substitution = True
                    sub_symbol = symbol

            elif len(variables_list) == 2:
                for symbol in variables_list:
                    solutions_dict[symbol] = [value for value in sp.solveset(equation, sp.Symbol(symbol))]
                    substitution = True
                    sub_symbol = symbol

            if len(variables_list) == 0:
                solved_equations += 1

                if solved_equations == len(equations_dict.keys()):
                    while True:
                        completion_counter = 0

                        for symbol, eq in solutions_dict.items():
                            final_variable_list = [str(x) for x in eq[0].atoms(sp.Symbol)]

                            if len(final_variable_list) != 0:
                                sub_symbol = final_variable_list[0]
                                solutions_dict[symbol][0] = eq[0].subs(sp.S(sub_symbol), solutions_dict[sub_symbol][0])

                            else:
                                completion_counter += 1

                        if completion_counter == len(solutions_dict.keys()):
                            return solutions_dict

            if substitution is True:
                for key2, equation2 in equations_dict.items():
                    equations_dict[key2] = equation2.subs(sp.sympify(sub_symbol), solutions_dict[sub_symbol][0])

                substitution = False


# IDEA FOR IMPLEMENTING ADDITIONAL INFORMATION
# Add info onto each equations_dict for each CV
# Once a CV uses it, replace all other instances of {Info 1: blah} in the other equation_dicts with 0
# this is because it can only be used once
def cv_multi_unit_processes():
    cv_count = 0
    cv_list = []
    total_unknowns_list = []
    solutions_dict = {}
    equations_list = []
    info_used_list = []
    cv_max = int(input('Input the number of control volumes: '))

    while cv_count != cv_max:
        cv_count += 1

        print('\n--------------------\nFor Control Volume {}\n--------------------\n'.format(cv_count))

        cv = control_volume_setup()

        for path in cv:
            for k, v in path.items():
                if k != 'Direction':
                    for symbol in v.atoms(sp.Symbol):
                        if symbol not in total_unknowns_list:
                            total_unknowns_list.append(symbol)

        cv_list.append(cv)

    unknown_total = len(total_unknowns_list)

    info_dict = cv_additional_info()

    for i in range(cv_max):
        equations_list.append(0)

    while True:
        cv_count = 0

        for control_volume in cv_list:
            if info_used_list is not []:
                for t in info_used_list:
                    info_dict['Info {}'.format(t)] = sp.sympify('0')
                    info_used_list = []

            if equations_list[cv_count] == 0:
                equations_list[cv_count] = cv_equations(control_volume, info_dict)
                unknowns = dof_unknowns(control_volume)

            else:
                unknowns_list = []

                for key, equation in equations_list[cv_count].items():
                    unknowns_check = equation.atoms(sp.Symbol)

                    for unknown_symbol in unknowns_check:
                        if unknown_symbol not in unknowns_list:
                            unknowns_list.append(unknown_symbol)

                unknowns = len(unknowns_list)

            for n in range(len(info_dict.keys())):
                info_key = 'Info {}'.format(n + 1)

                if info_key in equations_list[cv_count].keys():
                    if equations_list[cv_count][info_key] != 0:
                        info_used_list.append(n + 1)

            dof = dof_analysis(control_volume, unknowns, len(info_used_list))

            if dof == 0:
                solutions_dict = {**solutions_dict, **cv_equation_solver(equations_list[cv_count])}

            else:
                for variable, solution in solutions_dict.items():
                    for key, equation in (equations_list[cv_count]).items():
                        equations_list[cv_count][key] = equation.subs(sp.sympify(variable), solutions_dict[variable][0])

            cv_count += 1

        if len(solutions_dict) == unknown_total:
            return solutions_dict
