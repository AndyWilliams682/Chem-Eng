# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):

    """This code was generated using QtDesigner. The designer was used to generate a layout that I felt was readable
    and functional. This class adds no actually functionality to any of the tables or buttons. It provides the vertical
    and horizontal layouts that must be used to keep things from becoming a giant mess in the UI window."""

    # This class looks extremely messy even after I tried organizing things and adding appropriate whitespace
    # The QtDesigner does not generate code that is entirely readable, but it is much easier than writing it all by hand
    def setupUi(self, MainWindow):

        # Names and sizes the window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 637)

        # Sets the central widget for the window
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        # A series of horizontal and vertical layouts used to hold other widgets in the appropriate places
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.horizontalLayout_0 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_0.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_0.setSpacing(6)
        self.horizontalLayout_0.setObjectName("horizontalLayout_0")

        self.verticalLayout_00 = QtWidgets.QVBoxLayout()
        self.verticalLayout_00.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_00.setSpacing(6)
        self.verticalLayout_00.setObjectName("verticalLayout_00")

        # This widget is shown on the upper left, it handles the list that allows the user to cycle through tables
        self.listWidget = QtWidgets.QListWidget(self.centralWidget)
        self.listWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.listWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.insertItem(0, item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.insertItem(1, item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.insertItem(2, item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.insertItem(3, item)
        self.verticalLayout_00.addWidget(self.listWidget)

        # This table corresponds to the unknowns table, which is not finished and has no functionality yet
        self.tableWidget = QtWidgets.QTableWidget(self.centralWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.verticalLayout_00.addWidget(self.tableWidget)

        # The solve button sits at the bottom left and is used to solve the system
        self.solveButton = QtWidgets.QPushButton(self.centralWidget)
        self.solveButton.setObjectName("solveButton")
        self.verticalLayout_00.addWidget(self.solveButton)

        # More layout formatting
        self.horizontalLayout_0.addLayout(self.verticalLayout_00)
        self.verticalLayout_01 = QtWidgets.QVBoxLayout()
        self.verticalLayout_01.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_01.setSpacing(6)
        self.verticalLayout_01.setObjectName("verticalLayout_01")

        # The stacked widget holds each table widget and allows the UI to cycle between them with the list widget
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralWidget)
        self.stackedWidget.setObjectName("stackedWidget")

        # The reactions page is the first page in the stacked widget
        self.reactionPage = QtWidgets.QWidget()
        self.reactionPage.setObjectName("reactionPage")

        # Layouts for the reaction page
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.reactionPage)
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        # A label to describe how the reactions table works
        self.label_2 = QtWidgets.QLabel(self.reactionPage)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)

        # More reactions page layout formatting
        self.horizontalLayout_01r = QtWidgets.QHBoxLayout()
        self.horizontalLayout_01r.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_01r.setSpacing(6)
        self.horizontalLayout_01r.setObjectName("horizontalLayout_01r")

        # The reaction widget is the reactions table that the user inputs values into
        self.reactionWidget = QtWidgets.QTableWidget(self.reactionPage)
        self.reactionWidget.setObjectName("reactantWidget")
        self.reactionWidget.setColumnCount(3)
        self.reactionWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.reactionWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.reactionWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.reactionWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.reactionWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.reactionWidget.setItem(0, 0, item)
        self.horizontalLayout_01r.addWidget(self.reactionWidget)

        self.verticalLayout_4.addLayout(self.horizontalLayout_01r)

        # A spacer is used to separate the reaction table from the inerts text editor
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem)

        # This label provides instructions on how to input the inert materials
        self.label_3 = QtWidgets.QLabel(self.reactionPage)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)

        # The lineEdit is for the inert materials in the system
        self.lineEdit = QtWidgets.QLineEdit(self.reactionPage)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_4.addWidget(self.lineEdit)

        # Adds the reaction page to the stacked widget
        self.stackedWidget.addWidget(self.reactionPage)

        # The stream page is the second page in the stacked widget
        self.streamsPage = QtWidgets.QWidget()
        self.streamsPage.setObjectName("streamsPage")

        # Layouts for the stream page
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.streamsPage)
        self.verticalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        # A label to describe how the streams table works
        self.label_4 = QtWidgets.QLabel(self.streamsPage)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4)

        # The stream widget is the streams table that the user inputs values into
        self.streamWidget = QtWidgets.QTableWidget(self.streamsPage)
        self.streamWidget.setObjectName("streamWidget")
        self.streamWidget.setColumnCount(2)
        self.streamWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.streamWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.streamWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.streamWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.streamWidget.setItem(0, 1, item)
        self.verticalLayout_5.addWidget(self.streamWidget)

        # Adds the stream page to the stacked widget
        self.stackedWidget.addWidget(self.streamsPage)

        # The info page is the third page in the stacked widget
        self.infoPage = QtWidgets.QWidget()
        self.infoPage.setObjectName("infoPage")

        # Layouts for the info page
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.infoPage)
        self.verticalLayout_7.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")

        # A label to describe how the info table works
        self.label_5 = QtWidgets.QLabel(self.infoPage)
        self.label_5.setObjectName("label_10")
        self.verticalLayout_7.addWidget(self.label_5)

        # The info widget is the streams table that the user inputs values into
        self.infoWidget = QtWidgets.QTableWidget(self.infoPage)
        self.infoWidget.setObjectName("infoWidget")
        self.infoWidget.setColumnCount(1)
        self.infoWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.infoWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.infoWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.infoWidget.setItem(0, 1, item)
        self.verticalLayout_7.addWidget(self.infoWidget)

        # Adds the info page to the stacked widget
        self.stackedWidget.addWidget(self.infoPage)

        # The volume page is the last page in the stacked widget
        self.volumesPage = QtWidgets.QWidget()
        self.volumesPage.setObjectName("volumesPage")

        # Layouts for the info page
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.volumesPage)
        self.verticalLayout_6.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        # A label to describe how the volume table works
        self.label_1 = QtWidgets.QLabel(self.volumesPage)
        self.label_1.setObjectName("label")
        self.verticalLayout_6.addWidget(self.label_1)

        # The volume widget is the volume table that the user inputs values into
        self.volumeWidget = QtWidgets.QTableWidget(self.volumesPage)
        self.volumeWidget.setObjectName("volumeWidget")
        self.volumeWidget.setColumnCount(3)
        self.volumeWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.volumeWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.volumeWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.volumeWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.volumeWidget.setHorizontalHeaderItem(2, item)
        self.verticalLayout_6.addWidget(self.volumeWidget)

        # Adds the volume page to the stacked widget
        self.stackedWidget.addWidget(self.volumesPage)

        # More layout workings
        self.verticalLayout_01.addWidget(self.stackedWidget)
        self.horizontalLayout_0.addLayout(self.verticalLayout_01)
        self.horizontalLayout_0.setStretch(0, 1)
        self.horizontalLayout_0.setStretch(1, 1)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_0)
        MainWindow.setCentralWidget(self.centralWidget)

        # The menu bar sits at the top of the window, it will hold some functionality to make things more convenient
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 951, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)

        # The tool bar appears when the mouse is held over something (like file save)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)

        # The status bar sits at the bottom and provides information when the mouse is over something (like file save)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        # retranslateUi adds strings and other static things to the UI
        self.retranslateUi(MainWindow)

        # The stacked widget is tied to the list widgets slots
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # This adds finishing touches to the UI, like strings to all of the labels, tables, and buttons
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "Reactions and Inerts"))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "Streams"))
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", "Info Equations"))
        item = self.listWidget.item(3)
        item.setText(_translate("MainWindow", "Control Volumes"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Unknowns..."))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Values"))
        self.solveButton.setText(_translate("MainWindow", "Solve"))

        self.label_2.setText(_translate("MainWindow", "Each row is a different reaction, input species as space "
                                                      "separated formulas (ex: C2H6 C2H4 H2)\n"
                                        "Coefficients must be in the same order as the species they are tied to: "
                                        "+ for product, - for reactants\n"
                                        "Extent is for the extent of the reaction"))
        item = self.reactionWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Reaction..."))
        item = self.reactionWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Species"))
        item = self.reactionWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Coefficients"))
        item = self.reactionWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Extent"))
        __sortingEnabled = self.reactionWidget.isSortingEnabled()
        self.reactionWidget.setSortingEnabled(False)
        self.reactionWidget.setSortingEnabled(__sortingEnabled)
        self.label_3.setText(_translate("MainWindow", "Inerts must be input similarly to the species formulas above "
                                                      "(ex: N2 Ar)"))

        self.label_4.setText(_translate("MainWindow", "Each row represents a different stream\n"
                                        "Input the variables or values for each material mole fraction (or the mole "
                                        "total in the stream)"))
        item = self.streamWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Stream..."))
        item = self.streamWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Total Moles"))
        item = self.streamWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Material..."))
        __sortingEnabled = self.streamWidget.isSortingEnabled()
        self.streamWidget.setSortingEnabled(False)
        self.streamWidget.setSortingEnabled(__sortingEnabled)

        self.label_5.setText(_translate("MainWindow", "Each row represents a different relationship in the form of "
                                                      "an equation\n"
                                                      "Enter the left side of the equations, assumed to equal zero, "
                                                      "in the Equation column"""))
        item = self.infoWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Info..."))
        item = self.infoWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Equation"))
        __sortingEnabled = self.infoWidget.isSortingEnabled()
        self.streamWidget.setSortingEnabled(False)
        self.streamWidget.setSortingEnabled(__sortingEnabled)

        self.label_1.setText(_translate("MainWindow", "Each row represents a different control volume\n"
                                      "Enter reaction or stream integers with space separation (ex: 1 3)"))
        item = self.volumeWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Control Volume..."))
        item = self.volumeWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Reactions Present"))
        item = self.volumeWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Streams In"))
        item = self.volumeWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Streams Out"))

