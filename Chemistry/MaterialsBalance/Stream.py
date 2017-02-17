

class Stream(dict):

    """The Stream() class inherits from a standard dictionary with one overloaded operation (-Stream).
    If stream N = {'Total': 100, 'H2O': 1}, then -N returns {'Total': -100, 'H2O': 1}
    A negative 'Total' value means that the stream is flowing out of the system"""

    def __init__(self):
        # The class inherits from a dictionary base class
        super(self.__class__, self).__init__()

    # This overloads the __neg__ operator for easy switching of the direction of a stream
    def __neg__(self):
        # It must return a new Stream, leaving the original self untouched
        out_stream = None

        # Checks if the Stream has a 'Total' key to prevent errors
        if 'Total' in self.keys():
            # Creates a copy of the original Stream in a new space of memory, then changes the 'Total' value to negative
            out_stream = Stream()
            out_stream.update(self)
            out_stream['Total'] *= -1

        # If no 'Total' is present then the negation cannot be done
        else:
            print('Error, no \'Total\' found in stream')

        return out_stream
