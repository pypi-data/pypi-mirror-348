# lab.py - Daniel Dunal

"""Testing QT with an example window"""

import sys


# import all modules
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QPushButton,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QRadioButton,
    QGroupBox,
    QVBoxLayout,
    QSlider,
    QSpinBox,
    QListWidget,
    QTableWidget,
    QHeaderView,
    QProgressBar,
    QTextEdit,
)
from PyQt6.QtCore import Qt
import colorsys

# make an instance of QApplication
app = QApplication([])

# make the QWidget
window = QWidget()
window.setStyleSheet("background-color: black;")
window.setWindowTitle("Example Project")
window.setGeometry(100, 100, 560, 600)
titleMsg = QLabel("<h1>Welcome</h1>", parent=window)
titleMsg.move(40, 15)

# add a label for the button
label = QLabel("<h1>Waiting for input</h1>", parent=window)
label.move(40, 300)

# counter label
counts = [0]
counter = QLabel("Counter : " + str(counts[0]), parent=window)
counter.move(40, 130)

# resize
label.resize(440, 30)
counter.resize(220, 30)

# wrap if too long
label.setWordWrap(True)
counter.setWordWrap(True)

# create button
button = QPushButton("Click Me", parent=window)
button.move(40, 60)
button.resize(150, 75)

# create input box
inputBox = QLineEdit(parent=window)
inputBox.move(40, 160)
inputBox.setPlaceholderText("Type in something funny")
inputBox.resize(220, 30)


# on an enter input
def onEnterPressed():
    text = inputBox.text()
    label.setText(f"You typed: {text}")
    inputBox.clear()


# input box signal
inputBox.returnPressed.connect(onEnterPressed)

# update label color
buttonHue = [0]


def changeLabelColor():
    buttonHue[0] = (buttonHue[0] + 30) % 360
    h = buttonHue[0] / 360
    r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    label.setStyleSheet(f"color: rgb({r}, {g}, {b})")


# button on click method
prog = [0]


def onClick():
    label.setText("<h1>clicked</h1>")
    counts[0] += 1
    counter.setText("Counter : " + str(counts[0]))
    if prog[0] <= 100:
        prog[0] += 5
    qBar.setValue(prog[0])


# button on release method
def onRelease():
    changeLabelColor()
    label.setText("Waiting for input...")
    label.setText("<h1>Example by bladewolf!</h1>")


# button signals
button.pressed.connect(onClick)
button.released.connect(onRelease)

# add combo box
comboBox = QComboBox(parent=window)
comboBox.move(40, 200)
items = ["Select a Color", "Red", "Blue", "Green", "Yellow", "Orange"]
comboBox.addItems(items)


# combo box method that changes label color
def onIndexChange(index):
    if index == 1:
        buttonHue[0] = 0
        h = buttonHue[0] / 360
        r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        label.setStyleSheet(f"color: rgb({r}, {g}, {b})")
    if index == 2:
        buttonHue[0] = 240
        h = buttonHue[0] / 360
        r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        label.setStyleSheet(f"color: rgb({r}, {g}, {b})")
    if index == 3:
        buttonHue[0] = 120
        h = buttonHue[0] / 360
        r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        label.setStyleSheet(f"color: rgb({r}, {g}, {b})")
    if index == 4:
        buttonHue[0] = 60
        h = buttonHue[0] / 360
        r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        label.setStyleSheet(f"color: rgb({r}, {g}, {b})")
    if index == 5:
        buttonHue[0] = 30
        h = buttonHue[0] / 360
        r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        label.setStyleSheet(f"color: rgb({r}, {g}, {b})")


comboBox.currentIndexChanged.connect(onIndexChange)

# checkbox
checkBox = QCheckBox("Are you feeling good today?", parent=window)
checkBox.move(40, 240)

# radio buttons, group box, and layout
radioBox = QGroupBox("Pick one", parent=window)
layout = QVBoxLayout()
radioButton1 = QRadioButton("Pick A", parent=window)
radioButton2 = QRadioButton("Pick B", parent=window)
radioButton3 = QRadioButton("Pick C", parent=window)
layout.addWidget(radioButton1)
layout.addWidget(radioButton2)
layout.addWidget(radioButton3)
radioBox.setLayout(layout)
radioBox.move(200, 40)

# slider
sliderLabel = QLabel("Rate your day: ", parent=window)
slider = QSlider(Qt.Orientation.Horizontal, parent=window)
slider.setMinimum(0)
slider.setMaximum(100)
sliderLabel.move(300, 40)
sliderLabel.resize(180, 30)
slider.move(300, 70)


# update label logic
def updateLabel(value):
    sliderLabel.setText(f"Rate your day: {value}")


# slider signals
slider.valueChanged.connect(updateLabel)

# spin box
spinBox = QSpinBox(parent=window)
spinBox.setRange(0, 100)
spinBox.setValue(10)
spinBox.setSingleStep(5)
spinBox.move(300, 100)
spinBox.setStyleSheet(
    """
  QSpinBox {
    font-size: 16px;
    padding: 3px;
  }
  QSpinBox::up-button, QSpinBox::down-button {
    width: 20px;
  }
"""
)


def onChangeValSpinBox(value):
    slider.setSliderPosition(value)


spinBox.valueChanged.connect(onChangeValSpinBox)

# List Widget
qList = QListWidget(parent=window)
qListLabel = QLabel("Pick your favroite food: ", parent=window)
qListLabel.move(300, 160)
qList.move(300, 175)
qList.resize(200, 200)
qList.addItems(["Pizza", "Burritos", "Garlic Bread"])

# Table Widget
qTable = QTableWidget(3, 2, parent=window)
qTable.move(30, 350)
hdr = qTable.horizontalHeader()
hdr.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
vhd = qTable.verticalHeader()
vhd.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

# Progress Bar
qBar = QProgressBar(parent=window)
qBar.move(340, 525)
qBar.resize(200, 40)
qBar.setMinimum(0)
qBar.setMaximum(100)

# Editor
qEditor = QTextEdit(parent=window)
qEditor.move(300, 400)
qEditor.resize(200, 100)
qEditor.setPlaceholderText("Share what is on your mind......")

# show window
window.show()

# run loop
sys.exit(app.exec())
