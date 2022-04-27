style_string = """QWidget { background: #eeeeee; }

QGroupBox:enabled {
    color: black;
    font: bold;
    font: 20px;
}

QGroupBox:disabled {
    color: #bcbcbc;
    font: bold;
    font: 20px;
}

QPushButton { font: 12px; }
QPushButton:enabled { background: #0b7ecf; }
QPushButton:disabled { background: #24394a; }
QPushButton:hover {
    background: #009de0;
    color: black;
}

QLineEdit { color: black; font: 12px; }

QLineEdit:enabled { color: black; background: white;}

Qlabel { font: 12px; }
QLabel:enabled { color: black; }
QLabel:disabled { color: #bcbcbc; }

QCheckBox { font: 12px;}
QCheckBox:enabled { color: black; }
QCheckBox:disabled { color: #bcbcbc; }
QCheckBox:enabled:checked { color: #0b7ecf; }

QRadioButton { font: 12px; }
QRadioButton:enabled { color: black; }
QRadioButton:disabled { color: black; }
QRadioButton:checked { color: black; color: #0b7ecf; }
"""
