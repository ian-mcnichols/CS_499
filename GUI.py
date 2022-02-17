import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QGroupBox, QVBoxLayout, QCheckBox, \
    QRadioButton, QPushButton, QHBoxLayout

if __name__ == "__main__":
    app = QApplication([])                      # Needed for UI
    w = QWidget()                               # Base widget
    w.resize(500, 600)                          # Window default size
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

    operation_chckbx = QCheckBox("Mean")
    vertLay.addWidget(operation_chckbx)
    operation_chckbx = QCheckBox("Median")
    vertLay.addWidget(operation_chckbx)
    operation_chckbx = QCheckBox("Mode")
    vertLay.addWidget(operation_chckbx)
    operation_chckbx = QCheckBox("Standard deviation")
    vertLay.addWidget(operation_chckbx)
    operation_chckbx = QCheckBox("Variance")
    vertLay.addWidget(operation_chckbx)
    operation_chckbx = QCheckBox("Coefficient of variance")
    vertLay.addWidget(operation_chckbx)
    operation_chckbx = QCheckBox("Percentiles")
    vertLay.addWidget(operation_chckbx)
    operation_chckbx = QCheckBox("Probability distribution")
    vertLay.addWidget(operation_chckbx)
    operation_chckbx = QCheckBox("Binomial distribution")
    vertLay.addWidget(operation_chckbx)
    operation_chckbx = QCheckBox("Least square line")
    vertLay.addWidget(operation_chckbx)
    operation_chckbx = QCheckBox("Chi square")
    vertLay.addWidget(operation_chckbx)
    operation_chckbx = QCheckBox("Correlation coefficient")
    vertLay.addWidget(operation_chckbx)
    operation_chckbx = QCheckBox("Sign test")
    vertLay.addWidget(operation_chckbx)
    operation_chckbx = QCheckBox("Rank sum test")
    vertLay.addWidget(operation_chckbx)
    operation_chckbx = QCheckBox("Spearman rank correction coefficient")
    vertLay.addWidget(operation_chckbx)

    # Data range option:
    dataRange_group = QGroupBox("Data Range:")
    dataRange_layout = QGridLayout()
    dataRange_group.setLayout(dataRange_layout)

    allOfFile_radiobttn = QRadioButton("All of file")
    allOfFile_radiobttn.setChecked(True)
    dataRange_layout.addWidget(allOfFile_radiobttn, 0, 0)
    partialRange_radiobttn = QRadioButton("Partial range")
    dataRange_layout.addWidget(partialRange_radiobttn, 1, 0)

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
    appLayout.addWidget(operations_group, 1, 1, 2, 1)
    appLayout.addWidget(dataRange_group, 1, 0)
    appLayout.addWidget(output_group, 2, 0)
    appLayout.addWidget(calcResults_bttn, 3, 0, 3, 2)

    w.show()
    sys.exit(app.exec_())       # Run the app until the user closes
