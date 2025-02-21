from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QLineEdit, QFileDialog)
from PySide6.QtCore import Qt

class MenuPage(QWidget):
    def __init__(self, button_names):
        super().__init__()
        self.button_names = button_names
        self.init_ui()
        
    def init_ui(self):
        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)  # Add padding around edges
        
        # Title label (centered at top)
        title = QLabel("Menu")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        main_layout.addWidget(title)
        
        # Path input row
        path_layout = QHBoxLayout()
        
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select folder path...")
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_folder)
        
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.add_path_button)
        
        # Add widgets to path row with spacing
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_btn)
        path_layout.addWidget(self.save_btn)
        main_layout.addLayout(path_layout)
        
        # Add some spacing between sections
        main_layout.addSpacing(30)
        
        # Dynamic buttons section
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.setAlignment(Qt.AlignCenter)
        
        # Add initial buttons
        for name in self.button_names:
            self.create_button(name.capitalize())
        
        main_layout.addLayout(self.buttons_layout)
        main_layout.addStretch()  # Push everything to top
        
        self.setLayout(main_layout)
    
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.path_input.setText(folder)
    
    def create_button(self, text):
        """Helper function to create centered buttons"""
        btn = QPushButton(text)
        btn.setFixedSize(150, 40)
        
        # Center button in horizontal layout
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(btn)
        h_layout.addStretch()
        
        self.buttons_layout.addLayout(h_layout)
    
    def add_path_button(self):
        """Add a new button with the current path"""
        path = self.path_input.text().strip()
        if path:
            self.create_button(path)
            self.path_input.clear()  # Clear the input after adding

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-Page App")
        self.setGeometry(100, 100, 600, 400)
        
        # Create menu page with initial button names
        button_names = ["first", "second", "third"]
        self.menu_page = MenuPage(button_names)
        
        self.setCentralWidget(self.menu_page)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()