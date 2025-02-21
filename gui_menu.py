from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QLineEdit, QFileDialog, QStackedWidget)
from PySide6.QtCore import Qt
from sys import argv

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ELZ GUI")
        self.setGeometry(500, 100, 500, 800)
        self.setMinimumSize(500, 800)

        # Create a QStackedWidget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create pages
        self.menu_page = self.create_menu_page()
        self.actions_page = self.create_actions_page()

        self.stacked_widget.addWidget(self.menu_page)
        self.stacked_widget.addWidget(self.actions_page)

    
    def create_menu_page(self):
        page = QWidget()
        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Main menu")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        menu_layout.addWidget(title)

        path_layout = QHBoxLayout()

        # MP: Menu page
        self.MP_path_input = QLineEdit()
        self.MP_path_input.setPlaceholderText("Select folder path...")

        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_folder)

        self.MP_open_btn = QPushButton("Open")
        self.MP_open_btn.clicked.connect(self.open_path_page)

        path_layout.addWidget(self.MP_path_input)
        path_layout.addWidget(browse_btn)
        path_layout.addWidget(self.MP_open_btn)
        menu_layout.addLayout(path_layout)

        # Push everything to top
        menu_layout.addStretch()

        page.setLayout(menu_layout)
        return page;

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.MP_path_input.setText(folder)

    def create_actions_page(self):
        page = QWidget()
        actions_layout = QVBoxLayout()
        actions_layout.setContentsMargins(20, 20, 20, 20)

        # The title text, and below it the path
        title = QLabel("Actions for:")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 2px;")
        actions_layout.addWidget(title)

        self.AP_subtitle = QLabel("") # setting text at open_path_page()
        self.AP_subtitle.setAlignment(Qt.AlignCenter)
        self.AP_subtitle.setStyleSheet("font-size: 14px; font-style: italic; margin-bottom: 20px;")
        actions_layout.addWidget(self.AP_subtitle)

        # Add some spacing
        actions_layout.addSpacing(15)

        # Monitoring button
        monitoring_btn = QPushButton("Monitoring")
        monitoring_btn.setFixedSize(200, 60)

        actions_layout.addLayout(self.get_h_centered_layout(monitoring_btn))

        # Add spacing
        actions_layout.addSpacing(20)

        # Return button
        return_btn = QPushButton("Return to selection page")
        return_btn.setFixedSize(200, 60)
        return_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        actions_layout.addLayout(self.get_h_centered_layout(return_btn))

        # Push everything to top
        actions_layout.addStretch()

        page.setLayout(actions_layout)

        return page

    def get_h_centered_layout(self, widget) -> QHBoxLayout:
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(widget)
        h_layout.addStretch()
        return h_layout

    def open_path_page(self):
        self.stacked_widget.setCurrentIndex(1)
        self.AP_subtitle.setText(self.MP_path_input.text().strip())        


if __name__ == '__main__':
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec()