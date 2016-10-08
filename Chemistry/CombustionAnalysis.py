# This code does combustion analysis for MOST CH and CHO fuels provided the fuel mass, CO2 mass, and H2O mass

# Import numpy and periodictable to do the chemistry
import numpy as np
import periodictable as ptable

# User input for necessary masses (initial fuel, CO2, and H2O)
fuel_mass = float(input('Input the mass of compound combusted '))
CO2_mass = float(input('Input the mass of CO2 produced '))
H2O_mass = float(input('Input the mass of H2O produced '))

# Calling ptable to convert CO2 mass to C mass to C mol
C_mass = CO2_mass * ptable.C.mass / ptable.formula('CO2').mass
C_mol = C_mass / ptable.C.mass

# Same for H2O to H mass to H mol
H_mass = H2O_mass * 2 * ptable.H.mass / ptable.formula('H2O').mass
H_mol = H_mass / ptable.H.mass

# O mass is the remaining mass in the fuel, convert to moles
O_mass = fuel_mass - H_mass - C_mass
O_mol = O_mass / ptable.O.mass

# A list of valid mole values
mol_values = [C_mol, H_mol]

# If the O_mass is valid, then O_mol is added to the moles list. If not, ignore it
if O_mass < 0.01:
    O_mol = 0
else:
    mol_values = mol_values + [O_mol]

# The minimum must be defined initially, it's just the first one in the list (Carbon)
min_mol = mol_values[0]

# Testing all mol values to see which is smallest using subtraction
for value in mol_values:
    if value - min_mol <= 0:
        min_mol = value

# The empirical values are acquired through division of lowest mole value, then rounded
C_empirical = round(C_mol / min_mol)
H_empirical = round(H_mol / min_mol)
O_empirical = round(O_mol / min_mol)

# Print the empirical formula HUZZAH
print('The empirical formula is C{}H{}O{}'.format(C_empirical, H_empirical, O_empirical))

# Need to add a script or extension that can solve for molecular formula
# Script does not work if fractions are required to solve the bullshit, maybe I'll add that later
