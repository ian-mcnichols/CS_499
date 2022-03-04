import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QGroupBox, QVBoxLayout, QCheckBox, \
    QRadioButton, QPushButton, QHBoxLayout


if __name__ == "__main__":
    app = QApplication([])                      # Needed for UI
    w = QWidget()                               # Base widget
    w.resize(500, 500)                          # Window default size
    w.setWindowTitle("Statistical Analyzer")    # Window title
    app.setStyle("Fusion")                      # Style of app (choices are: Fusion, Windows, WindowsVista, Macintosh)

    # File name option:
    fileName_lbl = QLabel(w)
    fileName_lbl.setText("File name: ")
    fileName_lbl.show()

    fileName_txtbx = QLineEdit(w)
    fileName_txtbx.setPlaceholderText("Enter file name")
    fileName_txtbx.show()
    fileName_lbl.setBuddy(fileName_lbl)

    fileName_layout = QHBoxLayout()
    fileName_layout.addWidget(fileName_lbl)
    fileName_layout.addWidget(fileName_txtbx)

    submit_bttn = QPushButton("Submit")
    fileName_layout.addWidget(submit_bttn)

    # Operation options:
    operations_group = QGroupBox("Operations:")
    vertLay = QVBoxLayout()
    operations_group.setLayout(vertLay)

    mean_chckbx = QCheckBox("Mean")
    vertLay.addWidget(mean_chckbx)
    median_chckbx = QCheckBox("Median")
    vertLay.addWidget(median_chckbx)
    mode_chckbx = QCheckBox("Mode")
    vertLay.addWidget(mode_chckbx)
    range_chckbx = QCheckBox("Range")
    vertLay.addWidget(range_chckbx)
    stndrddev_chckbx = QCheckBox("Standard deviation")
    vertLay.addWidget(stndrddev_chckbx)
    variance_chckbx = QCheckBox("Variance")
    vertLay.addWidget(variance_chckbx)
    coeffvar_chckbx = QCheckBox("Coefficient of variance")
    vertLay.addWidget(coeffvar_chckbx)
    percentile_chckbx = QCheckBox("Percentiles")
    vertLay.addWidget(percentile_chckbx)
    #operation_chckbx = QCheckBox("Probability distribution")
    #vertLay.addWidget(operation_chckbx)
    #operation_chckbx = QCheckBox("Binomial distribution")
    #vertLay.addWidget(operation_chckbx)
    leastsqr_chckbx = QCheckBox("Least square line")
    vertLay.addWidget(leastsqr_chckbx)
    chi_chckbx = QCheckBox("Chi square")
    vertLay.addWidget(chi_chckbx)
    #operation_chckbx = QCheckBox("Correlation coefficient")
    #vertLay.addWidget(operation_chckbx)
    #operation_chckbx = QCheckBox("Sign test")
    #vertLay.addWidget(operation_chckbx)
    #operation_chckbx = QCheckBox("Rank sum test")
    #vertLay.addWidget(operation_chckbx)
    #operation_chckbx = QCheckBox("Spearman rank correction coefficient")
    #vertLay.addWidget(operation_chckbx)

    # Data range option:
    dataRange_group = QGroupBox("Data Range:")
    dataRange_layout = QVBoxLayout()
    dataRange_group.setLayout(dataRange_layout)

    allOfFile_radiobttn = QRadioButton("All of file")
    allOfFile_radiobttn.setChecked(True)
    dataRange_layout.addWidget(allOfFile_radiobttn)

    partialRange_layout = QGridLayout()
    partialRange_radiobttn = QRadioButton("Partial range")
    partialRange_layout.addWidget(partialRange_radiobttn, 0, 0)

    rowTxtbx_lbl = QLabel()
    rowTxtbx_lbl.setText("Rows")
    partialRange_layout.addWidget(rowTxtbx_lbl, 1, 1)
    minRow_txtbx = QLineEdit()
    minRow_txtbx.setPlaceholderText("Min row number")
    partialRange_layout.addWidget(minRow_txtbx, 2, 1)
    maxRow_txtbx = QLineEdit()
    maxRow_txtbx.setPlaceholderText("Max row number")
    partialRange_layout.addWidget(maxRow_txtbx, 2, 3)

    columnTxtbx_lbl = QLabel()
    columnTxtbx_lbl.setText("Columns")
    partialRange_layout.addWidget(columnTxtbx_lbl, 3, 1)
    minColumn_txtbx = QLineEdit()
    minColumn_txtbx.setPlaceholderText("Min column number")
    partialRange_layout.addWidget(minColumn_txtbx, 4, 1)
    maxColumn_txtbx = QLineEdit()
    maxColumn_txtbx.setPlaceholderText("Max column number")
    partialRange_layout.addWidget(maxColumn_txtbx, 4, 3)
    dataRange_layout.addLayout(partialRange_layout)

    # Data type option:
    dataType_group = QGroupBox("Data Type: ")
    dataType_layout = QVBoxLayout()
    dataType_group.setLayout(dataType_layout)

    ordinal_radiobttn = QRadioButton("Ordinal data")
    ordinal_radiobttn.setChecked(True)
    range_chckbx.setDisabled(True)      # since ordinal is checked by default, disable range option by default
    dataType_layout.addWidget(ordinal_radiobttn)
    interval_radiobttn = QRadioButton("Interval data")
    dataType_layout.addWidget(interval_radiobttn)

    # Set default disables (all of file option selected by default)
    columnTxtbx_lbl.setDisabled(True)
    rowTxtbx_lbl.setDisabled(True)
    maxRow_txtbx.setDisabled(True)
    minRow_txtbx.setDisabled(True)
    maxColumn_txtbx.setDisabled(True)
    minColumn_txtbx.setDisabled(True)

    # Output option:
    output_group = QGroupBox("Output:")
    output_layout = QVBoxLayout()
    output_group.setLayout(output_layout)

    displayResults_chckbx = QCheckBox("Display results")
    output_layout.addWidget(displayResults_chckbx)
    saveResults_chckbx = QCheckBox("Save results to computer")
    output_layout.addWidget(saveResults_chckbx)

    # Calculate results button:
    calcResults_bttn = QPushButton("Calculate Results")

    # Main app layout:
    appLayout = QGridLayout(w)
    appLayout.addLayout(fileName_layout, 0, 0, 1, 0)
    appLayout.addWidget(operations_group, 1, 1, 3, 1)
    appLayout.addWidget(dataRange_group, 1, 0)
    appLayout.addWidget(dataType_group, 2, 0)
    appLayout.addWidget(output_group, 3, 0)
    appLayout.addWidget(calcResults_bttn, 4, 0, 4, 2)

    # Disable operations depending on data type
    ordinal_radiobttn.toggled.connect(stndrddev_chckbx.setEnabled)
    ordinal_radiobttn.toggled.connect(variance_chckbx.setEnabled)
    ordinal_radiobttn.toggled.connect(coeffvar_chckbx.setEnabled)
    ordinal_radiobttn.toggled.connect(percentile_chckbx.setEnabled)
    ordinal_radiobttn.toggled.connect(leastsqr_chckbx.setEnabled)

    # Disable data range options based on selection
    allOfFile_radiobttn.toggled.connect(columnTxtbx_lbl.setDisabled)
    allOfFile_radiobttn.toggled.connect(rowTxtbx_lbl.setDisabled)
    allOfFile_radiobttn.toggled.connect(maxRow_txtbx.setDisabled)
    allOfFile_radiobttn.toggled.connect(minRow_txtbx.setDisabled)
    allOfFile_radiobttn.toggled.connect(maxColumn_txtbx.setDisabled)
    allOfFile_radiobttn.toggled.connect(minColumn_txtbx.setDisabled)

    interval_radiobttn.toggled.connect(range_chckbx.setEnabled)

    w.show()

    sys.exit(app.exec_())       # Run the app until the user closes
