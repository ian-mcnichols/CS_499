style_string = """QWidget { background: #eeeeee; }

QGroupBox:enabled {
    color: black;
    font: bold;
    font: 20px;
}

QGroupBox:disabled {
    color: #444444;
    font: bold;
    font: 20px;
}

QPushButton { font: 12px; }
QPushButton:enabled { color: black; background: #0b7ecf; }
QPushButton:disabled { color: black; background: #24394a; }
QPushButton:hover {
    background: #009de0;
    color: black;
}

QLineEdit { color: black; font: 12px; }
QLineEdit:enabled { color: black; background: white;}

Qlabel { font: 12px; }
QLabel:enabled { color: black; }
QLabel:disabled { color: #444444; }

QCheckBox { font: 12px;}
QCheckBox:enabled { color: black; }
QCheckBox:disabled { color: #444444; }
QCheckBox:enabled:checked { color: #0b7ecf; }

QRadioButton { font: 12px; }
QRadioButton:enabled { color: black; }
QRadioButton:disabled { color: black; }
QRadioButton:checked { color: black; color: #0b7ecf; }
"""
