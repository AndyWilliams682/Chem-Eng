# This library entails a plethora of functions that lead to the solving of a multi-unit process materials balance
# problem. It can perform a degree of freedom analysis, setup equations and control volume, solve equations and control
# volumes, determine the average molar mass of a system, and identify if a system is in steady state.
#
# Next implementations:
# PyQt UI to avoid ALL THESE INPUTS
# The ability to handle chemical reactions within a unit process

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


# This function uses the control volume setup to determine if there is any accumulation in the system.
# IT IS NOT FINISHED
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
