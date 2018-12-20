from Chemistry.MaterialsBalance.Stream import Stream
from Chemistry.MaterialsBalance.System import System
import sympy as sp
from sympy import S
import itertools

'''S1 = Stream(10, {'A': S('x1A'), 'B': S('x1B')}, 'Surr', 'm')
S2 = Stream(S('m2'), {'A': 0.8, 'B': S('x2B'), 'C': S('x2C')}, 'm', 'a')
S3 = Stream(20, {'A': S('x3A'), 'B': 0.1, 'C': S('x3C')}, 'a', 'b')
S4 = Stream(S('m4'), {'A': S('x4A'), 'C': S('x4C')}, 'b', 'c')
S5 = Stream(15, {'A': S('x5A'), 'C': S('x5C')}, 'c', 'Surr')
S6 = Stream(S('m6'), {'A': S('x6A'), 'B': S('x6B'), 'C': S('x6C')}, 'b', 'd')
S7 = Stream(S('m7'), {'B': S('x7B')}, 'd', 'Surr')
S8 = Stream(S('m8'), {'C': S('x8C')}, 'Surr', 'b')
S9 = Stream(S('m9'), {'A': S('x9A'), 'C': S('x9C')}, 'd', 'm')

streams = [S1, S2, S3, S4, S5, S6, S7, S8, S9]'''

SF = Stream(S('F'), {'A': 0.16, 'B': 1 - 0.16}, 'Surr', 'a')
SD = Stream(21772.45965, {'A': 0.96, 'B': 1 - 0.96}, 'a', 'Surr')
SW = Stream(S('W'), {'A': 0.038, 'B': 1 - 0.038}, 'a', 'Surr')

streams = [SF, SD, SW]
systems = {}

for stream in streams:
    if stream.start != 'Surr':
        if stream.start not in systems.keys():
            systems[stream.start] = System({})

        systems[stream.start] += -stream

    if stream.end != 'Surr':
        if stream.end not in systems.keys():
            systems[stream.end] = System({})

        systems[stream.end] += stream

solved_variables = {}
total_unknowns = set()

unknowns_counted = False
first_pass = False

while len(solved_variables.keys()) != len(total_unknowns) or unknowns_counted is False:

    for L in range(0, len(systems) + 1):
        for subset in itertools.combinations(systems, L):

            subset_system = System({})

            if len(subset) == 0:
                if first_pass is False:
                    first_pass = True

                else:
                    unknowns_counted = True

            for system in subset:
                subset_system += systems[system]

                if unknowns_counted is False and len(subset) == 1:
                    total_unknowns = total_unknowns.union(systems[system].unknowns)

            if subset_system.solutions is not None:
                for thing in subset_system.solutions:

                    solved_variables = {**solved_variables, **thing}

                    for variable, value in thing.items():
                        for system in systems.keys():
                            systems[system].substitute(variable, value)

                print(subset, subset_system.DoF)
                print('solved')

print(solved_variables)
