from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QLineEdit, QFileDialog, QStackedWidget,
                              QScrollArea, QGroupBox, QFrame)
from PySide6.QtCore import Qt
from sys import argv
from collections import defaultdict

from read_dir import read_dir

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
        self.monitoring_page = self.create_monitoring_page()

        self.stacked_widget.addWidget(self.menu_page)
        self.stacked_widget.addWidget(self.actions_page)
        self.stacked_widget.addWidget(self.monitoring_page)

    
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
        monitoring_btn.clicked.connect(self.open_monitoring_page)
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
    
    def create_monitoring_page(self):
        page = QWidget()
        monitoring_layout = QVBoxLayout()
        monitoring_layout.setContentsMargins(20, 20, 20, 20)

        # Title and path
        title = QLabel("Monitoring for:")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 2px;")
        monitoring_layout.addWidget(title)
        
        # Create a NEW subtitle for monitoring page
        self.MP_subtitle = QLabel("")
        self.MP_subtitle.setAlignment(Qt.AlignCenter)
        self.MP_subtitle.setStyleSheet("font-size: 14px; font-style: italic; margin-bottom: 20px;")
        monitoring_layout.addWidget(self.MP_subtitle)

        # Scroll area setup
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        scroll.setWidget(self.scroll_content)
        
        # Add scroll area to layout
        monitoring_layout.addWidget(scroll)
        
        page.setLayout(monitoring_layout)
        return page

    def open_monitoring_page(self):
        self.stacked_widget.setCurrentIndex(2)
        
        # Update monitoring page subtitle
        self.MP_subtitle.setText(self.MP_path_input.text().strip())
        
        # Clear previous content
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Load data and populate layout
        try:
            data = read_dir(self.MP_path_input.text().strip())
            
            # Group processes by computer
            computer_processes = defaultdict(list)
            for process_group in data['FOLYAMATOK'].values():
                for process in process_group:
                    computer_name = process['SZAMITOGEP']
                    computer_processes[computer_name].append(process)
            
            # Create computer sections
            for computer_name, specs in data['SZAMITOGEPEK'].items():
                computer_group = QGroupBox(f"{computer_name}")
                computer_layout = QVBoxLayout()
                
                # Computer specs
                specs_layout = QHBoxLayout()
                specs_layout.addWidget(QLabel(f"Magszám: {specs['MAGSZAM']}"))
                specs_layout.addWidget(QLabel(f"Memória egységek: {specs['MEMORIASZAM']}"))
                specs_layout.addStretch()
                
                computer_layout.addLayout(specs_layout)
                
                # Processes for this computer
                processes = computer_processes.get(computer_name, [])
                for process in processes:
                    process_frame = QFrame()
                    process_frame.setFrameShape(QFrame.Box)
                    process_frame.setLineWidth(1)
                    
                    process_layout = QHBoxLayout()
                    process_layout.addWidget(QLabel(f"Kód: {process['KOD']}"))
                    process_layout.addWidget(QLabel(f"Indítás: {process['INDITAS']}"))
                    process_layout.addWidget(QLabel(f"Magszám: {process['MAGSZAM']}"))
                    process_layout.addWidget(QLabel(f"Memória: {process['MEMORIASZAM']}"))
                    process_layout.addWidget(QLabel("Aktív" if process['AKTIV'] else "Inaktív"))
                    process_layout.addStretch()
                    
                    process_frame.setLayout(process_layout)
                    computer_layout.addWidget(process_frame)
                
                computer_group.setLayout(computer_layout)
                self.scroll_layout.addWidget(computer_group)
            
            self.scroll_layout.addStretch()
        
        except Exception as e:
            print(f"Error loading data: {e}")


if __name__ == '__main__':
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec()