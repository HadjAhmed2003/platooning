import sys
import socket
import threading
from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QMessageBox
from PySide6.QtCore import Qt

HOST = "192.168.1.219"  # Standard loopback interface address (localhost)
PORT = 5000  # Port to listen on (non-privileged ports are > 1023)
clients = {}  # Dictionary to store connected clients and their socket objects

def start_game_server(client_selection_window):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            print(addr[0])
            clients[addr[0]] = conn  # Store the client's socket object with its address
            client_selection_window.add_client(addr)
            data = conn.recv(1024)
            print(data)

class ClientSelectionWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Client Selection")
        self.setGeometry(100, 100, 300, 300)

        layout = QVBoxLayout()

        self.client_list = QListWidget()
        layout.addWidget(self.client_list)

        self.select_button = QPushButton("Select Clients")
        self.select_button.clicked.connect(self.select_clients)
        layout.addWidget(self.select_button)

        self.setLayout(layout)

    def add_client(self, address):
        item = QListWidgetItem(address[0] + ":" + str(address[1]))
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Unchecked)
        self.client_list.addItem(item)

    def select_clients(self):
        selected_clients = []
        for i in range(self.client_list.count()):
            item = self.client_list.item(i)
            if item.checkState() == Qt.Checked:
                selected_clients.append(item.text().split(":")[0])
        if selected_clients:
            start_game_window = StartGameWindow(selected_clients)
            start_game_window.show()
            self.hide()

class StartGameWindow(QWidget):
    def __init__(self, selected_clients, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Start Game")
        
        layout = QVBoxLayout(self)
        
        # label = QLabel("Start the game and send 'Hello' to the selected clients?")
        # layout.addWidget(label)
        
        # Add custom "Start the game" button
        self.start_game_button = QPushButton("Start the game")
        self.end_game_button = QPushButton("end the game")
        layout.addWidget(self.start_game_button)
        layout.addWidget(self.end_game_button)
        # Connect button clicked signal to handler
        self.start_game_button.clicked.connect(lambda: self.handle_start_game(selected_clients))
        self.end_game_button.clicked.connect(lambda: self.handle_end_game(selected_clients))

    def handle_start_game(self, selected_clients):
        # Send "start" message to the selected clients
        for client in selected_clients:
            print(client)
            clients[client].sendall(b"start")
            print("Sent 'start' to client:", client)
    def handle_end_game(self, selected_clients):
        # Send "start" message to the selected clients
        for client in selected_clients:
            print(client)
            clients[client].sendall(b"end")
            print("Sent 'end' to client:", client)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set up the client selection window
    client_selection_window = ClientSelectionWindow()
    client_selection_window.show()

    # Start the game server
    start_game_server_thread = threading.Thread(target=start_game_server, args=(client_selection_window,))
    start_game_server_thread.start()

    # Run the application
    sys.exit(app.exec())