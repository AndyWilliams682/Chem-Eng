import copy
from Chemistry.MaterialsBalance.System import System
import sympy as sp

# Add average_molar_mass attribute
# Make the sympy stuff happen in this class


class Stream(object):

    """The Stream() class inherits from a standard dictionary with one overloaded operation (-Stream).
    If stream N.total = 100, then -N returns a stream with total = -100
    A negative total value means that the stream is flowing out of the system"""

    def __init__(self, total, composition, start, end):

        # A dictionary in {component:fraction} format, initially empty
        self.composition = composition

        self.composition_constraint()

        # The total amount of material in the stream [mass or mol possibly per unit time]
        self.total = total

        # In order to create a graph of the known streams, their connecting nodes must be known. Differentiating
        # between start and end will allow for directionality to come into play
        self.start = start
        self.end = end

    # This overloads the __neg__ operator for easy switching of the direction of a stream
    def __neg__(self):
        # It must return a new Stream, leaving the original self untouched
        out_stream = None

        # Checks if the Stream has a total attribute to prevent errors
        if self.total != 0:
            # Creates a copy of the original Stream in a new space of memory, then changes the total value to negative
            out_stream = copy.deepcopy(self)
            out_stream.total *= -1

        # If no total is present then the negation cannot be done
        else:
            print('Error, no \'total\' found in stream')

        return out_stream

    def __add__(self, addend_stream):

        balances = {}

        for material in set(list(self.composition.keys()) + list(addend_stream.composition.keys())):
            self.update_composition(material)
            addend_stream.update_composition(material)
            balances[material] = sp.S((self.total * self.composition[material] +
                                       addend_stream.total * addend_stream.composition[material]))

        return System(balances)

    def update_composition(self, material):
        if material not in self.composition.keys():
            self.composition[material] = 0

    def composition_constraint(self):

        composition_equation = sp.S('1')
        variable = None

        for material, fraction in self.composition.items():
            composition_equation -= fraction

            if type(fraction) == sp.Symbol:
                variable = (material, fraction)

        if len(composition_equation.atoms(sp.Symbol)) > 0:
            composition_equation = sp.solve(composition_equation, variable[1])
            self.composition[variable[0]] = self.composition[variable[0]].subs(variable[1], composition_equation[0])


if __name__ == '__main__':
    S1 = Stream(sp.S('m1'), {'A': 0.5, 'B': 0.5}, 'Surr', 'a')
    S2 = Stream(5, {'A': sp.S('X2A'), 'B': sp.S('X2B')}, 'Surr', 'a')
    print((S1 + S2).balances)
