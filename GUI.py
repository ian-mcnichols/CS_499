import sys
import numpy as np
import PyQt5.QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QGroupBox, QVBoxLayout, QCheckBox, \
    QRadioButton, QPushButton, QHBoxLayout

import Data
import Analyzer

class StatsOperator(QWidget):
    def __init__(self):
        self.app = QApplication([])
        super(StatsOperator, self).__init__()
        self.w = QWidget()                               # Base widget
        self.w.resize(500, 600)                          # Window default size
        self.w.setWindowTitle("Statistical Analyzer")    # Window title
        self.app.setStyle("Fusion")                      # Style of app (choices are: Fusion, Windows, WindowsVista, Macintosh)
        self.initUI()
        self.operations = []
        self.display = False
        self.save = False
        self.range_rows = None
        self.range_cols = None
        self.pretest = None
        self.posttest = None
        self.ordinals = None
        self.filename = None
        self.datatype = None

    def initUI(self):
        # All the formatting and button/widget declarations go here
        # File name option:
        self.fileName_lbl = QLabel(self.w)
        self.fileName_lbl.setText("File name: ")
        self.fileName_lbl.show()

        self.fileName_txtbx = QLineEdit(self.w)
        self.fileName_txtbx.setPlaceholderText("Enter file name")
        self.fileName_txtbx.show()
        self.fileName_lbl.setBuddy(self.fileName_lbl)

        self.fileName_layout = QHBoxLayout()
        self.fileName_layout.addWidget(self.fileName_lbl)
        self.fileName_layout.addWidget(self.fileName_txtbx)

        self.submit_bttn = QPushButton("Submit")
        self.fileName_layout.addWidget(self.submit_bttn)
        self.submit_bttn.clicked.connect(self.load_file)

        # Operation options:
        self.operations_group = QGroupBox("Operations:")
        self.vertLay = QVBoxLayout()
        self.operations_group.setLayout(self.vertLay)

        self.mean_chckbx = QCheckBox("Mean")
        self.vertLay.addWidget(self.mean_chckbx)
        self.median_chckbx = QCheckBox("Median")
        self.vertLay.addWidget(self.median_chckbx)
        self.mode_chckbx = QCheckBox("Mode")
        self.vertLay.addWidget(self.mode_chckbx)
        self.stand_dev_chckbx = QCheckBox("Standard deviation")
        self.vertLay.addWidget(self.stand_dev_chckbx)
        self.variance_chckbx = QCheckBox("Variance")
        self.vertLay.addWidget(self.variance_chckbx)
        self.percentiles_chckbx = QCheckBox("Percentiles")
        self.vertLay.addWidget(self.percentiles_chckbx)
        self.least_square_chckbx = QCheckBox("Least square line")
        self.vertLay.addWidget(self.least_square_chckbx)
        self.prob_dist_chckbx = QCheckBox("Probability distribution")
        self.vertLay.addWidget(self.prob_dist_chckbx)
        self.corr_coeff_chckbx = QCheckBox("Correlation coefficient")
        self.vertLay.addWidget(self.corr_coeff_chckbx)
        self.spearman_chckbx = QCheckBox("Spearman rank correction coefficient")
        self.vertLay.addWidget(self.spearman_chckbx)

        # Data range option:
        self.dataRange_group = QGroupBox("Data Range:")
        self.dataRange_layout = QGridLayout()
        self.allOfFile_radiobttn = QRadioButton("All of file")
        self.allOfFile_radiobttn.setChecked(True)
        self.dataRange_layout.addWidget(self.allOfFile_radiobttn, 0, 0)
        self.partialRange_radiobttn = QRadioButton("Partial range")
        self.dataRange_layout.addWidget(self.partialRange_radiobttn, 1, 0)

        self.dataRange_group.setLayout(self.dataRange_layout)
        self.partialRange_layout = QGridLayout()
        self.rowTxtbx_lbl = QLabel()
        self.rowTxtbx_lbl.setText("Rows")
        self.partialRange_layout.addWidget(self.rowTxtbx_lbl, 1, 1)
        self.minRow_txtbx = QLineEdit()
        self.minRow_txtbx.setPlaceholderText("Min row number")
        self.partialRange_layout.addWidget(self.minRow_txtbx, 2, 1)
        self.maxRow_txtbx = QLineEdit()
        self.maxRow_txtbx.setPlaceholderText("Max row number")
        self.partialRange_layout.addWidget(self.maxRow_txtbx, 2, 3)

        self.columnTxtbx_lbl = QLabel()
        self.columnTxtbx_lbl.setText("Columns")
        self.partialRange_layout.addWidget(self.columnTxtbx_lbl, 3, 1)
        self.minColumn_txtbx = QLineEdit()
        self.minColumn_txtbx.setPlaceholderText("Min column number")
        self.partialRange_layout.addWidget(self.minColumn_txtbx, 4, 1)
        self.maxColumn_txtbx = QLineEdit()
        self.maxColumn_txtbx.setPlaceholderText("Max column number")
        self.partialRange_layout.addWidget(self.maxColumn_txtbx, 4, 3)
        self.dataRange_layout.addLayout(self.partialRange_layout, 1, 1)

        # Range options disabled if using all of file
        self.allOfFile_radiobttn.toggled.connect(lambda:self.columnTxtbx_lbl.setDisabled(True))
        self.allOfFile_radiobttn.toggled.connect(lambda:self.rowTxtbx_lbl.setDisabled(True))
        self.allOfFile_radiobttn.toggled.connect(lambda:self.maxRow_txtbx.setDisabled(True))
        self.allOfFile_radiobttn.toggled.connect(lambda:self.minRow_txtbx.setDisabled(True))
        self.allOfFile_radiobttn.toggled.connect(lambda:self.maxColumn_txtbx.setDisabled(True))
        self.allOfFile_radiobttn.toggled.connect(lambda:self.minColumn_txtbx.setDisabled(True))

        self.partialRange_radiobttn.toggled.connect(lambda:self.columnTxtbx_lbl.setDisabled(False))
        self.partialRange_radiobttn.toggled.connect(lambda:self.rowTxtbx_lbl.setDisabled(False))
        self.partialRange_radiobttn.toggled.connect(lambda:self.maxRow_txtbx.setDisabled(False))
        self.partialRange_radiobttn.toggled.connect(lambda:self.minRow_txtbx.setDisabled(False))
        self.partialRange_radiobttn.toggled.connect(lambda:self.maxColumn_txtbx.setDisabled(False))
        self.partialRange_radiobttn.toggled.connect(lambda:self.minColumn_txtbx.setDisabled(False))

        # Data type option:
        # TODO: Make this show up
        self.dataType_group = QGroupBox("Data Type: ")
        self.dataType_layout = QVBoxLayout()
        self.dataType_group.setLayout(self.dataType_layout)

        self.ordinal_radiobttn = QRadioButton("Ordinal data")
        self.ordinal_radiobttn.setChecked(True)
        #self.range_chckbx.setDisabled(True)  # since ordinal is checked by default, disable range option by default
        self.dataType_layout.addWidget(self.ordinal_radiobttn)
        self.interval_radiobttn = QRadioButton("Interval data")
        self.dataType_layout.addWidget(self.interval_radiobttn)

        # Output option:
        self.output_group = QGroupBox("Output:")
        self.output_layout = QVBoxLayout()
        self.output_group.setLayout(self.output_layout)
        # Display results
        self.displayResults_chckbx = QCheckBox("Display results")
        self.output_layout.addWidget(self.displayResults_chckbx)
        self.displayResults_chckbx.toggled.connect(self.toggle_display)
        # Save results to file
        self.saveResults_chckbx = QCheckBox("Save results to computer")
        self.output_layout.addWidget(self.saveResults_chckbx)
        self.saveResults_chckbx.toggled.connect(self.toggle_save)

        # Calculate results button:
        self.calcResults_bttn = QPushButton("Calculate Results")
        self.calcResults_bttn.clicked.connect(self.run_calculations)

        # Main app layout:
        self.appLayout = QGridLayout(self.w)
        self.appLayout.addLayout(self.fileName_layout, 0, 0, 1, 0)
        self.appLayout.addWidget(self.operations_group, 1, 1, 2, 1)
        self.appLayout.addWidget(self.dataRange_group, 1, 0)
        self.appLayout.addWidget(self.output_group, 2, 0)
        self.appLayout.addWidget(self.calcResults_bttn, 3, 0, 3, 2)

        # have the operations checkboxes update automatically
        for checkbox in [
            self.mean_chckbx,
            self.median_chckbx,
            self.mode_chckbx,
            self.stand_dev_chckbx,
            self.variance_chckbx,
            self.percentiles_chckbx,
            self.least_square_chckbx,
            self.prob_dist_chckbx,
            self.corr_coeff_chckbx,
            self.spearman_chckbx
        ]:
            checkbox.stateChanged.connect(self.update_operations)

    def start_GUI(self):
        self.w.show()
        sys.exit(self.app.exec_())       # Run the app until the user closes

    # Specific functions that correspond to GUI widgets go under here
    def load_file(self):
        filename = self.fileName_txtbx.text()
        print("loading file {}!".format(filename))
        my_data = Data.Data(filename, "Interval")
        self.datatype = my_data.data_type
        if self.datatype == 'Interval':
            self.pretest = my_data.data_np["Pretest"]
            self.posttest = my_data.data_np["Posttest"]
            print("My data:", self.pretest, self.posttest)
        else:
            print("no ordinals yet")

    def run_calculations(self):
        print("running calculations!")
        for calculation in self.operations:
            print("running {}".format(calculation))
            if self.datatype == "Interval":
                results = Analyzer.run_function(calculation, self.pretest,
                                                self.posttest)
                print("Results:", results)
            else:
                Analyzer.run_function(calculation, self.ordinals)
        return

    def toggle_display(self):
        self.display = not self.display
        print("display is set to: ", self.display)

    def toggle_save(self):
        self.save = not self.save
        print("save output is set to: ", self.save)

    def update_operations(self):
        """continually check and review the operations boxes to update the
        list of operations that will be called"""
        checkboxes = (
            self.mean_chckbx,
            self.median_chckbx,
            self.mode_chckbx,
            self.stand_dev_chckbx,
            self.variance_chckbx,
            self.percentiles_chckbx,
            self.prob_dist_chckbx,
            self.least_square_chckbx,
            self.corr_coeff_chckbx,
            self.spearman_chckbx
        )
        for checkbox in checkboxes:
            if checkbox.isChecked() and checkbox.text() not in self.operations:
                self.operations.append(checkbox.text())
                print("operations: ", self.operations)
            elif not checkbox.isChecked() and checkbox.text() in self.operations:
                self.operations.remove(checkbox.text())
                print("operations: ", self.operations)


if __name__ == "__main__":
    myGUI = StatsOperator()
    myGUI.start_GUI()
