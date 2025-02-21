import sys 
from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow
from PySide6.QtCore import QSize, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Hello")
        
        button = QPushButton("button")
        button.setFixedSize(QSize(200, 150))
        
        self.setFixedSize(QSize(400, 300))
        
        self.setCentralWidget(button)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()