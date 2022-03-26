import sys
import numpy as np
import PyQt5.QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QGroupBox, QVBoxLayout, QCheckBox, \
    QRadioButton, QPushButton, QHBoxLayout

import Data
import Analyzer
import visualize


class StatsOperator(QWidget):
    def __init__(self):
        self.app = QApplication([])
        super(StatsOperator, self).__init__()
        self.w = QWidget()  # Base widget
        self.w.resize(500, 800)  # Window default size
        self.w.setWindowTitle("Statistical Analyzer")  # Window title
        self.app.setStyle("Fusion")  # Style of app (choices are: Fusion, Windows, WindowsVista, Macintosh)
        self.initUI()
        self.operations = []
        self.results = {}
        self.display = True
        self.save = False
        self.range_rows = None
        self.range_cols = None
        self.pretest = None
        self.posttest = None
        self.ordinals = None
        self.filename = None
        self.datatype = "Interval"
        self.data_loaded = False
        self.resultsWindow = ResultsDisplay()
        self.dataEntryWindow = DataInputWindow()

    def initUI(self):
        # All the formatting and button/widget declarations go here
        self.file_entry()
        self.operation_options()
        self.data_range_options()
        self.data_type_options()
        self.output_options()
        self.calc_button_init()
        self.main_app_layout()

        # Range options disabled if using all of file
        self.allOfFile_radiobttn.toggled.connect(lambda: self.columnTxtbx_lbl.setDisabled(True))
        self.allOfFile_radiobttn.toggled.connect(lambda: self.rowTxtbx_lbl.setDisabled(True))
        self.allOfFile_radiobttn.toggled.connect(lambda: self.maxRow_txtbx.setDisabled(True))
        self.allOfFile_radiobttn.toggled.connect(lambda: self.minRow_txtbx.setDisabled(True))
        self.allOfFile_radiobttn.toggled.connect(lambda: self.maxColumn_txtbx.setDisabled(True))
        self.allOfFile_radiobttn.toggled.connect(lambda: self.minColumn_txtbx.setDisabled(True))
        # Range options enabled otherwise
        self.partialRange_radiobttn.toggled.connect(lambda: self.columnTxtbx_lbl.setDisabled(False))
        self.partialRange_radiobttn.toggled.connect(lambda: self.rowTxtbx_lbl.setDisabled(False))
        self.partialRange_radiobttn.toggled.connect(lambda: self.maxRow_txtbx.setDisabled(False))
        self.partialRange_radiobttn.toggled.connect(lambda: self.minRow_txtbx.setDisabled(False))
        self.partialRange_radiobttn.toggled.connect(lambda: self.maxColumn_txtbx.setDisabled(False))
        self.partialRange_radiobttn.toggled.connect(lambda: self.minColumn_txtbx.setDisabled(False))

        # Operations on for Interval data
        self.interval_radiobttn.toggled.connect(lambda: self.stand_dev_chckbx.setDisabled(False))
        self.interval_radiobttn.toggled.connect(lambda: self.variance_chckbx.setDisabled(False))
        self.interval_radiobttn.toggled.connect(lambda: self.percentiles_chckbx.setDisabled(False))
        self.interval_radiobttn.toggled.connect(lambda: self.least_square_chckbx.setDisabled(False))
        self.interval_radiobttn.toggled.connect(lambda: self.corr_coeff_chckbx.setDisabled(False))
        self.interval_radiobttn.toggled.connect(lambda: self.spearman_chckbx.setDisabled(False))
        self.interval_radiobttn.toggled.connect(self.set_datatype_interval)
        # These operations are off if ordinal data is selected
        self.ordinal_radiobttn.toggled.connect(lambda: self.stand_dev_chckbx.setDisabled(True))
        self.ordinal_radiobttn.toggled.connect(lambda: self.variance_chckbx.setDisabled(True))
        self.ordinal_radiobttn.toggled.connect(lambda: self.percentiles_chckbx.setDisabled(True))
        self.ordinal_radiobttn.toggled.connect(lambda: self.least_square_chckbx.setDisabled(True))
        self.ordinal_radiobttn.toggled.connect(lambda: self.corr_coeff_chckbx.setDisabled(True))
        self.ordinal_radiobttn.toggled.connect(lambda: self.spearman_chckbx.setDisabled(True))
        self.interval_radiobttn.toggled.connect(self.set_datatype_ordinal)
        self.dataType_layout.addWidget(self.ordinal_radiobttn)

        # When file upload is selected:
        self.filename_radiobttn.clicked.connect(lambda: self.numRows_lbl.setDisabled(True))
        self.filename_radiobttn.clicked.connect(lambda: self.numCol_lbl.setDisabled(True))
        self.filename_radiobttn.clicked.connect(lambda: self.col_txtbx.setDisabled(True))
        self.filename_radiobttn.clicked.connect(lambda: self.row_txtbx.setDisabled(True))
        self.filename_radiobttn.clicked.connect(lambda: self.enterData_bttn.setDisabled(True))
        self.filename_radiobttn.clicked.connect(lambda: self.fileName_lbl.setDisabled(False))
        self.filename_radiobttn.clicked.connect(lambda: self.fileName_txtbx.setDisabled(False))
        self.filename_radiobttn.clicked.connect(lambda: self.submit_bttn.setDisabled(False))
        # When manual data entry is selected:
        self.manual_entry_radiobttn.clicked.connect(lambda: self.fileName_lbl.setDisabled(True))
        self.manual_entry_radiobttn.clicked.connect(lambda: self.fileName_txtbx.setDisabled(True))
        self.manual_entry_radiobttn.clicked.connect(lambda: self.submit_bttn.setDisabled(True))
        self.manual_entry_radiobttn.clicked.connect(lambda: self.numRows_lbl.setDisabled(False))
        self.manual_entry_radiobttn.clicked.connect(lambda: self.numCol_lbl.setDisabled(False))
        self.manual_entry_radiobttn.clicked.connect(lambda: self.col_txtbx.setDisabled(False))
        self.manual_entry_radiobttn.clicked.connect(lambda: self.row_txtbx.setDisabled(False))
        self.manual_entry_radiobttn.clicked.connect(lambda: self.enterData_bttn.setDisabled(False))

        # Filename validation
        # Groups are disabled on startup
        self.operations_group.setDisabled(True)
        self.dataRange_group.setDisabled(True)
        self.output_group.setDisabled(True)
        self.calcResults_bttn.setDisabled(True)

        # Have the operations checkboxes update automatically
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

        #show manual entry window if enter data is clicked
        self.enterData_bttn.clicked.connect(self.display_manual_entry_window)

    def file_entry(self):
        # File name option:
        self.filename_radiobttn = QRadioButton("Enter a csv file")
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

        self.manual_entry_radiobttn = QRadioButton("Manually enter data")
        self.numRows_lbl = QLabel(self.w)
        self.numRows_lbl.setText("Number of rows: ")
        self.row_txtbx = QLineEdit(self.w)
        self.row_txtbx.setPlaceholderText("Enter a number 1-5")
        self.numCol_lbl = QLabel(self.w)
        self.numCol_lbl.setText("Number of columns: ")
        self.col_txtbx = QLineEdit(self.w)
        self.col_txtbx.setPlaceholderText("Enter a number 1-5")
        self.enterData_bttn = QPushButton("Enter data")
        self.dataRow_txtbx_layout = QHBoxLayout()
        self.dataRow_txtbx_layout.addWidget(self.numRows_lbl)
        self.dataRow_txtbx_layout.addWidget(self.row_txtbx)
        self.dataCol_txtbx_layout = QHBoxLayout()
        self.dataCol_txtbx_layout.addWidget(self.numCol_lbl)
        self.dataCol_txtbx_layout.addWidget(self.col_txtbx)
        self.data_entry_layout = QVBoxLayout()
        self.data_entry_layout.addLayout(self.dataRow_txtbx_layout)
        self.data_entry_layout.addLayout(self.dataCol_txtbx_layout)
        self.data_entry_layout.addWidget(self.enterData_bttn)

        self.data_entry_group = QGroupBox("Data Entry: ")
        self.entry_group_layout = QVBoxLayout()
        self.data_entry_group.setLayout(self.entry_group_layout)
        self.entry_group_layout.addWidget(self.filename_radiobttn)
        self.entry_group_layout.addLayout(self.fileName_layout)
        self.entry_group_layout.addWidget(self.manual_entry_radiobttn)
        self.entry_group_layout.addLayout(self.data_entry_layout)

        # Default options:
        self.filename_radiobttn.setChecked(True)
        self.numRows_lbl.setDisabled(True)
        self.numCol_lbl.setDisabled(True)
        self.col_txtbx.setDisabled(True)
        self.row_txtbx.setDisabled(True)
        self.enterData_bttn.setDisabled(True)

    def operation_options(self):
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

    def data_range_options(self):
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
        self.rowTxtbx_lbl.setDisabled(True)
        self.partialRange_layout.addWidget(self.rowTxtbx_lbl, 1, 1)
        self.minRow_txtbx = QLineEdit()
        self.minRow_txtbx.setPlaceholderText("Min row number")
        self.minRow_txtbx.setDisabled(True)
        self.partialRange_layout.addWidget(self.minRow_txtbx, 2, 1)
        self.maxRow_txtbx = QLineEdit()
        self.maxRow_txtbx.setDisabled(True)
        self.maxRow_txtbx.setPlaceholderText("Max row number")
        self.partialRange_layout.addWidget(self.maxRow_txtbx, 2, 3)

        self.columnTxtbx_lbl = QLabel()
        self.columnTxtbx_lbl.setText("Columns")
        self.columnTxtbx_lbl.setDisabled(True)
        self.partialRange_layout.addWidget(self.columnTxtbx_lbl, 3, 1)
        self.minColumn_txtbx = QLineEdit()
        self.minColumn_txtbx.setPlaceholderText("Min column number")
        self.minColumn_txtbx.setDisabled(True)
        self.partialRange_layout.addWidget(self.minColumn_txtbx, 4, 1)
        self.maxColumn_txtbx = QLineEdit()
        self.maxColumn_txtbx.setPlaceholderText("Max column number")
        self.maxColumn_txtbx.setDisabled(True)
        self.partialRange_layout.addWidget(self.maxColumn_txtbx, 4, 3)
        self.dataRange_layout.addLayout(self.partialRange_layout, 1, 1)

    def data_type_options(self):
        # Data type option:
        self.dataType_group = QGroupBox("Data Type: ")
        self.dataType_layout = QVBoxLayout()
        self.dataType_group.setLayout(self.dataType_layout)

        self.interval_radiobttn = QRadioButton("Interval data")
        self.dataType_layout.addWidget(self.interval_radiobttn)
        self.interval_radiobttn.setChecked(True)
        self.ordinal_radiobttn = QRadioButton("Ordinal data")

    def output_options(self):
        # Output option:
        self.output_group = QGroupBox("Output:")
        self.output_layout = QVBoxLayout()
        self.output_group.setLayout(self.output_layout)
        # Display results
        self.displayResults_chckbx = QCheckBox("Display results")
        self.displayResults_chckbx.setChecked(True)
        self.output_layout.addWidget(self.displayResults_chckbx)
        self.displayResults_chckbx.toggled.connect(self.toggle_display)
        # Save results to file
        self.saveResults_chckbx = QCheckBox("Save results to computer")
        self.output_layout.addWidget(self.saveResults_chckbx)
        self.saveResults_chckbx.toggled.connect(self.toggle_save)

    def calc_button_init(self):
        # Calculate results button:
        self.calcResults_bttn = QPushButton("Calculate Results")
        self.calcResults_bttn.clicked.connect(self.run_calculations)

    def main_app_layout(self):
        # Main app layout:
        self.appLayout = QGridLayout(self.w)
        self.appLayout.addWidget(self.data_entry_group, 0, 0, 1, 0)
        self.appLayout.addWidget(self.operations_group, 1, 1, 2, 1)
        self.appLayout.addWidget(self.dataRange_group, 2, 0)
        self.appLayout.addWidget(self.output_group, 3, 0)
        self.appLayout.addWidget(self.calcResults_bttn, 3, 0, 3, 2)
        self.appLayout.addWidget(self.dataType_group, 1, 0)

    def start_GUI(self):
        self.w.show()
        sys.exit(self.app.exec_())  # Run the app until the user closes

    # Specific functions that correspond to GUI widgets go under here
    def load_file(self):
        filename = self.fileName_txtbx.text()
        print("loading file {}!".format(filename))
        if self.datatype == 'Interval':
            my_data = Data.Data(filename, "Interval")
            self.pretest = my_data.data_np["Pretest"]
            self.posttest = my_data.data_np["Posttest"]
            print("My data:", self.pretest, self.posttest)
        else:
            my_data = Data.Data(filename, "Ordinal")
            print([my_data.data_np[x] for x in range(1, len(my_data.data_np.dtype.names))])
            print("no ordinals yet")
        self.data_loaded = True

        # Don't allow user to submit file again and enable the groups again
        self.operations_group.setDisabled(False)
        self.dataRange_group.setDisabled(False)
        self.output_group.setDisabled(False)
        self.data_entry_group.setDisabled(True)
        self.dataType_group.setDisabled(True)
        self.submit_bttn.setDisabled(True)

    def run_calculations(self):
        print("running calculations!")
        if not self.data_loaded:
            self.load_file()
        for calculation in self.operations:
            print("running {}".format(calculation))
            if self.datatype == "Interval":
                print("pretest:", self.pretest)
                print("posttest:", self.posttest)
                output = Analyzer.run_function(calculation, pretest=self.pretest,
                                               posttest=self.posttest, data_type="Interval")
                print("Results:", output)
            elif self.datatype == "Ordinal":
                output = Analyzer.run_function(calculation, ordinals=self.ordinals, data_type="Ordinal")
            else:
                raise Exception("Bad datatype {}".format(self.datatype))
            self.results[calculation] = output
        if self.save:
            visualize.build_csv("Results.csv", self.results)
            visualize.build_text("Results.txt", self.results)

        if self.display:
            self.show_results_window()

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

        if not self.operations:
            self.calcResults_bttn.setDisabled(True)
        else:
            self.calcResults_bttn.setDisabled(False)

    # datatype toggle functions
    def set_datatype_interval(self):
        self.datatype = "Interval"

    def set_datatype_ordinal(self):
        self.datatype = "Ordinal"

    def show_results_window(self):
        message = "\n\n";

        for i in range(0, len(self.operations), 1):
            message += "Results from " + self.operations[i]
            message += "\nPretest: "
            # TODO Add pre-test results
            message += "\n"
            message += "\nPost-test: "
            # TODO Add post-test results
            message += "\n\n\n\n"

        self.resultsWindow.result_lbl.setText(message)
        self.resultsWindow.start()

    def display_manual_entry_window(self):
        self.dataEntryWindow.rows = self.row_txtbx.text()
        self.dataEntryWindow.cols = self.col_txtbx.text()

        self.dataEntryWindow.start()


class ResultsDisplay(QWidget):
    def __init__(self):
        self.app = QApplication([])
        super(ResultsDisplay, self).__init__()
        self.w = QWidget()  # Base widget
        self.w.resize(500, 600)  # Window default size
        self.w.setWindowTitle("Statistical Analyzer Results")  # Window title
        self.app.setStyle("Fusion")  # Style of app (choices are: Fusion, Windows, WindowsVista, Macintosh)
        self.init_ui()

    def init_ui(self):
        self.result_lbl = QLabel(self.w)
        self.result_lbl.setText("Results:")
        self.result_layout = QVBoxLayout()
        self.oper_lbl = QLabel(self.w)
        self.pretest_lbl = QLabel(self.w)

        self.result_layout.addWidget(self.result_lbl)
        self.result_layout.addWidget(self.pretest_lbl)
        self.result_layout.addWidget(self.oper_lbl)
        #TODO Add a scroll bar so user can see all results

    def start(self):
        self.w.show()


class DataInputWindow(QWidget):
    def __init__(self):
        self.app = QApplication([])
        super(DataInputWindow, self).__init__()
        self.w = QWidget()  # Base widget
        self.w.resize(500, 300)  # Window default size
        self.w.setWindowTitle("Statistical Analyzer Manual Data Entry")  # Window title
        self.app.setStyle("Fusion")  # Style of app (choices are: Fusion, Windows, WindowsVista, Macintosh)
        self.init()
        self.rows = 0
        self.cols = 0

    def init(self):
        self.setup_elements()

    def start(self):
        self.w.show()

    def setup_elements(self):
        self.inputLayout = QGridLayout(self.w)
        self.txtbx1 = QLineEdit()
        self.txtbx2 = QLineEdit()
        self.txtbx3 = QLineEdit()
        self.txtbx4 = QLineEdit()
        self.txtbx5 = QLineEdit()
        self.txtbx6 = QLineEdit()
        self.txtbx7 = QLineEdit()
        self.txtbx8 = QLineEdit()
        self.txtbx9 = QLineEdit()
        self.txtbx10 = QLineEdit()
        self.txtbx11 = QLineEdit()
        self.txtbx12 = QLineEdit()
        self.txtbx13 = QLineEdit()
        self.txtbx14 = QLineEdit()
        self.txtbx15 = QLineEdit()
        self.txtbx16 = QLineEdit()
        self.txtbx17 = QLineEdit()
        self.txtbx18 = QLineEdit()
        self.txtbx19 = QLineEdit()
        self.txtbx20 = QLineEdit()
        self.txtbx21 = QLineEdit()
        self.txtbx22 = QLineEdit()
        self.txtbx23 = QLineEdit()
        self.txtbx24 = QLineEdit()
        self.txtbx25 = QLineEdit()

        self.textBoxes = [
            [self.txtbx1, self.txtbx2, self.txtbx3, self.txtbx4, self.txtbx5],
            [self.txtbx6, self.txtbx7, self.txtbx8, self.txtbx9, self.txtbx10],
            [self.txtbx11, self.txtbx12, self.txtbx13, self.txtbx14, self.txtbx15],
            [self.txtbx16, self.txtbx17, self.txtbx18, self.txtbx19, self.txtbx20],
            [self.txtbx21, self.txtbx22, self.txtbx23, self.txtbx24, self.txtbx25]]

        self.inputLayout.addWidget(self.txtbx1, 0, 0)
        self.inputLayout.addWidget(self.txtbx2, 0, 1)
        self.inputLayout.addWidget(self.txtbx3, 0, 2)
        self.inputLayout.addWidget(self.txtbx4, 0, 3)
        self.inputLayout.addWidget(self.txtbx5, 0, 4)
        self.inputLayout.addWidget(self.txtbx6, 1, 0)
        self.inputLayout.addWidget(self.txtbx7, 1, 1)
        self.inputLayout.addWidget(self.txtbx8, 1, 2)
        self.inputLayout.addWidget(self.txtbx9, 1, 3)
        self.inputLayout.addWidget(self.txtbx10, 1, 4)
        self.inputLayout.addWidget(self.txtbx11, 2, 0)
        self.inputLayout.addWidget(self.txtbx12, 2, 1)
        self.inputLayout.addWidget(self.txtbx13, 2, 2)
        self.inputLayout.addWidget(self.txtbx14, 2, 3)
        self.inputLayout.addWidget(self.txtbx15, 2, 4)
        self.inputLayout.addWidget(self.txtbx16, 3, 0)
        self.inputLayout.addWidget(self.txtbx17, 3, 1)
        self.inputLayout.addWidget(self.txtbx18, 3, 2)
        self.inputLayout.addWidget(self.txtbx19, 3, 3)
        self.inputLayout.addWidget(self.txtbx20, 3, 4)
        self.inputLayout.addWidget(self.txtbx21, 4, 0)
        self.inputLayout.addWidget(self.txtbx22, 4, 1)
        self.inputLayout.addWidget(self.txtbx23, 4, 2)
        self.inputLayout.addWidget(self.txtbx24, 4, 3)
        self.inputLayout.addWidget(self.txtbx25, 4, 4)

        self.submitData_bttn = QPushButton("Submit data")
        self.inputLayout.addWidget(self.submitData_bttn, 5, 1, 5, 3)


if __name__ == "__main__":
    myGUI = StatsOperator()
    myGUI.start_GUI()

