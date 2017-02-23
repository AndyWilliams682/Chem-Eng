import sympy as sp

# Ideas:
# Attribute: name (eg mixer) for use with dictionaries instead of lists
#
# The ability to add control volumes together to create a larger volume. They must share streams!
# The ability to add control volumes and streams


class ControlVolume(object):

    """The ControlVolume object is used to represent a boundary over which streams cross and in which reactions occur.
    Each combination of streams and reactions is generally specific to each ControlVolume while the total information
    given to solve a system can span across multiple ControlVolumes.

    The input streams must be a list of Stream objects. reactions must be a list of Reaction objects
    and the total_information must be a list of sympy expressions (which are assumed to equal zero).

    When a ControlVolume is created, it will automatically identify which parts of the total_information apply to the
    system. All unknowns will be stored in the variables_dict for the ControlVolume."""

    def __init__(self, reactions, streams, total_information):

        """Each input is automatically used to build the equations used to solve the ControlVolume variables.
        The specifics to how this works are described in the comments of the code."""

        # Attaches the inputs to the ControlVolume self
        self.reactions = reactions
        self.streams = streams
        self.total_information = total_information

        # The equations_dict will hold all equations that can be used to solve the system
        # The dict_of_variables holds all unknowns and their solutions (or symbols if no solution has been found yet)
        self.equations_dict = {}
        self.dict_of_variables = {}

        # This loop accounts for the mass flowing in and out of the system, known as streams
        for stream in self.streams:

            # It first creates empty equation dictionaries for each unique key in all the streams ('Total', 'H2O')
            for material, value in stream.items():

                # Each material provides only one equation, along with a 'Total' equation for the system, no duplicates
                if material not in self.equations_dict:
                    self.equations_dict[material] = 0

                # If an unknown is found, it is added the the dict_of_variables which stores what needs to be solved
                for variable in value.atoms(sp.Symbol):

                    # No duplicates can exist in the dict_of_variables
                    if variable not in self.dict_of_variables:
                        self.dict_of_variables[variable] = variable

                # This fraction is set for when material == 'Total', as the total lacks any fraction that scales it
                fraction = 1

                # If the material is anything but 'Total' (like 'H2O') then it's fraction in the stream is used
                if material != 'Total':
                    fraction = value

                # The balance equation for each material adds the given part for each stream
                # Advanced sympy operator functions are used to modify the equation in a manner that builds it properly
                # Ex: 'Total': n1 + n2 - n3 - n4 = 0, n is a mole total for a given stream
                # Ex: 'H2O': y1n1 + y2n2 - y3n3 - y4n4 = 0, where y is the mole fraction for a given stream
                self.equations_dict[material] = sp.Add(self.equations_dict[material], sp.Mul(fraction, stream['Total']))

        # This loop adds the mass generated or consumed for each material in the system
        for reaction in self.reactions:

            for material, coefficient in reaction.species.items():

                # Each material equation will add the reaction contribution similarly to the streams
                self.equations_dict[material] = sp.Add(self.equations_dict[material],
                                                       sp.Mul(coefficient, reaction.extent))

            # If there is a new unknown, it will be added to the dict_of_variables
            for variable in reaction.extent.atoms(sp.Symbol):
                if variable not in self.dict_of_variables:
                    self.dict_of_variables[variable] = variable

            # The total molar_change when used with the extent will contribute to the 'Total' equation
            self.equations_dict['Total'] = sp.Add(self.equations_dict['Total'],
                                                  sp.Mul(reaction.molar_change, reaction.extent))

        # The info_counter must be set to zero before the next loop
        self.info_counter = 0

        # This loop must check for the compatibility of each extra info equation to the system
        for equation in self.total_information:

            # Compatibility represents how useful an equation will be to the ControlVolume
            compatibility = 0

            # The info_unknowns is every unknown found in the given info equation
            info_unknowns = equation.atoms(sp.Symbol)

            # If the equation and the system share a variable, compatibility increases
            for variable in info_unknowns:
                if variable in self.dict_of_variables:
                    compatibility += 1

            # If every variable in the equation is also present in the ControlVolume, then the equation is useful
            # and it is stored in the equations_dict
            if compatibility == len(info_unknowns):

                # The info_counter is used to maintain nice keys for the info in the equations_dict (Ex: 'Info 1')
                self.info_counter += 1
                self.equations_dict['Info {}'.format(self.info_counter)] = equation

        # The total number unknowns in the system and a pre-allocation of the degrees of freedom in the system
        self.unknowns = len(self.dict_of_variables)
        self.degrees_of_freedom = None

        # This method will determine the degrees of freedom for the system
        self.degrees_of_freedom_update()

    def subs(self, substitution_dict):

        """The subs() method allows for unknowns found from other ControlVolumes to be substituted into the equations
        for this system, reducing the total number of unknowns and the total degrees of freedom (hopefully until the
        degrees of freedom for the system reach zero and it becomes solvable). It requires a dictionary of
        variable:solution format from which it will substitute values into the ControlVolume equations_dict."""

        # This list is created to store equations that are no longer useful and remove them
        # This occurs when an equation (generally an info equation) is used in another ControlVolume which implies that
        # all variables in that equation have been solved and it cannot provide any new relationships to the system
        remove_equation_list = []

        # For each solved variable in substitution_dict
        for substitution, solution in substitution_dict.items():

            # The substitution must meet 3 characteristics: it must exist in the current ControlVolume as a variable,
            # the variable in the ControlVolume must be unknown (a sympy Symbol, not a value), and the substitution must
            # be solved (it itself has zero unknowns in the form of sympy Symbols)
            if substitution in self.dict_of_variables and type(self.dict_of_variables[substitution]) == sp.Symbol and \
                            len(solution.atoms(sp.Symbol)) < 1:

                # If this is true, then the ControlVolume can remove the variable from it's dict_of_variables as it has
                # already been solved and doesn't need to be solved again. The total unknowns decreases by one
                self.dict_of_variables.pop(substitution)
                self.unknowns -= 1

                # Each equation needs to substitute the unknown for it's solved solution using the sympy subs() method
                for key, equation in self.equations_dict.items():
                    self.equations_dict[key] = equation.subs(substitution, solution)

                    # This if statement checks if the equation has become irrelevant (nothing to solve, just 0)
                    # If the equation lacks unknowns, it will be removed from the equations_dict for the ControlVolume
                    if len(self.equations_dict[key].atoms(sp.Symbol)) == 0:
                        remove_equation_list.append(key)

                # This loop removes every equation that is no longer useful
                for key in remove_equation_list:
                    self.equations_dict.pop(key)

        # After a substitution is done, the degrees of freedom have likely changed, so the ControlVolume will update it
        self.degrees_of_freedom_update()

    def degrees_of_freedom_update(self):

        """This method calculates and updates the degrees of freedom for a system. If the system has as many equations
        as it has unknowns, then it as zero degrees of freedom and will be solved. Otherwise, it must wait for a
        substitution to occur to lower the unknowns in the system."""

        # The degrees of freedom equation
        self.degrees_of_freedom = self.unknowns - len(self.equations_dict) + 1

        # If the system lacks any degrees of freedom, then it is solvable, and the solve() method will run
        if self.degrees_of_freedom == 0:
            print('Solving control volume {}'.format(self))
            self.solve()

    def solve(self):

        """The solve method will build a matrix that sympy can solve with the sympy.solve() function. It will return the
        values in a dict which will then be used to store all solved unknowns to the dict_of_variables of the system."""

        # A pre-allocation for the matrix used to solve the system
        matrix = []

        # Each unknown must be put into a list so sympy can solve it
        unknowns_list = list(self.dict_of_variables.keys())

        # Each equation (except for the 'Total') will be appended to the matrix. This is done to allow for the user
        # or the code (when this feature is added) to easily double check the variables for accuracy
        for key, equation in self.equations_dict.items():
            if key != 'Total':
                matrix.append(equation)

        # sympy does it's thing and returns a dict in the form of {symbol: solution}
        solutions = sp.solve(matrix, unknowns_list, dict=True)

        # This loop updates the dict_of_variables with the newly solved values for each
        for solutions_set in solutions:

            # This is done because the solutions are given in a list containing a dictionary: [{}], which is weird
            for count in range(len(solutions_set)):

                # The newly solved variables can be used to solve other ControlVolumes
                self.dict_of_variables[unknowns_list[count]] = solutions_set[unknowns_list[count]]
