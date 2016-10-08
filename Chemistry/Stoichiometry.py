import numpy as np
import periodictable as ptable

# Possible additions include a better input system

initial_amount = float(input('Input the initial amount '))
initial_units = str(input('Input the initial units '))
initial_formula = str(input('Input the initial compound '))

mole_ratio = float(input('Input the mole ratio '))

final_units = str(input('Input the final units '))
final_formula = str(input('Input the final compound '))

if initial_units == 'g':
    final_amount = initial_amount / ptable.formula(initial_formula).mass
else:
    final_amount = initial_amount

final_amount *= mole_ratio

if final_units == 'g':
    final_amount *= ptable.formula(final_formula).mass

print('{} {} {}'.format(final_amount, final_units, final_formula))
