# This code takes a particle, with atomic and mass numbers, and any series of decay reactions to output the daughter
# particle.

# import the chemistry
import periodictable as ptable

# User input for the mass and protons of the original atom
particle_properties = [int(input('Mass Number = ')), int(input('Atomic Number = '))]

# Decay is the array that holds the series of reactions
decay = []

# This loop goes until the user inputs an empty string. All other inputs are appended to the decay series
while True:
    decay_inp = str(input('Input the decay ')).lower()
    if decay_inp == '':
        break
    decay.append(decay_inp)

# This loops runs through all reactions in the decay series, applying the appropriate changes
for CurrentReaction in decay:
    if CurrentReaction == 'alpha':
        particle_properties = [particle_properties[0] - 4, particle_properties[1] - 2]

    if CurrentReaction == 'beta':
        particle_properties = [particle_properties[0], particle_properties[1] + 1]

    if CurrentReaction == 'positron':
        particle_properties = [particle_properties[0], particle_properties[1] - 1]

    if CurrentReaction == 'capture':
        particle_properties = [particle_properties[0], particle_properties[1] - 1]

# this converts the proton number to the element number for convenience
element = ptable.elements[particle_properties[1]]

# Prints Mass and Atomic numbers along with the Element symbol
print('Mass Number: {}\nAtomic Number: {}\nElement: {}'.format(particle_properties[0], particle_properties[1], element))
