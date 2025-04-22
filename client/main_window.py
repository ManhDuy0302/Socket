import socket
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLineEdit, QTextEdit, 
                            QListWidget, QMessageBox)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo List Manager (Socket)")
        self.setGeometry(100, 100, 600, 400)
        self.host = '127.0.0.1'
        self.port = 12345
        self.init_ui()
        self.load_todos()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()

        # Left panel - List of todos
        self.todo_list = QListWidget()
        self.todo_list.itemClicked.connect(self.display_todo)
        layout.addWidget(self.todo_list)

        # Right panel - Todo details and controls
        right_panel = QVBoxLayout()
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Todo Title")
        right_panel.addWidget(self.title_input)

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Todo Description")
        right_panel.addWidget(self.desc_input)

        # Buttons
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Add Todo")
        self.add_button.clicked.connect(self.add_todo)
        button_layout.addWidget(self.add_button)

        self.update_button = QPushButton("Update Todo")
        self.update_button.clicked.connect(self.update_todo)
        button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete Todo")
        self.delete_button.clicked.connect(self.delete_todo)
        button_layout.addWidget(self.delete_button)

        right_panel.addLayout(button_layout)
        layout.addLayout(right_panel)
        
        central_widget.setLayout(layout)

    def send_request(self, request):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            client_socket.send(json.dumps(request).encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            client_socket.close()
            return json.loads(response)
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def load_todos(self):
        request = {'action': 'get_all'}
        response = self.send_request(request)
        if response['status'] == 'success':
            self.todo_list.clear()
            for todo in response['data']:
                self.todo_list.addItem(f"{todo['id']}: {todo['title']}")
        else:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải danh sách: {response['message']}")

    def display_todo(self, item):
        todo_id = int(item.text().split(':')[0])
        request = {'action': 'get', 'data': {'id': todo_id}}
        response = self.send_request(request)
        if response['status'] == 'success':
            self.title_input.setText(response['data']['title'])
            self.desc_input.setPlainText(response['data']['description'])
        else:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải công việc: {response['message']}")

    def add_todo(self):
        request = {
            'action': 'create',
            'data': {
                'title': self.title_input.text(),
                'description': self.desc_input.toPlainText()
            }
        }
        response = self.send_request(request)
        if response['status'] == 'success':
            self.load_todos()
            self.clear_inputs()
        else:
            QMessageBox.critical(self, "Lỗi", f"Không thể thêm công việc: {response['message']}")

    def update_todo(self):
        selected = self.todo_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một công việc để cập nhật")
            return
        
        todo_id = int(selected.text().split(':')[0])
        request = {
            'action': 'update',
            'data': {
                'id': todo_id,
                'title': self.title_input.text(),
                'description': self.desc_input.toPlainText(),
                'completed': False
            }
        }
        response = self.send_request(request)
        if response['status'] == 'success':
            self.load_todos()
            self.clear_inputs()
        else:
            QMessageBox.critical(self, "Lỗi", f"Không thể cập nhật công việc: {response['message']}")

    def delete_todo(self):
        selected = self.todo_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một công việc để xóa")
            return
        
        todo_id = int(selected.text().split(':')[0])
        request = {'action': 'delete', 'data': {'id': todo_id}}
        response = self.send_request(request)
        if response['status'] == 'success':
            self.load_todos()
            self.clear_inputs()
        else:
            QMessageBox.critical(self, "Lỗi", f"Không thể xóa công việc: {response['message']}")

    def clear_inputs(self):
        self.title_input.clear()
        self.desc_input.clear()