import socket
import json
import threading
from .models import TodoModel

class TodoServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.model = TodoModel()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

    def start(self):
        print(f"Server started on {self.host}:{self.port}")
        while True:
            client_socket, addr = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            client_thread.start()

    def handle_client(self, client_socket, addr):
        try:
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                request = json.loads(data)
                response = self.process_request(request)
                client_socket.send(json.dumps(response).encode('utf-8'))
        except Exception as e:
            print(f"Error handling client {addr}: {str(e)}")
        finally:
            client_socket.close()

    def process_request(self, request):
        action = request.get('action')
        try:
            if action == 'get_all':
                todos = self.model.get_all_todos()
                return {'status': 'success', 'data': todos}
            elif action == 'create':
                todo_id = self.model.create_todo(
                    request['data']['title'],
                    request['data']['description']
                )
                return {'status': 'success', 'data': {'id': todo_id}}
            elif action == 'get':
                todo = self.model.get_todo(request['data']['id'])
                if todo:
                    return {'status': 'success', 'data': todo}
                return {'status': 'error', 'message': 'Todo not found'}
            elif action == 'update':
                todo = self.model.update_todo(
                    request['data']['id'],
                    request['data']['title'],
                    request['data']['description'],
                    request['data']['completed']
                )
                if todo:
                    return {'status': 'success', 'data': todo}
                return {'status': 'error', 'message': 'Todo not found'}
            elif action == 'delete':
                self.model.delete_todo(request['data']['id'])
                return {'status': 'success', 'message': 'Todo deleted'}
            else:
                return {'status': 'error', 'message': 'Invalid action'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}