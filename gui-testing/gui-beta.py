from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QPushButton, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a QStackedWidget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create pages
        self.page1 = self.create_page("Page 1", "Go to Page 2", self.go_to_page2)
        self.page2 = self.create_page("Page 2", "Go to Page 1", self.go_to_page1)

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)

    def create_page(self, label_text, button_text, button_callback):
        # Create a widget for the page
        page = QWidget()
        layout = QVBoxLayout()

        # Add a label to the page
        label = QLabel(label_text)
        layout.addWidget(label)

        # Add a button to switch pages
        button = QPushButton(button_text)
        button.clicked.connect(button_callback)
        layout.addWidget(button)

        # Set the layout for the page
        page.setLayout(layout)
        return page

    def go_to_page1(self):
        self.stacked_widget.setCurrentIndex(0)

    def go_to_page2(self):
        self.stacked_widget.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()