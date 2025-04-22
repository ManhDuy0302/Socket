from server.server import TodoServer
from client.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
import threading

def run_server():
    server = TodoServer()
    server.start()

if __name__ == '__main__':
    # Start server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Start PyQt5 application
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())