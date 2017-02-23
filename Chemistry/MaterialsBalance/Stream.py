import copy

# Add average_molar_mass attribute
# Make the sympy stuff happen in this class


class Stream(object):

    """The Stream() class inherits from a standard dictionary with one overloaded operation (-Stream).
    If stream N.total = 100, then -N returns a stream with total = -100
    A negative total value means that the stream is flowing out of the system"""

    def __init__(self):

        # A dictionary in {component:fraction} format, initially empty
        self.composition = {}

        # The total amount of material in the stream [mass or mol possibly per unit time]
        self.total = 0

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
