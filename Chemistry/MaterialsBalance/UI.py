# This file contains all of the UI code for the multi_unit_solver.
# This isn't finished yet, and probably won't be for a while.
# I got sick of doing UI code by hand but Qt Designer won't convert
# .ui files to python code for me, so once I get that figured out
# I'll continue work on this

import sys, random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import (QFont, QIcon, QColor, QPixmap, QDrag, QPainter, QPen, QBrush, QPolygon)
import PyQt5.QtCore as QtC


# This signal is created to later be activated by a mouse click
class clicked_signal(QtC.QObject):
    # the variable clicked is set to a pyqtSignal, which can be emitted later
    clicked = QtC.pyqtSignal()


# Here lies the main window of the UI, all action will exist in this window
class Solver(QMainWindow):
    unit_list = []
    path_list = []

    # initializing itself based on it's parent object, QMainWindow
    def __init__(self):
        super().__init__()

        # Adding the UI into the process
        self.init_UI()

    # The UI is defined here
    def init_UI(self):
        # This statement allows the main window to accept drag and drops of widgets
        self.setAcceptDrops(True)

        test = QPushButton('test')
        self.init_layout = QHBoxLayout(self)
        self.init_layout.addWidget(test)

        self.layout_widget = layouts()
        self.setCentralWidget(self.layout_widget)

        # self.diagram = Diagram()
        # self.setCentralWidget(self.diagram)

        # Here the status bar is defined
        self.status_bar = self.statusBar()

        # The menu bar is defined
        menu_bar = self.menuBar()

        # The exit action is defined, it is assigned a shortcut, Ctrl+Q, and text appears on the status bar
        exit_action = QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.quit)
        # save_as_action
        # open_action

        # A File tab is added to the menu bar, it contains the exit_action
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(exit_action)

        # The insert unit action is defined, assigned a shortcut, and text appears on the status bar
        insert_unit = QAction('&Insert Unit', self)
        insert_unit.setShortcut('Ctrl+U')
        insert_unit.setStatusTip('Insert a new unit')
        insert_unit.triggered.connect(self.layout_widget.diagram.add_unit)

        insert_path = QAction('&Insert Path', self)
        insert_path.setShortcut('Ctrl+I')
        insert_path.setStatusTip('Insert a new path')
        insert_path.triggered.connect(self.layout_widget.diagram.add_path)

        # An insert tab is added to the menu bar, it contains the insert_unit action
        insert_menu = menu_bar.addMenu('Insert')
        insert_menu.addAction(insert_unit)
        insert_menu.addAction(insert_path)
        # insert_menu.addAction(insert_control_volume)

        # The window is resized and centered on the screen
        self.resize(1125, 750)
        self.center()

        # The window is given a title and shown to the user
        self.setWindowTitle('Materials Balance')
        self.show()

    # If something (a widget) is dragged into the main window, it will accept it
    def dragEnterEvent(self, e):
        e.accept()

    # When something is accepted, the widget will be moved and set to the new position of the cursor
    def dropEvent(self, e):
        position = e.pos()
        Diagram.move_widget.move(position)

        e.setDropAction(QtC.Qt.MoveAction)
        e.accept()

    # This centers the window relative to the monitor, it is called earlier
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


class layouts(QWidget):
    def __init__(self):
        super().__init__()

        self.diagram = Diagram()
        test = QPushButton('test')
        hbox = QHBoxLayout()
        hbox.addWidget(test)
        hbox.addWidget(self.diagram)
        hbox.setStretch(0, 2)
        hbox.setStretch(1, 8)
        self.setLayout(hbox)


class Diagram(QWidget):
    unit_list = []
    path_list = []

    def __init__(self):
        super().__init__()

    # If something (a widget) is dragged into the main window, it will accept it
    def dragEnterEvent(self, e):
        e.accept()

    # When something is accepted, the widget will be moved and set to the new position of the cursor
    def dropEvent(self, e):
        position = e.pos()
        Diagram.move_widget.move(position)

        e.setDropAction(QtC.Qt.MoveAction)
        e.accept()

    # This adds a new unit widget to the main window
    def add_unit(self):
        self.unit_widget = Unit(self)
        Diagram.unit_list.append(self.unit_widget)

        # The unit is moved slightly away from the corner and then displayed on the main window
        self.unit_widget.move(50, 50)
        self.unit_widget.show()

    def add_path(self):
        self.path_widget = Path(self)
        Diagram.path_list.append(self.path_widget)
        self.path_widget.move(500, 400)
        self.path_widget.show()


# A unit widget is where a process occurs (a reactor, evaporator, separator, etc)
# Make Unit accommodate for new text that may be longer/shorter
class Unit(QWidget):
    # Static variable identity is defined to keep track of each unit created
    identity = 0

    def __init__(self, parent):
        super().__init__(parent)

        # The current unit is given an identity, starting at 0, and then the identity is increased for the next unit
        self.identity = Unit.identity
        Unit.identity += 1

        # The unit is given a frame to add borders, it is given the same size as the unit
        self.unit_frame = QFrame(self)
        self.unit_frame.setStyleSheet("QWidget { border: 2px solid black }")
        self.unit_frame.resize(120, 80)

        # The unit is given a label of text, which is aligned to the center of the box
        self.unit_label = QLabel(self)
        self.unit_label.setText('Unit')
        self.unit_label.setAlignment(QtC.Qt.AlignCenter)
        self.unit_label.resize(120, 80)

        # If the unit is clicked, it will connect to the method down below
        self.unit_clicked_signal = clicked_signal()
        self.unit_clicked_signal.clicked.connect(self.buttonClicked)

        # The unit itself is resized
        self.resize(120, 80)

    # This allows for the unit to be dragged around the main window
    def mouseMoveEvent(self, e):
        # It will only trigger if the left button is clicked onto the widget itself
        if e.buttons() != QtC.Qt.LeftButton:
            return

        unit_id = self.identity
        Diagram.move_widget = Diagram.unit_list[unit_id]

        # Data will be gathered from the cursor to appropriately move the unit
        unit_mime_data = QtC.QMimeData()

        # The unit will be dragged to the appropriate position based on the data
        drag = QDrag(self)
        drag.setMimeData(unit_mime_data)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(QtC.Qt.MoveAction)

    # If the unit is clicked on with the right button, the clicked signal will emit
    def mousePressEvent(self, e):
        if e.buttons() == QtC.Qt.RightButton:
            self.unit_clicked_signal.clicked.emit()

    # When the clicked signal is emitted, this method will begin
    def buttonClicked(self):
        # An input dialog window will be shown
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Rename the unit:')

        # If the user accepts the changes (clicks ok instead of cancel)
        if ok:
            # Then whatever text is typed into the input dialog window will replace the unit label text
            self.unit_label.setText(text)


# Needs to be label-able
# Rotatable
# Editable
class Path(QWidget):
    identity = 0

    def __init__(self, parent):
        super().__init__(parent)

        self.identity = Path.identity
        Path.identity += 1

        self.setMinimumSize(120, 80)

        self.path_clicked_signal = clicked_signal()
        self.path_clicked_signal.clicked.connect(self.buttonClicked)

        self.path_label = QLabel(self)
        self.path_label.setText(str(self.identity))
        self.path_label.move(60, 50)

        self.shape = QPolygon([QtC.QPoint(150, 50), QtC.QPoint(120, 55), QtC.QPoint(120, 45)])

    def mouseMoveEvent(self, e):
        # It will only trigger if the left button is clicked onto the widget itself
        if e.buttons() != QtC.Qt.LeftButton:
            return

        path_id = self.identity
        Diagram.move_widget = Diagram.path_list[path_id]

        # Data will be gathered from the cursor to appropriately move the unit
        unit_mime_data = QtC.QMimeData()

        # The unit will be dragged to the appropriate position based on the data
        drag = QDrag(self)
        drag.setMimeData(unit_mime_data)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(QtC.Qt.MoveAction)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        self.drawShape(qp)
        qp.end()

    def drawLines(self, qp):
        pen = QPen(QtC.Qt.black, 2, QtC.Qt.SolidLine)

        qp.setPen(pen)
        qp.drawLine(10, 50, 150, 50)

    def drawShape(self, qp):
        brush = QBrush(QtC.Qt.black)
        qp.setBrush(QBrush(QtC.Qt.black))
        qp.drawPolygon(self.shape)

    def mousePressEvent(self, e):
        if e.buttons() == QtC.Qt.RightButton:
            self.path_clicked_signal.clicked.emit()

    # When the clicked signal is emitted, this method will begin
    def buttonClicked(self):
        print('yay')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Solver()
    sys.exit(app.exec_())
