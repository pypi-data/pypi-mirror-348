import sys 
import time

from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
                             QLabel, QCheckBox, QRadioButton, QButtonGroup,
                             QLineEdit)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt
print(" ")
print("IKcode GUI terminal connector")
print(" ")
print("Server log:")
print(" ")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IKcode GUI terminal connector - v1.0.PyQt5")
        self.setGeometry(100, 100, 800, 800)
        self.setWindowIcon(QIcon("ikcode.png"))
        self.setStyleSheet("background-color: #1a7689;")

        self.checkbox = QCheckBox("Connect to terminal", self)

        self.blabel = QLabel("   GUI disabled", self)

        self.radio1 = QRadioButton("Record to server log", self)
        self.radio2 = QRadioButton("Do not record to server log", self)

        self.button_group = QButtonGroup(self)
        
        label = QLabel("IKcode GUI", self)
        label.setFont(QFont("Veranda", 18, QFont.Bold))
        label.setGeometry(0, 0, 500, 100)
        label.setStyleSheet("color: white; background-color: #1a7689; border: 2px solid #ffcc00;")
        label.setAlignment(Qt.AlignCenter)

        self.rlabel = QLabel("Server preferences:", self)
        self.rlabel.setGeometry(10, 500, 500, 100)
        self.rlabel.setStyleSheet("color: white; background-color: #1a7689; font-size:20px; font-family: Veranda;")
        
        self.tlabel = QLabel("Connect to your \n IKcode account:", self)
        self.tlabel.setGeometry(600, 50, 200, 50)
        self.tlabel.setStyleSheet("color: white; background-color: #1a7689; font-size:16px; font-family: Veranda;")
        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(600, 100, 150, 30)
        self.textbutton = QPushButton("Connect", self)
        self.textbutton.setGeometry(600, 140, 150, 30)

        self.initUI()

        pixmap = QPixmap("ikcode.png")
        picture_label = QLabel(self)
        scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        picture_label.setPixmap(scaled_pixmap)
        picture_label.setGeometry(500, 0, 100, 100)
        picture_label.setAlignment(Qt.AlignCenter)

    def initUI(self):
        self.button = QPushButton("Enable GUI", self)
        self.button.setGeometry(300, 150, 200, 50)
        self.button.setStyleSheet("border: 2px solid #ffcc00; background-color: #155e6e; color: white; font-size: 20px; font-family: Veranda;")
        self.button.clicked.connect(self.on_click)

        self.help_button = QPushButton("Help", self)
        self.help_button.setGeometry(690, 740, 100, 50)
        self.help_button.setStyleSheet("border: 2px solid #ffcc00; background-color: #155e6e; color: white; font-size: 20px; font-family: Veranda;")
        self.help_button.clicked.connect(self.help_button_clicked)

    
        self.blabel.setGeometry(300, 210, 200, 50)
        self.blabel.setStyleSheet("background-color: #155e6e; color: white; font-size: 20px; font-family: Veranda;")
        
        self.checkbox.setStyleSheet("background-color: #155e6e; color: white; font-size: 16px; font-family: Veranda;")
        self.checkbox.setGeometry(300, 270, 200, 50)
        self.checkbox.setChecked(False)
        self.checkbox.stateChanged.connect(self.checkbox_changed)

        self.radio_group = QButtonGroup(self)
        self.radio_group.addButton(self.radio1)
        self.radio_group.addButton(self.radio2)

        self.radio1.setGeometry(10, 610, 200, 50)
        self.radio1.setStyleSheet("background-color: #155e6e; color: white; font-size: 16px; font-family: Veranda;")
        self.radio1.clicked.connect(self.radio1_checked)
        self.radio1.setChecked(True)
        self.log = True
        
        self.radio2.setGeometry(10, 670, 200, 50)
        self.radio2.setStyleSheet("background-color: #155e6e; color: white; font-size: 16px; font-family: Veranda;")
        self.radio2.clicked.connect(self.radio2_checked)

        self.button_group.addButton(self.radio1)
        self.button_group.addButton(self.radio2)

        self.textbox.setStyleSheet("background-color: #155e6e; color: white; font-size: 16px; font-family: Veranda;")
        self.textbutton.setStyleSheet("border: 2px solid #ffcc00; background-color: #155e6e; color: white; font-size: 20px; font-family: Veranda;")
        self.textbutton.clicked.connect(self.textbutton_clicked)


    def on_click(self):
        self.blabel.setText("   GUI enabled")
        self.button.setText("Disable GUI")
        self.button.clicked.connect(self.off_click)    
    
    def off_click(self):
        self.blabel.setText("   GUI disabled")
        self.button.setText("Enable GUI")
        self.button.clicked.connect(self.on_click)

    def checkbox_changed(self, state):
        if self.log:
            if state == Qt.Checked:
                print(" ")
                print("Terminal connected")
                if self.button.text() == "Disable GUI" and self.checkbox.isChecked():
                    print(" ")
                    print("GUI successfully connected to terminal")
                    self.blabel.setText("   GUI enabled")
            else:
                print(" ")
                print("Terminal disconnected")
                if self.button.text() == "Disable GUI" and not self.checkbox.isChecked():
                    print(" ")
                    print("GUI disconnected from terminal")
                

    def radio1_checked(self):
        self.log = True
        print(" ")
        print("Server log enabled")

    def radio2_checked(self):
        self.log = False
        print(" ")
        print("Server log disabled")


    def help_button_clicked(self):
        print(" ")
        print("Help button clicked")
        print(" ")
        print("This is a simple GUI application that connects to a terminal.")
        print("You can enable or disable the GUI, connect or disconnect from the terminal, and choose whether to record to the server log.")
        print(" ")

        print("To use the application:")
        print("1. Click 'Enable GUI' to enable the GUI, it won't show in the server log unless the checkbox is clicked")
        print("2. Check the 'Connect to terminal' checkbox to connect to the terminal.")
        print("3. Choose whether to record to the server log by selecting one of the options under 'server preferences'")
        print(" ")
        print("More info:")
        print("To successfully connect the GUI to the terminal, you need to first enable the GUI before checking the checkbox")
        print("Not seeing any output in the server log? Make sure the server is enabled under 'server preferences'")
        print("^ SCROLL UP ^")
        print(" ")

    def textbutton_clicked(self):
        text = self.textbox.text()

        if self.log:
            time.sleep(0.3)
            print(" ")
            print("Connecting to IKcode account...")
            time.sleep(2.7)
            print(" ")
            print(f"Connected to IKcode account: {text}")
            print(" ")




def runGUI():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    runGUI()

