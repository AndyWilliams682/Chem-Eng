# This script handles the input and solving of a multiple unit process using general balance equations provided that it
# is solvable (determined using a degree of freedom analysis).

# sympy is used to store and manipulate expressions
# All inputs are handled using functions from the control_volumes module
# Chemical Reaction balancing is done with the chemical_reactions module
# The degrees_of_freedom module is used to determine if a control volume is solvable
# The balance_equations module builds and solves general balance equations for the control volume
import sympy as sp
from Chemistry.MaterialsBalance import control_volumes as cvs
from Chemistry.MaterialsBalance import chemical_reactions as rxn
from Chemistry.MaterialsBalance import degrees_of_freedom as dof
from Chemistry.MaterialsBalance import balance_equations as eqs

CV_list = []
total_unknowns_list = []
solutions_dict = {}
equations_list = []
info_used_list = []

# The setup function from the chemical_reaction module is called to obtain every present reaction in the whole system
reaction_dict = rxn.setup()

# CV_count is used to determine if the maximum number of control volumes has been reached
CV_count = 0

# This determines the total control volumes defined in the process
CV_max = int(input('\nInput the number of control volumes: '))

# A continuous loop until the control_volume max has been reached
while CV_count != CV_max:

    # CV_count allows for tracking control volumes, and clearer input prompts
    CV_count += 1

    # Printed for organizational purposes
    print('\n--------------------\nFor Control Volume {}\n--------------------\n'.format(CV_count))

    # Function called from ControlVolume. Takes in a large amount of inputs to construct a control volume
    CV = cvs.setup(reaction_dict)

    # For loop that checks each section in a control volume for unknowns, and appends them to the total_unknowns_list
    for path in CV[:-1]:
        for k, v in path.items():
            if k != 'Direction':
                for symbol in v.atoms(sp.Symbol):
                    if symbol not in total_unknowns_list:
                        total_unknowns_list.append(symbol)
    
    # If a reaction is present, then each reaction with an unknown extent will be included in the total_unknowns_list
    if CV[-1] != {}:
        for reaction in CV[-1]:
            if CV[-1][reaction] != {}:
                CV[-1][reaction] = rxn.reaction_balance(CV[-1][reaction])

                for symbol in sp.S(CV[-1][reaction]['Extent']).atoms(sp.Symbol):
                    if symbol not in total_unknowns_list:
                        total_unknowns_list.append(symbol)

    # Current control volume is added to the control volume list
    CV_list.append(CV)

# The unknowns in the process are counted
unknown_total = len(total_unknowns_list)

# Function called from ControlVolume. Takes in inputs until '' is provided. All inputs must be expressions set equal to
# zero
info_dict = cvs.info()

# Predetermining the size of the equations_list by storing zeroes in the required slots
for i in range(CV_max):
    equations_list.append(0)

# The setup part of this script is finished. This is where the math happens
# while loop continues until all variables have a solution (either a value or an expression)
while True:

    # The CV_count is reset upon each run of the solving loops
    CV_count = 0

    # checks every control_volume in the CV_list
    for control_volume in CV_list:

        # Statement checks if a prior control volume has used an info equation, it would be stored in the info_used_list
        if info_used_list is not []:

            # Runs through the values in the info_used_list (which are integers) and removes them from the other control
            # volumes. Once an info equation has been used, it cannot be used elsewhere
            for t in info_used_list:
                info_dict['Info {}'.format(t)] = sp.sympify('0')

                # info_used_list is reset for the next info equations that are used
                info_used_list = []

        # if no equations have been setup for the control volume, then this statement will create a dict containing all
        # pertinent general balance equations and info equations
        if equations_list[CV_count] == 0:
            equations_list[CV_count] = eqs.setup(control_volume, info_dict)

            # Unknowns in the control volume are also counted using a function from DegreesOfFreedom
            unknowns = dof.count_unknowns(control_volume)

        # Equations have already been setup for the control volume, and are ready to be manipulated
        else:
            unknowns_list = []

            # A separate check for unknowns using the equations of a given control volume
            # This is more useful since unknowns in the equations can change in the process of solving them whereas the
            # control volume dimensions are no altered after being created
            for key, equation in equations_list[CV_count].items():
                unknowns_check = equation.atoms(sp.Symbol)

                for unknown_symbol in unknowns_check:
                    if unknown_symbol not in unknowns_list:
                        unknowns_list.append(unknown_symbol)

            unknowns = len(unknowns_list)

        # This checks each for each info equation in the equations_list for a given control volume
        # if the equation key is present (and not equal to zero) then the info number is appended to the info_used_list
        for n in range(len(info_dict.keys())):
            info_key = 'Info {}'.format(n + 1)

            if info_key in equations_list[CV_count].keys():
                if equations_list[CV_count][info_key] != 0:
                    info_used_list.append(n + 1)

        # Function called from DegreesOfFreedom. It determines if a control volume is solvable (dof must equal zero)
        DOF = dof.analysis(control_volume, unknowns, len(info_used_list))

        # if the control volume is solvable at this point, the script will attempt to solve it using sympy
        if DOF == 0:

            # Combines the solutions_dict with any newly solved variables from the solver function found in
            # the BalanceEquations module
            solutions_dict = {**solutions_dict, **eqs.solver(equations_list[CV_count])}

        # if the equation is not solvable (or has been solved already) then it will substitute any solved variables
        # into unsolved equations to reduce the degrees of freedom of other control volumes
        else:
            for variable, solution in solutions_dict.items():
                for key, equation in (equations_list[CV_count]).items():

                    # The sympy method subs() is used on expressions to replace variables with their solved forms
                    equations_list[CV_count][key] = equation.subs(sp.sympify(variable), solutions_dict[variable][0])

        # Increments the CV_count so that the next control volume is checked
        CV_count += 1

    # if the total number of solved variables in the solutions_dict is equal to the total number of unknowns from the
    # beginning of the script, then the while loop can end. All variables should be solved
    if len(solutions_dict) == unknown_total:
        break

# Print the output of variables to the screen
print(solutions_dict)
