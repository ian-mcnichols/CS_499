import os
import sys
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QGroupBox, QVBoxLayout, QCheckBox, \
    QRadioButton, QPushButton, QHBoxLayout, QScrollArea, QFileDialog
import logging
import Data
import Analyzer
import visualize


class StatsOperator(QWidget):
    def __init__(self):
        self.app = QApplication([])
        super(StatsOperator, self).__init__()
        self.w = QWidget()  # Base widget
        self.w.setFixedSize(500, 850)  # Window is fixed size
        self.w.setWindowTitle("Statistical Analyzer")  # Window title
        with open('style.qss', 'r') as f:
            style = f.read()
            # Set the stylesheet of the application
            self.app.setStyleSheet(style)
        self.initUI()
        self.set_defaults()
        self.my_data = None
        self.resultsWindow = ResultsDisplay()
        self.dataEntryWindow = DataInputWindow()

        self.do_logging = True
        if self.do_logging:
            logging.basicConfig(level=logging.INFO, filename='log.log', filemode='w',
                                format='%(asctime)s  [%(filename)s:%(lineno)d] %(message)s')

    def set_defaults(self):
        """Sets default parameters"""
        self.operations = []
        self.results = {}
        self.display = True
        self.save = False
        self.range_rows = None
        self.range_cols = None
        self.my_data = None
        self.filename = None
        self.datatype = "Interval"
        self.data_loaded = False

    def initUI(self):
        """ All the formatting and button/widget declarations go here """
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
        self.interval_radiobttn.toggled.connect(lambda: self.mean_chckbx.setDisabled(False))
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

        # show manual entry window if enter data is clicked
        self.enterData_bttn.clicked.connect(self.display_manual_entry_window)

    # GUI layout and organization
    def file_entry(self):
        """File name option:"""
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
        self.submit_bttn = QPushButton("Load File")
        self.fileName_layout.addWidget(self.submit_bttn)
        self.submit_bttn.clicked.connect(self.load_file)

        self.manual_entry_radiobttn = QRadioButton("Manually enter data")
        self.numRows_lbl = QLabel(self.w)
        self.numRows_lbl.setText("Number of rows: ")
        self.row_txtbx = QLineEdit(self.w)

        self.row_txtbx.setPlaceholderText("Enter a number 1-50")
        self.numCol_lbl = QLabel(self.w)
        self.numCol_lbl.setText("Number of columns: ")
        self.col_txtbx = QLineEdit(self.w)
        self.col_txtbx.setPlaceholderText("Enter a number 1-50")

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
        """ Operation options: """
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
        """Data range option: """
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
        """Data type option:"""
        self.dataType_group = QGroupBox("Data Type: ")
        self.dataType_layout = QVBoxLayout()
        self.dataType_group.setLayout(self.dataType_layout)

        self.interval_radiobttn = QRadioButton("Interval data")
        self.dataType_layout.addWidget(self.interval_radiobttn)
        self.interval_radiobttn.setChecked(True)
        self.ordinal_radiobttn = QRadioButton("Ordinal data")

        # These operations are off if ordinal data is selected
        self.ordinal_radiobttn.toggled.connect(lambda: self.mean_chckbx.setDisabled(True))
        self.ordinal_radiobttn.toggled.connect(lambda: self.stand_dev_chckbx.setDisabled(True))
        self.ordinal_radiobttn.toggled.connect(lambda: self.variance_chckbx.setDisabled(True))
        self.ordinal_radiobttn.toggled.connect(lambda: self.percentiles_chckbx.setDisabled(True))
        self.ordinal_radiobttn.toggled.connect(lambda: self.least_square_chckbx.setDisabled(True))
        self.ordinal_radiobttn.toggled.connect(lambda: self.corr_coeff_chckbx.setDisabled(True))
        self.ordinal_radiobttn.toggled.connect(lambda: self.spearman_chckbx.setDisabled(True))
        self.interval_radiobttn.toggled.connect(self.set_datatype_ordinal)
        self.dataType_layout.addWidget(self.ordinal_radiobttn)

    def output_options(self):
        """Output option:"""
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
        """Calculate results button:"""
        self.calcResults_bttn = QPushButton("Calculate Results")
        self.calcResults_bttn.clicked.connect(self.run_calculations)
        self.reset_bttn = QPushButton("Do Another Calculation")
        self.reset_bttn.clicked.connect(self.restart)

    def main_app_layout(self):
        """Main app layout:"""
        self.appLayout = QGridLayout(self.w)
        self.appLayout.addWidget(self.data_entry_group, 1, 0, 1, 0)
        self.appLayout.addWidget(self.operations_group, 2, 1)
        self.appLayout.addWidget(self.dataRange_group, 0, 1)
        self.appLayout.addWidget(self.output_group, 2, 0)
        self.appLayout.addWidget(self.calcResults_bttn, 3, 0, 3, 2)
        self.appLayout.addWidget(self.dataType_group, 0, 0)
        self.appLayout.addWidget(self.reset_bttn, 4, 0, 4, 2)

    def start_GUI(self):
        """GUI Driver function"""
        self.w.show()
        sys.exit(self.app.exec_())  # Run the app until the user closes

    # Specific functions that correspond to GUI widgets go under here
    def load_file(self):
        """Loads in the user's inputted file and saves data to variable"""
        if self.fileName_txtbx.text() != "":
            filename = self.fileName_txtbx.text()
        else:
            filename = str(QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*.csv)")[0])
            if filename == "":
                return
        self.fileName_txtbx.setPlaceholderText(filename)
        if self.do_logging:
            logging.info("loading file {}!".format(filename))
        if not os.path.isfile(filename):
            if self.do_logging:
                logging.error("File does not exist.")
            return
        if self.datatype == 'Interval':
            my_data = Data.Data(filename, "Interval")
            self.my_data = my_data
            if self.do_logging:
                logging.info(f"My data: {np.array2string(self.my_data.data_np)}")
        else:
            my_data = Data.Data(filename, "Ordinal")
            self.my_data = my_data
            if self.do_logging:
                logging.info(f"My data: {np.array2string(self.my_data.data_np)}")
        self.data_loaded = True
        # If user has selected a range
        if self.partialRange_radiobttn.isChecked():
            min_column = int(self.minColumn_txtbx.text()) - 1
            max_column = int(self.maxColumn_txtbx.text())
            min_row = int(self.minRow_txtbx.text()) - 1
            max_row = int(self.maxRow_txtbx.text())

            # Check that all values are integers
            if all([isinstance(i, int) for i in [min_column, max_column, min_row, max_row]]):
                # Edit the data array
                new_data_np = self.my_data.data_np[min_column:max_column, min_row:max_row]
                self.my_data.data_np = new_data_np
                # Reset column/row labels
                new_column_labels = self.my_data.column_labels[min_column:max_column]
                self.my_data.column_labels = new_column_labels
                new_row_labels = self.my_data.row_labels[min_row:max_row]
                self.my_data.row_labels = new_row_labels
                if self.do_logging:
                    logging.info(f"my new data: {np.array2string(self.my_data.data_np)}")
                    logging.info(f"column labels: {self.my_data.column_labels}")
                    logging.info(f"row labels: {self.my_data.row_labels}")
            else:
                # The values entered were not correct
                if self.do_logging:
                    logging.warning("Please enter integer values for rows/columns")

        # Don't allow user to submit file again and enable the groups again
        self.operations_group.setDisabled(False)
        self.dataRange_group.setDisabled(True)
        self.output_group.setDisabled(False)
        self.data_entry_group.setDisabled(True)
        self.dataType_group.setDisabled(True)
        self.submit_bttn.setDisabled(True)

    def run_calculations(self):
        """Iterate over user's selected calculations and run them with the Analyzer.
        Save or display outputs according to user's choices.
        The bulk of our logic goes here"""
        if self.do_logging:
            logging.info("running calculations!")
        if self.save:
            os.makedirs("output/", exist_ok=True)
        if not self.data_loaded:
            if self.do_logging:
                logging.error("Cannot run without inputs loaded.")
            return
        elif self.my_data.data_np is None:
            if self.do_logging:
                logging.error("Cannot run without data numpy.")
            self.operations_group.setDisabled(True)
            return
        for calculation in self.operations:
            if self.do_logging:
                logging.info(f"running {format(calculation)}")
            if self.datatype == "Interval":
                output = Analyzer.run_function(calculation, self.my_data.data_np, data_type="Interval",
                                               display=self.display, save=self.save)
                if self.do_logging:
                    logging.info(f"Results: {output}")
            elif self.datatype == "Ordinal":
                output = Analyzer.run_function(calculation, self.my_data.data_np, data_type="Ordinal",
                                               display=self.display, save=self.save)
                if calculation == "Mode":
                    visualize.plot_chart(self.my_data, "Vertical Bar Chart", results=output,
                                         data_type='ordinal', save=self.save, display=self.display)
                if self.do_logging:
                    logging.info(f"Results: {output}")
            else:
                raise Exception("Bad datatype {}".format(self.datatype))
            self.results[calculation] = output
        if self.display or self.save:
            if self.do_logging:
                logging.info(f"operations list: {self.operations}")
            if self.datatype == "Interval":
                visualize.plot_chart(self.my_data, "box plot", data_type=self.datatype, display=self.display,
                                     save=self.save)
                visualize.plot_chart(self.my_data, "Histogram", data_type=self.datatype, display=self.display,
                                     save=self.save)
            if "Probability distribution" in self.operations:
                visualize.plot_chart(self.my_data, "Probability Distribution", display=self.display,
                                     save=self.save, data_type=self.datatype)
            if self.save:
                visualize.build_csv("Results.csv", self.results, self.my_data.column_labels, self.datatype)
                visualize.build_text("Results.txt", self.results, self.my_data.column_labels, self.datatype)
            if self.display:
                self.show_results_window()
        if self.do_logging:
            logging.info("Program Complete")
        return
        
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
                if self.do_logging:
                    logging.info(f"operations: {str(self.operations)}")
            elif not checkbox.isChecked() and checkbox.text() in self.operations:
                self.operations.remove(checkbox.text())
                if self.do_logging:
                    logging.info(f"operations: {str(self.operations)}")

        if not self.operations:
            self.calcResults_bttn.setDisabled(True)
        else:
            self.calcResults_bttn.setDisabled(False)

    # Additional window options
    def show_results_window(self):
        """Displays results from calculations to screen"""
        message = ""
        if self.datatype == "Interval":
            for function in self.results:
                message += "\n\nResults from " + function + ":\n"
                if type(self.results[function]) is list:
                    for i in range(len(self.results[function])):
                        if self.results[function][i] != self.results[function][-1]:
                            message += "\t" + self.my_data.column_labels[i] + ": "
                        else:
                            message += "\tDifference between first and last column: "
                        message += str(self.results[function][i]) + "\n"
                else:
                    message += "\t" + str(self.results[function]) + "\n"
        else:
            for function in self.results:
                message += "\n\nResults from " + function + ":\n"
                if type(self.results[function]) is list:
                    for i in range(len(self.results[function])):
                        message += "\t #" + str(i+1) + ": " + str(self.results[function][i]) + "\n"

        self.resultsWindow.result_lbl.setText(message)
        self.resultsWindow.start()

    def display_manual_entry_window(self):
        """Opens the data entry window"""
        self.my_data = Data.Data("GUI", self.datatype)
        self.dataEntryWindow.rows = self.row_txtbx.text()
        self.dataEntryWindow.cols = self.col_txtbx.text()
        if self.row_txtbx.text() == "" or self.col_txtbx.text() == "":
            if self.do_logging:
                logging.error("no rows or columns entered.")
            return
        self.dataEntryWindow.start(self.dataEntryWindow.rows,
                                   self.dataEntryWindow.cols,
                                   self.my_data)
        self.operations_group.setDisabled(False)
        self.output_group.setDisabled(False)
        self.data_loaded = True
        self.data_entry_group.setEnabled(False)
        self.dataRange_group.setEnabled(False)
        self.dataType_group.setEnabled(False)

    def restart(self):
        """Restart the app so user can make another calculation"""
        self.calcResults_bttn.setEnabled(True)
        self.operations_group.setEnabled(False)
        self.output_group.setEnabled(False)
        self.data_entry_group.setEnabled(True)
        self.dataType_group.setEnabled(True)
        self.dataRange_group.setEnabled(True)
        self.filename_radiobttn.setChecked(True)
        self.fileName_txtbx.setEnabled(True)
        self.fileName_lbl.setEnabled(True)
        self.submit_bttn.setEnabled(True)
        self.row_txtbx.setEnabled(False)
        self.col_txtbx.setEnabled(False)
        self.enterData_bttn.setEnabled(False)

        # uncheck all operations
        self.mean_chckbx.setChecked(False)
        self.median_chckbx.setChecked(False)
        self.mode_chckbx.setChecked(False)
        self.stand_dev_chckbx.setChecked(False)
        self.variance_chckbx.setChecked(False)
        self.percentiles_chckbx.setChecked(False)
        self.least_square_chckbx.setChecked(False)
        self.prob_dist_chckbx.setChecked(False)
        self.corr_coeff_chckbx.setChecked(False)
        self.spearman_chckbx.setChecked(False)

        # default output group
        self.displayResults_chckbx.setChecked(True)
        self.saveResults_chckbx.setChecked(False)

        # default data type group
        self.interval_radiobttn.setChecked(True)

        # Empty variables
        self.set_defaults()
        self.resultsWindow.init_ui()

    #  Toggle functions
    def set_datatype_interval(self):
        self.datatype = "Interval"

    def set_datatype_ordinal(self):
        self.datatype = "Ordinal"

    def toggle_display(self):
        self.display = not self.display
        if self.do_logging:
            logging.info(f"display is set to: {self.display}")

    def toggle_save(self):
        self.save = not self.save
        if self.do_logging:
            logging.info(f"save output is set to: {self.save}")


# Other window classes
class ResultsDisplay(QWidget):
    def __init__(self):
        self.app = QApplication([])
        super(ResultsDisplay, self).__init__()
        self.w = QWidget()  # Base widget
        self.w.setFixedSize(900, 600) # Window default size
        #self.w.resize(900, 600)  # Window default size
        self.w.setWindowTitle("Statistical Analyzer Results")  # Window title
        self.app.setStyle("Fusion")  # Style of app (choices are: Fusion, Windows, WindowsVista, Macintosh)
        self.init_ui()

    def init_ui(self):
        self.result_lbl = QLabel(self.w)
        self.result_lbl.setText("Results:")
        self.result_layout = QVBoxLayout()
        self.oper_lbl = QLabel(self.w)
        self.pretest_lbl = QLabel(self.w)
        self.scroll = QScrollArea(self.w)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.resize(900, 600)
        self.scroll.setWidget(self.result_lbl)

    def start(self):
        self.w.show()
        self.close()


class DataInputWindow(QWidget):
    """User input for data"""
    def __init__(self):
        self.app = QApplication([])
        super(DataInputWindow, self).__init__()
        self.w = QWidget()  # Base widget
        self.w.resize(500, 300)  # Window default size
        self.w.setWindowTitle("Statistical Analyzer Manual Data Entry")  # Window title
        self.app.setStyle("Fusion")  # Style of app (choices are: Fusion, Windows, WindowsVista, Macintosh)
        self.rows = 0
        self.cols = 0
        self.data = None
        self.textBoxes = []
        self.submitData_bttn = QPushButton("Submit data")
        self.submitData_bttn.clicked.connect(self.grab_input)
        self.inputLayout = QGridLayout(self.w)

    def start(self, rows, cols, data_object):
        """Checks inputs and shows window
        :param rows: String, number of rows to add
        :param cols: String, number of columns to add
        :param data_object: Data.Data
        """
        self.data = data_object
        try:
            tmp = int(rows)
            tmp = int(cols)
        except ValueError:
            if self.do_logging:
                logging.warning("Warning, rows/cols not integers.")
            return
        self.rows = int(rows)
        if self.rows > 50:
            self.rows = 50
        elif self.rows < 1:
            return
        self.cols = int(cols)
        if self.cols > 50:
            self.cols = 50
        elif self.cols < 1:
            return
        self.setup_elements()
        self.w.show()

    def setup_elements(self):
        """Initializes input array boxes."""
        self.textBoxes = []
        if self.do_logging:
            logging.info(self.rows)
            logging.info(self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                self.textBoxes.append(QLineEdit())
                self.inputLayout.addWidget(self.textBoxes[-1], i, j)
        self.inputLayout.addWidget(self.submitData_bttn, self.rows+1, 1, self.cols+1, 3)

    def grab_input(self):
        """Converts input to variables for data object"""
        for x in self.textBoxes:
            if x.text() == "":
                if self.do_logging:
                    logging.warning("Warning: Entry box empty. Cannot get inputs.")
                return
        user_input = np.array([int(x.text()) for x in self.textBoxes])
        user_input = np.reshape(user_input, (self.rows, self.cols))
        row_labels = ["Row {}".format(i+1) for i in range(self.rows)]
        col_labels = ["Col {}".format(i+1) for i in range(self.cols)]
        self.data.add_data(user_input, col_labels, row_labels)
        self.w.close()


if __name__ == "__main__":
    myGUI = StatsOperator()
    myGUI.start_GUI()
