import sys
import sympy as sp
from PyQt5 import QtWidgets
from Chemistry.MaterialsBalance.Stream import Stream
from Chemistry.MaterialsBalance.Reaction import Reaction
from Chemistry.MaterialsBalance.ControlVolume import ControlVolume
from Chemistry.MaterialsBalance import mainwindow
from Chemistry.MaterialsBalance.Materials_Balance_Solver import solve

# To do:
# A script or file that allows users to confirm if their system is solvable using DoF analysis. Just lets them know
# if the system is under or over specified and if they must assume a basis, etc.
#
# Possibly create a main file that calls everything else for ease
#
# Make it so it definitely ignores empty rows of stuff
# Lots of if statements just for every possible exception
# Try pretty hard to break it and then sanitize the inputs (this can always be improved)
# Make instructions painfully clear
#
# Table rows should have editable names, that way reactions/volumes can be titled and everything can use a dict/obj
#
# On the streams page, if all fractions are filled but one, automatically input a 1 - x1 - x2 ... - xn equation OR
# input a symbol with that format equation in the info list
#
# Maybe replace the final script with a overall_system object that has a solve method
#
# Add the option to use units for the totals in each stream, as it currently assumes moles (this will likely be a mess)
# Unit conversion methods for streams
#
# A linear independence checker for the equations as some things (splitters) will not work for solving equations
#
# The ability to save/load tables for further editing


class MassBalanceUI(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):

    """This is object takes the UI from mainwindow and adds functionality. This is done using PyQt5. It allows for the
    values entered in the table widgets to be read and stored, and later manipulated to solve systems. A plethora of
    methods exist in this class that allow for the UI to update as it is used. More functionality may be added to this
    as it is very modular and a user interface can have lots of useful features.

    The user is prompted to build a series of pieces (reactions, streams, information) to generate the ControlVolume
    objects that will be used to solve the multi-unit system."""

    def __init__(self, parent=None):
        super(MassBalanceUI, self).__init__(parent)

        # setupUi is from the mainwindow class
        self.setupUi(self)

        # The right display is where the table widgets are shown
        self.listWidget.currentRowChanged.connect(self.right_display)

        # Pre-allocations occur here for each element of the UI: reactions, inerts, streams, info, and volumes
        self.reaction_counter = 0
        self.list_of_reactions = []

        self.list_of_inerts = []
        self.materials = []

        self.stream_counter = 0
        self.list_of_streams = []

        self.info_counter = 0
        self.list_of_info = []

        self.volume_counter = 0
        self.list_of_volumes = []

        # This states that when a cell in a table is clicked, the connected methods will run
        self.reactionWidget.cellClicked.connect(self.new_reaction)
        self.streamWidget.cellClicked.connect(self.new_stream)
        self.infoWidget.cellClicked.connect(self.new_info)
        self.volumeWidget.cellClicked.connect(self.new_volume)

        # The solve button is connected to the solve_system method
        self.solveButton.clicked.connect(self.solve_system)

    def right_display(self, i):

        # The right display is a stacked widget with 4 pages, one for each tab in the list on the upper left
        # The lists correspond to each page, first is reactions, then streams, info, and volumes
        self.stackedWidget.setCurrentIndex(i)

    # This adds a new row, which represents a reaction, if the bottom row is clicked
    def new_reaction(self):

        # If the cell clicked is at the bottom of the table widget then it will add a new row second from the bottom
        if self.reactionWidget.currentRow() == self.reaction_counter:
            self.reactionWidget.insertRow(self.reaction_counter)
            self.reaction_counter += 1

    # This method updates the stream tables to include all materials from the reactions/inerts page
    # Each material is added as a column for the table
    # This method also generates the reaction list (a feature I may move to a different method for clarity)
    def reaction_list_generator(self):

        # Every reaction must be checked for new materials
        for reaction in range(self.reaction_counter):

            # Obtaining data from the table widget using the .text() method
            reaction_materials = self.reactionWidget.item(reaction, 0).text().split()
            coefficients = self.reactionWidget.item(reaction, 1).text().split()

            # If there are not enough coefficients in the reaction table, it will not progress
            if len(coefficients) != len(reaction_materials):
                print('Error, not enough materials or coefficients')
                self.list_of_reactions = []
                return

            # If enough information is provided for the reactions/inerts table then the total materials will be stored
            else:

                # Reaction objects are made and stored in the overall list_of_reactions for later ControlVolume use
                reaction_object = Reaction(dict(zip(reaction_materials, sp.sympify(coefficients))), '',
                                           sp.sympify(self.reactionWidget.item(reaction, 2).text()))
                self.list_of_reactions.append(reaction_object)

                # The total materials in the system is updated for the stream table column headers
                self.materials += list(set(reaction_materials) - set(self.materials))

        # The inerts are also added to the materials
        self.list_of_inerts += self.lineEdit.text().split()
        self.materials += self.list_of_inerts

        # Columns are inserted into the stream widget for each material present in the system
        for column_count in range(len(self.materials)):
            self.streamWidget.insertColumn(column_count)

        # Each material (plus 'Total') is added as a header to all the new columns
        self.streamWidget.setHorizontalHeaderLabels(['Total'] + self.materials)

    # This adds a new row, which represents a stream, if the bottom row is clicked
    # The first time this runs, the stream_page_updater() method will be called
    def new_stream(self):

        # This only runs the first time a new row is added to the table
        if self.stream_counter == 0:
            self.reaction_list_generator()

        # If the cell clicked is at the bottom of the table widget then it will add a new row second from the bottom
        if self.streamWidget.currentRow() == self.stream_counter:
            self.streamWidget.insertRow(self.stream_counter)
            self.stream_counter += 1

    # This adds a new row, which represents a new equation from additional information, if the bottom row is clicked
    def new_info(self):

        # If the cell clicked is at the bottom of the table widget then it will add a new row second from the bottom
        if self.infoWidget.currentRow() == self.info_counter:
            self.infoWidget.insertRow(self.info_counter)
            self.info_counter += 1

    # This uses the inputs from the stream table to generate a list that the code can maneuver through
    def stream_list_generator(self):

        # Every row in the stream table corresponds to a given Stream object
        for stream in range(self.stream_counter):

            # The Stream object is used to store each stream, starting with an empty Stream object
            stream_object = Stream()

            # Every column header is read for the given stream, these provide the keys for the stream object
            # Every value in the cell corresponding to the given stream (row) and material (column) is stored in the
            # Stream object in the proper key space
            for column in range(self.streamWidget.columnCount() - 1):

                # The first column is always the total column
                if column == 0:

                    # The total attribute for the stream is set to the total value from the table widget
                    stream_object.total = sp.sympify(self.streamWidget.item(stream, column).text())

                # Every material fraction is then added to the stream composition dictionary {material:fraction} format
                else:
                    stream_object.composition[self.streamWidget.horizontalHeaderItem(column).text()] = sp.sympify(
                        self.streamWidget.item(stream, column).text())

            # The finished Stream() object is then appended to the total list_of_streams for the system
            self.list_of_streams.append(stream_object)

    # This uses the inputs from the info table to generate a list that the code can maneuver through
    def info_list_generator(self):

        # The text within an info cell is converted to a sympy expression and stored in the list_of_info
        for info in range(self.info_counter):
            self.list_of_info.append(sp.sympify(self.infoWidget.item(info, 0).text()))

    # This adds a new row, which represents a ControlVolume, if the bottom row is clicked
    # The first time this runs, both the stream_list_generator() and the info_list_generator() methods are called
    def new_volume(self):

        # This only runs the first time a new row is added to the table
        if self.volume_counter == 0:
            self.stream_list_generator()
            self.info_list_generator()

        # If the cell clicked is at the bottom of the table widget then it will add a new row second from the bottom
        if self.volumeWidget.currentRow() == self.volume_counter:
            self.volumeWidget.insertRow(self.volume_counter)
            self.volume_counter += 1

    # This method occurs when the solve button is pressed, it will solve the system for all unknowns (if it can) and
    # print the resulting dictionary with unknown:solution format
    # To do this it must read the values from the volume table and build up each ControlVolume from the pile of pieces
    def solve_system(self):
        print('Solving the system')

        # Every row in the volume table will be read
        for volume in range(self.volume_counter):

            # If the reaction cell for a volume is None, then that means the user didn't click on it to make it an
            # empty string. This if statement had to be put in place for when this occurs
            if self.volumeWidget.item(volume, 0) is None:
                reactions_in = []

            # If there is information in the reaction cell for the given volume, then they will be stored for later use
            else:
                reactions_in = self.volumeWidget.item(volume, 0).text().split()

            # This is to ensure no issues occur if the streams_in slot is untouched
            if self.volumeWidget.item(volume, 1) is None:
                streams_in = []

            # If there is information in the streams_in cell for the volume, then they will be stored for later use
            else:
                streams_in = self.volumeWidget.item(volume, 1).text().split()

            # This is to ensure no issues occur if the streams_out slot is untouched
            if self.volumeWidget.item(volume, 2) is None:
                streams_out = []

            # If there is information in the streams_out cell for the volume, then they will be stored for later use
            else:
                streams_out = self.volumeWidget.item(volume, 2).text().split()

            # The following lists are used to actually build the ControlVolume from the previous input lists
            reactions = []
            streams = []

            # Each reaction reads from the list_of_reactions and appends the appropriate reactions to the ControlVolume
            for reaction in reactions_in:
                reactions.append(self.list_of_reactions[int(reaction) - 1])

            # Each reaction reads from the list_of_streams and appends the appropriate streams to the ControlVolume
            for stream in streams_in:
                streams.append(self.list_of_streams[int(stream) - 1])

            # Each reaction reads from the list_of_streams and appends the appropriate streams to the ControlVolume
            # These streams must have a negative 'Total' value, as the flow out of the ControlVolume
            for stream in streams_out:
                streams.append(-self.list_of_streams[int(stream) - 1])

            # A ControlVolume object is created using the unique lists of reactions and streams, and the total info
            control_volume = ControlVolume(reactions, streams, self.list_of_info)

            # The built ControlVolume object is added to the list_of_volumes
            self.list_of_volumes.append(control_volume)

        # The solve() function is called to return a dictionary of solutions which is printed
        # This will likely be added to the UI somehow so the user never has to leave the window
        print(solve(self.list_of_volumes))

# If this is the main script that is running, then the window will show and begin to function
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = MassBalanceUI()
    form.show()
    app.exec_()
