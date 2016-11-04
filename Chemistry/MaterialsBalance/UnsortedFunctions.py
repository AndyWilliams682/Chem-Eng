# This has two functions that I didn't really feel like putting into it's own fancy 
# category yet. They will get one eventually

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
