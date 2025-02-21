import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QSizePolicy
)
from PySide6.QtCore import Qt

class MenuPage(QWidget):
    def __init__(self, buttonnames):
        super().__init__()

        self.setMinimumSize(400, 400)

        self.setWindowTitle("Menu Page")
        main_layout = QVBoxLayout(self)

        # Title Label at the top centre
        title_label = QLabel("Menu")
        title_label.setAlignment(Qt.AlignHCenter)
        main_layout.addWidget(title_label)

        # Input area: QLineEdit with "Browse" and "Save" buttons in a horizontal layout
        input_layout = QHBoxLayout()
        # Add some padding to the layout (left, top, right, bottom)
        input_layout.setContentsMargins(10, 10, 10, 10)

        # QLineEdit for the folder path
        self.path_line_edit = QLineEdit()
        input_layout.addWidget(self.path_line_edit)

        # Browse button: opens a file explorer to select a folder
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.open_file_explorer)
        input_layout.addWidget(browse_button)

        # Save button: currently does nothing
        save_button = QPushButton("Save")
        input_layout.addWidget(save_button)

        main_layout.addLayout(input_layout)

        # List of buttons, centered horizontally
        for name in buttonnames:
            # Create a button with the given name
            button = QPushButton(name)
            # Wrap the button in a horizontal layout with stretch on both sides to center it
            button_layout = QHBoxLayout()
            button_layout.addStretch(1)
            button_layout.addWidget(button)
            button_layout.addStretch(1)
            main_layout.addLayout(button_layout)

        # Optionally add a stretch at the bottom to push all items to the top
        main_layout.addStretch()

    def open_file_explorer(self):
        # Open a dialog to select a folder
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.path_line_edit.setText(folder)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # List of button names for the bottom part
    buttonnames = ["first", "second", "third"]
    window = MenuPage(buttonnames)
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec())