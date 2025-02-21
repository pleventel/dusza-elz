from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QLineEdit, QFileDialog, QStackedWidget,
                              QScrollArea, QGroupBox, QFrame, QDialog, QMessageBox,
                              QSpinBox, QInputDialog, QComboBox, QCheckBox)
from PySide6.QtCore import Qt
from sys import argv
from collections import defaultdict

from read_dir import read_dir, write_dir

class EditComputerDialog(QDialog):
    def __init__(self, parent, old_name, current_data):
        super().__init__(parent)
        self.old_name = old_name
        self.current_data = current_data
        self.setWindowTitle("Edit Computer")
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Computer name
        self.name_edit = QLineEdit(old_name)
        layout.addWidget(QLabel("Computer Name:"))
        layout.addWidget(self.name_edit)
        
        # Specs
        specs = self.current_data['SZAMITOGEPEK'][old_name]
        self.magszam_spin = QSpinBox()
        self.magszam_spin.setRange(1, 1000000000)
        self.magszam_spin.setValue(specs['MAGSZAM'])
        layout.addWidget(QLabel("Magszám:"))
        layout.addWidget(self.magszam_spin)
        
        self.memoriaszam_spin = QSpinBox()
        self.memoriaszam_spin.setRange(1, 1000000000)
        self.memoriaszam_spin.setValue(specs['MEMORIASZAM'])
        layout.addWidget(QLabel("Memória egységek:"))
        layout.addWidget(self.memoriaszam_spin)
        
        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_changes)
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_computer)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

    def save_changes(self):
        new_name = self.name_edit.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Error", "Computer name cannot be empty!")
            return
            
        specs = {
            'MAGSZAM': self.magszam_spin.value(),
            'MEMORIASZAM': self.memoriaszam_spin.value()
        }
        
        # Update computer name if changed
        if new_name != self.old_name:
            # Update SZAMITOGEPEK
            self.current_data['SZAMITOGEPEK'][new_name] = self.current_data['SZAMITOGEPEK'].pop(self.old_name)
            
            # Update FOLYAMATOK references
            for process_group in self.current_data['FOLYAMATOK'].values():
                for process in process_group:
                    if process['SZAMITOGEP'] == self.old_name:
                        process['SZAMITOGEP'] = new_name
        
        # Update specs
        self.current_data['SZAMITOGEPEK'][new_name].update(specs)
        self.accept()

    def delete_computer(self):
        confirm = QMessageBox.question(
            self, 
            "Confirm Delete",
            f"Delete {self.old_name} and all its processes?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            # Remove from SZAMITOGEPEK
            del self.current_data['SZAMITOGEPEK'][self.old_name]
            
            # Remove associated processes
            for pg_name, processes in list(self.current_data['FOLYAMATOK'].items()):
                remaining = [p for p in processes if p['SZAMITOGEP'] != self.old_name]
                if remaining:
                    self.current_data['FOLYAMATOK'][pg_name] = remaining
                else:
                    del self.current_data['FOLYAMATOK'][pg_name]
            
            self.accept()

class EditProcessDialog(QDialog):
    def __init__(self, parent, process_group_name, process_index, current_data):
        super().__init__(parent)
        self.current_data = current_data
        self.process_group_name = process_group_name
        self.process_index = process_index
        self.original_name = process_group_name
        self.process = current_data['FOLYAMATOK'][process_group_name][process_index]
        
        self.setWindowTitle("Edit Process")
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Process Name
        self.name_edit = QLineEdit(self.process_group_name)
        layout.addWidget(QLabel("Process Group Name:"))
        layout.addWidget(self.name_edit)
        
        # Computer Selection
        self.computer_combo = QComboBox()
        self.computer_combo.addItems(self.current_data['SZAMITOGEPEK'].keys())
        current_computer = self.process['SZAMITOGEP']
        if current_computer in self.current_data['SZAMITOGEPEK']:
            self.computer_combo.setCurrentText(current_computer)
        layout.addWidget(QLabel("Computer:"))
        layout.addWidget(self.computer_combo)
        
        # Process Details
        self.kod_edit = QLineEdit(self.process['KOD'])
        self.kod_edit.setPlaceholderText("Kód...")
        layout.addWidget(QLabel("Kód (egyedinek kell lennie):"))
        layout.addWidget(self.kod_edit)
        
        self.inditas_edit = QLineEdit(self.process['INDITAS'])
        layout.addWidget(QLabel("Indítás:"))
        layout.addWidget(self.inditas_edit)
        
        self.magszam_spin = QSpinBox()
        self.magszam_spin.setRange(1, 1000000000)
        self.magszam_spin.setValue(self.process['MAGSZAM'])
        layout.addWidget(QLabel("Magszám:"))
        layout.addWidget(self.magszam_spin)
        
        self.memoriaszam_spin = QSpinBox()
        self.memoriaszam_spin.setRange(1, 1000000000)
        self.memoriaszam_spin.setValue(self.process['MEMORIASZAM'])
        layout.addWidget(QLabel("Memória:"))
        layout.addWidget(self.memoriaszam_spin)
        
        self.aktiv_check = QCheckBox("Aktív")
        self.aktiv_check.setChecked(self.process['AKTIV'])
        layout.addWidget(self.aktiv_check)
        
        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_changes)
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_process)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

    def save_changes(self):
        new_name = self.name_edit.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Error", "Process group name cannot be empty!")
            return
            
        # Update process group name if changed
        if new_name != self.process_group_name:
            # Handle name change
            if new_name in self.current_data['FOLYAMATOK']:
                QMessageBox.warning(self, "Error", "Process group name already exists!")
                return
                
            # Move processes to new group name
            self.current_data['FOLYAMATOK'][new_name] = self.current_data['FOLYAMATOK'].pop(self.process_group_name)
            self.process_group_name = new_name

        # Update process data
        self.process.update({
            'SZAMITOGEP': self.computer_combo.currentText(),
            'KOD': self.kod_edit.text(),
            'INDITAS': self.inditas_edit.text(),
            'MAGSZAM': self.magszam_spin.value(),
            'MEMORIASZAM': self.memoriaszam_spin.value(),
            'AKTIV': self.aktiv_check.isChecked()
        })
        
        self.accept()

    def delete_process(self):
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Delete this process?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            # Remove the process from its group
            del self.current_data['FOLYAMATOK'][self.process_group_name][self.process_index]
            
            # Remove group if empty
            if not self.current_data['FOLYAMATOK'][self.process_group_name]:
                del self.current_data['FOLYAMATOK'][self.process_group_name]
            
            self.accept()

class AddComputerDialog(QDialog):
    def __init__(self, parent, current_data):
        super().__init__(parent)
        self.current_data = current_data
        self.setWindowTitle("Add New Computer")
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Computer name
        self.name_edit = QLineEdit()
        layout.addWidget(QLabel("Computer Name:"))
        layout.addWidget(self.name_edit)
        
        # Specs
        self.magszam_spin = QSpinBox()
        self.magszam_spin.setRange(1, 1000000000)
        self.magszam_spin.setValue(1)
        layout.addWidget(QLabel("Magszám:"))
        layout.addWidget(self.magszam_spin)
        
        self.memoriaszam_spin = QSpinBox()
        self.memoriaszam_spin.setRange(1, 1000000000)
        self.memoriaszam_spin.setValue(1)
        layout.addWidget(QLabel("Memória egységek:"))
        layout.addWidget(self.memoriaszam_spin)
        
        # Buttons
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_computer)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

    def add_computer(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Computer name cannot be empty!")
            return
            
        if name in self.current_data['SZAMITOGEPEK']:
            QMessageBox.warning(self, "Error", "Computer name already exists!")
            return
            
        self.current_data['SZAMITOGEPEK'][name] = {
            'MAGSZAM': self.magszam_spin.value(),
            'MEMORIASZAM': self.memoriaszam_spin.value()
        }
        
        self.accept()

class AddProcessDialog(QDialog):
    def __init__(self, parent, current_data):
        super().__init__(parent)
        self.current_data = current_data
        self.setWindowTitle("Add New Process")
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Process Group Name
        self.group_edit = QLineEdit()
        self.group_edit.setPlaceholderText("Process group name")
        layout.addWidget(QLabel("Process Group Name:"))
        layout.addWidget(self.group_edit)
        
        # Computer Selection
        self.computer_combo = QComboBox()
        self.computer_combo.addItems(self.current_data['SZAMITOGEPEK'].keys())
        layout.addWidget(QLabel("Computer:"))
        layout.addWidget(self.computer_combo)
        
        # Process Details
        self.kod_edit = QLineEdit()
        self.kod_edit.setPlaceholderText("Unique process code")
        layout.addWidget(QLabel("Kód (unique identifier):"))
        layout.addWidget(self.kod_edit)
        
        self.inditas_spin = QSpinBox()
        self.inditas_spin.setRange(0, 999999)
        layout.addWidget(QLabel("Indítás:"))
        layout.addWidget(self.inditas_spin)
        
        self.magszam_spin = QSpinBox()
        self.magszam_spin.setRange(1, 1000000000)
        self.magszam_spin.setValue(1)
        layout.addWidget(QLabel("Magszám:"))
        layout.addWidget(self.magszam_spin)
        
        self.memoriaszam_spin = QSpinBox()
        self.memoriaszam_spin.setRange(1, 1000000000)
        self.memoriaszam_spin.setValue(1)
        layout.addWidget(QLabel("Memória:"))
        layout.addWidget(self.memoriaszam_spin)
        
        self.aktiv_check = QCheckBox("Aktív")
        self.aktiv_check.setChecked(True)
        layout.addWidget(self.aktiv_check)
        
        # Buttons
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_process)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

    def add_process(self):
        group_name = self.group_edit.text().strip()
        kod = self.kod_edit.text().strip()
        
        if not group_name:
            QMessageBox.warning(self, "Error", "Process group name cannot be empty!")
            return
            
        if not kod:
            QMessageBox.warning(self, "Error", "Kód cannot be empty!")
            return
            
        # Check for duplicate Kód in the group
        if group_name in self.current_data['FOLYAMATOK']:
            existing_kods = {p['KOD'] for p in self.current_data['FOLYAMATOK'][group_name]}
            if kod in existing_kods:
                QMessageBox.warning(self, "Error", "Kód must be unique within the group!")
                return

        new_process = {
            'SZAMITOGEP': self.computer_combo.currentText(),
            'KOD': kod,
            'INDITAS': self.inditas_spin.value(),
            'MAGSZAM': self.magszam_spin.value(),
            'MEMORIASZAM': self.memoriaszam_spin.value(),
            'AKTIV': self.aktiv_check.isChecked()
        }
        
        # Add to data structure
        if group_name not in self.current_data['FOLYAMATOK']:
            self.current_data['FOLYAMATOK'][group_name] = []
            
        self.current_data['FOLYAMATOK'][group_name].append(new_process)
        self.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ELZ GUI")
        self.setGeometry(500, 100, 1200, 800)
        self.setMinimumSize(1200, 800)

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
        path = self.MP_path_input.text().strip()
        if path:
            try:
                self.current_data = read_dir(path)
                self.stacked_widget.setCurrentIndex(1)
                self.AP_subtitle.setText(path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load directory: {str(e)}")    
    
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
        
        

        # Add new SZÁMÍTÓGÉP
        new_computer_btn = QPushButton("New computer")
        new_computer_btn.setFixedSize(200, 60)
        new_computer_btn.clicked.connect(self.open_add_computer_page) 

        monitoring_layout.addLayout(self.get_h_centered_layout(new_computer_btn))

        # Add new FOLYAMAT
        new_process_btn = QPushButton("New process")
        new_process_btn.setFixedSize(200, 60)
        new_process_btn.clicked.connect(self.open_add_process_page)

        monitoring_layout.addLayout(self.get_h_centered_layout(new_process_btn))

        # Return button
        return_btn = QPushButton("Return to actions page")
        return_btn.setFixedSize(200, 60)
        return_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        monitoring_layout.addLayout(self.get_h_centered_layout(return_btn))

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
            data = self.current_data
            
            # Group processes by computer
            computer_processes = defaultdict(list)
            for process_group in data['FOLYAMATOK'].keys():
                for process in data['FOLYAMATOK'][process_group]:
                    computer_name = process['SZAMITOGEP']
                    process['NEV'] = process_group
                    computer_processes[computer_name].append(process)
            
            # Create computer sections
            for computer_name, specs in data['SZAMITOGEPEK'].items():
                computer_group = QGroupBox(f"{computer_name}")
                computer_layout = QVBoxLayout()
                
                # Computer specs
                specs_layout = QHBoxLayout()
                comp_edit_btn = QPushButton("Edit computer")
                comp_edit_btn.clicked.connect(lambda _, cn=computer_name: self.open_edit_computer_page(cn))
                specs_layout.addWidget(comp_edit_btn)
                specs_layout.addWidget(QLabel(f"Magszám: {specs['MAGSZAM']}"))
                specs_layout.addWidget(QLabel(f"Memória egységek: {specs['MEMORIASZAM']}"))
                specs_layout.addStretch()
                
                computer_layout.addLayout(specs_layout)
                
                # Processes for this computer
                processes = computer_processes.get(computer_name, [])
                for process in processes:
                    
                    # Getting the process index
                    i = -1
                    for p in self.current_data['FOLYAMATOK'][process['NEV']]:
                        i += 1
                        if p['KOD'] == process['KOD']:
                            break

                    process_frame = QFrame()
                    process_frame.setFrameShape(QFrame.Box)
                    process_frame.setLineWidth(1)
                    
                    process_layout = QHBoxLayout()
                    process_layout.addWidget(QLabel(f"{process['NEV']}"))
                    pro_edit_btn = QPushButton("Edit")
                    pro_edit_btn.clicked.connect(lambda _, pg=process['NEV'], idx=i: self.open_edit_process_page(pg, idx))
                    process_layout.addWidget(pro_edit_btn)

                    process_layout.addWidget(QLabel(f"Kód: {process['KOD']}  |"))
                    process_layout.addWidget(QLabel(f"Indítás: {process['INDITAS']}  |"))
                    process_layout.addWidget(QLabel(f"Magszám: {process['MAGSZAM']}  |"))
                    process_layout.addWidget(QLabel(f"Memória: {process['MEMORIASZAM']} MB  |"))
                    process_layout.addWidget(QLabel("Aktív" if process['AKTIV'] else "Inaktív"))
                    process_layout.addStretch()
                    
                    process_frame.setLayout(process_layout)
                    computer_layout.addWidget(process_frame)
                
                computer_group.setLayout(computer_layout)
                self.scroll_layout.addWidget(computer_group)
            
            self.scroll_layout.addStretch()
        
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def open_edit_computer_page(self, computer_name):
        if computer_name not in self.current_data['SZAMITOGEPEK']:
            return
            
        dialog = EditComputerDialog(self, computer_name, self.current_data)
        if dialog.exec():
            # Refresh monitoring page after changes
            self.open_monitoring_page()
            # Save changes to file as well
            try:
                write_dir(self.MP_path_input.text().strip(), self.current_data)
            except Exception as e:
                print(f"Error! Failed to save new computer: {str(e)}")

    def open_edit_process_page(self, process_group_name, process_index):
        if process_group_name not in self.current_data['FOLYAMATOK']:
            return
        if process_index >= len(self.current_data['FOLYAMATOK'][process_group_name]):
            return
            
        dialog = EditProcessDialog(
            self,
            process_group_name,
            process_index,
            self.current_data
        )
        if dialog.exec():
            self.open_monitoring_page()

            try:
                write_dir(self.MP_path_input.text().strip(), self.current_data)
            except Exception as e:
                print(f"Error! Failed to save new computer: {str(e)}")
    def open_add_computer_page(self):
        dialog = AddComputerDialog(self, self.current_data)
        if dialog.exec():
            self.open_monitoring_page()
            try:
                write_dir(self.MP_path_input.text().strip(), self.current_data)
            except Exception as e:
                print(f"Error! Failed to save new computer: {str(e)}")
    def open_add_process_page(self):
        if not self.current_data['SZAMITOGEPEK']:
            QMessageBox.warning(self, "Error", "No computers available! Create a computer first.")
            return
            
        dialog = AddProcessDialog(self, self.current_data)
        if dialog.exec():
            self.open_monitoring_page()
            try:
                write_dir(self.MP_path_input.text().strip(), self.current_data)
            except Exception as e:
                print(f"Error! Failed to save new computer: {str(e)}")


if __name__ == '__main__':
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec()