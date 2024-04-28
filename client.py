import socket
import time
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton
import os
import signal
import admin
HOST = "192.168.1.219"  # Server IP address
PORT = 5000  # Server port
RETRY_INTERVAL = 2  # Interval in seconds between connection retries
game_proc=0
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connection Setup")
        self.layout = QVBoxLayout()

        self.age_label = QLabel("Enter your age:")
        self.layout.addWidget(self.age_label)

        self.age_input = QLineEdit()
        self.layout.addWidget(self.age_input)

        self.sex_label = QLabel("Select your sex:")
        self.layout.addWidget(self.sex_label)

        # Radio buttons for selecting sex
        self.male_radio = QRadioButton("Male")
        self.female_radio = QRadioButton("Female")
        self.layout.addWidget(self.male_radio)
        self.layout.addWidget(self.female_radio)

        self.connect_button = QPushButton("Connect to Server")
        self.connect_button.clicked.connect(self.connect_to_server)
        self.layout.addWidget(self.connect_button)

        self.setLayout(self.layout)

    def connect_to_server(self):
        age = self.age_input.text()
        sex = "Male" if self.male_radio.isChecked() else "Female"

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(f"Age: {age}, Sex: {sex}".encode())
                print("Connected to server.")
                while True: 
                    data = s.recv(1024)
                    if data == b"start":
                        # Path to the executable file
                        executable_path = r"C:\Program Files (x86)\Steam\steamapps\common\American Truck Simulator Demo\bin\win_x64\amtrucks.exe"
                        # Call the subprocess to execute the executable file
                        game_proc=subprocess.Popen([executable_path])
                    if data == b"end":
                        pid=game_proc.pid
                        os.kill(int(pid),signal.SIGTERM)
                    print("Received:", data.decode())
        except ConnectionRefusedError:
            print("Connection refused. Retrying in", RETRY_INTERVAL, "seconds...")
            time.sleep(RETRY_INTERVAL)

if __name__ == "__main__":
    if not admin.isUserAdmin():
        admin.runAsAdmin()
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()