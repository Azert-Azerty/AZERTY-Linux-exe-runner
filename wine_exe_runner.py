import sys
import os
import shutil
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QFileDialog, QLabel, QTabWidget, QMessageBox)


def check_dependencies():
    """
    Check all necessary requirements for the application
    
    Returns:
        tuple: (bool, str) - Check status, and error message if any
    """
    # List of dependencies to check
    dependencies = [
        ('wine', 'Wine'),
        ('python3', 'Python 3'),
        ('pip', 'Pip'),
        ('update-desktop-database', 'Update Desktop Database')
    ]
    
    missing_deps = []
    
    for cmd, name in dependencies:
        if not shutil.which(cmd):
            missing_deps.append(name)
    
    # Check PyQt5 availability
    try:
        import PyQt5
    except ImportError:
        missing_deps.append('PyQt5')
    
    # If there are missing dependencies
    if missing_deps:
        error_message = "The following requirements are missing:\n" + "\n".join(missing_deps)
        return False, error_message
    
    return True, ""

class WineExeRunner(QWidget):
    def __init__(self):
        super().__init__()
        
        # Check requirements before running the application
        dependencies_ok, error_message = check_dependencies()
        if not dependencies_ok:
            # Create message box with button to open requirements
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("Dependencies Error")
            msg_box.setText(error_message)
            
            # Add button to open requirements file
            open_req_button = msg_box.addButton("Open Requirements File", QMessageBox.ActionRole)
            cancel_button = msg_box.addButton(QMessageBox.Cancel)
            
            # Execute message box
            msg_box.exec_()
            
            # Check which button was pressed
            if msg_box.clickedButton() == open_req_button:
                # Open requirements file
                requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
                
                # Try to open file using system default
                try:
                    if sys.platform.startswith('darwin'):
                        subprocess.run(['open', requirements_path], check=True)
                    elif sys.platform.startswith('win'):
                        os.startfile(requirements_path)
                    else:  # linux
                        subprocess.run(['xdg-open', requirements_path], check=True)
                except Exception as e:
                    QMessageBox.warning(None, "Error", f"Could not open requirements file: {str(e)}")
            
            # Exit the program
            sys.exit(1)
        
        self.initUI()

    def initUI(self):
        # Set title and size
        self.setWindowTitle('AZERTY EXE Runner')
        self.setGeometry(300, 300, 600, 300)
        
        # Create main tab
        self.tabs = QTabWidget()
        
        # Create tabs
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        
        # Add tabs
        self.tabs.addTab(self.tab1, "Downloads EXE")
        self.tabs.addTab(self.tab2, "Wine 32bit Apps")
        
        # Setup first tab
        self.setup_first_tab()
        
        # Setup second tab
        self.setup_second_tab()
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        
        # Set layout
        self.setLayout(main_layout)
    
    def setup_first_tab(self):
        # Create vertical layout for first tab
        layout = QVBoxLayout()
        
        # Create horizontal layout for path and browse button
        path_layout = QHBoxLayout()
        
        # Path input with default path
        self.path_input1 = QLineEdit()
        default_path = os.path.expanduser('~/Downloads')
        self.path_input1.setText(default_path)
        path_layout.addWidget(self.path_input1)
        
        # Browse button
        browse_btn1 = QPushButton('Browse')
        browse_btn1.clicked.connect(lambda: self.browse_file(self.path_input1))
        path_layout.addWidget(browse_btn1)
        
        # Add path layout to main layout
        layout.addLayout(path_layout)
        
        # Run button
        run_btn1 = QPushButton('Run')
        run_btn1.clicked.connect(lambda: self.run_exe(self.path_input1))
        layout.addWidget(run_btn1)
        
        # Result label
        self.result_label1 = QLabel('Results will appear here')
        layout.addWidget(self.result_label1)
        
        # Set layout for first tab
        self.tab1.setLayout(layout)
    
    def setup_second_tab(self):
        # Create vertical layout for second tab
        layout = QVBoxLayout()
        
        # Create horizontal layout for path and browse button
        path_layout = QHBoxLayout()
        
        # Path input with default path for Wine 32bit apps
        self.path_input2 = QLineEdit()
        default_path = os.path.expanduser('~/.wine/drive_c/Program Files (x86)')
        self.path_input2.setText(default_path)
        path_layout.addWidget(self.path_input2)
        
        # Browse button
        browse_btn2 = QPushButton('Browse')
        browse_btn2.clicked.connect(lambda: self.browse_file(self.path_input2))
        path_layout.addWidget(browse_btn2)
        
        # Add path layout to main layout
        layout.addLayout(path_layout)
        
        # Create shortcut button
        create_shortcut_btn = QPushButton('Create shortcut in start menu')
        create_shortcut_btn.clicked.connect(self.create_wine_shortcut)
        layout.addWidget(create_shortcut_btn)
        
        # Run button
        run_btn2 = QPushButton('Run')
        run_btn2.clicked.connect(lambda: self.run_exe(self.path_input2))
        layout.addWidget(run_btn2)
        
        # Result label
        self.result_label2 = QLabel('Results will appear here')
        layout.addWidget(self.result_label2)
        
        # Set layout for second tab
        self.tab2.setLayout(layout)
    
    def browse_file(self, path_input):
        # Open file dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            'Choose EXE file', 
            path_input.text(), 
            'Executable Files (*.exe)'
        )
        
        # Update path input with chosen file
        if file_path:
            path_input.setText(file_path)
    
    def create_wine_shortcut(self):
        # Get path from path input
        exe_path = self.path_input2.text()
        
        try:
            # Check if file exists
            if not os.path.exists(exe_path):
                self.result_label2.setText('Error: File not found')
                return
            
            # Extract program name
            program_name = os.path.splitext(os.path.basename(exe_path))[0]
            
            # Path to start menu
            start_menu_path = os.path.expanduser('~/.local/share/applications')
            os.makedirs(start_menu_path, exist_ok=True)
            
            # Path to new shortcut
            shortcut_path = os.path.join(start_menu_path, f'{program_name}_wine.desktop')
            
            # Shortcut content
            shortcut_content = f'''[Desktop Entry]
Name={program_name}
Exec=wine "{exe_path}"
Type=Application
Categories=Wine;
Icon=wine
'''
            
            # Write shortcut
            with open(shortcut_path, 'w') as f:
                f.write(shortcut_content)
            
            # Make shortcut executable
            os.chmod(shortcut_path, 0o755)
            
            # Update desktop database
            subprocess.run(['update-desktop-database', start_menu_path], check=True)
            
            # Show success message
            self.result_label2.setText(f'Shortcut created for {program_name}')
            
            # Show confirmation message
            QMessageBox.information(
                self, 
                'Success', 
                f'Shortcut created for {program_name} in start menu'
            )
        
        except Exception as e:
            self.result_label2.setText(f'Error creating shortcut: {str(e)}')
            
            # Show error message
            QMessageBox.critical(
                self, 
                'Error', 
                f'Error creating shortcut: {str(e)}'
            )
    
    def run_exe(self, path_input):
        # Get path from path input
        exe_path = path_input.text()
        
        try:
            # Check if file exists
            if not os.path.exists(exe_path):
                # Determine result label
                result_label = self.result_label1 if path_input == self.path_input1 else self.result_label2
                result_label.setText('Error: File not found')
                return
            
            # Run file using Wine
            result = subprocess.run(
                ['wine', exe_path], 
                capture_output=True, 
                text=True
            )
            
            # Determine result label
            result_label = self.result_label1 if path_input == self.path_input1 else self.result_label2
            
            # Show result
            if result.returncode == 0:
                result_label.setText('Run successfully')
            else:
                result_label.setText(f'Error running: {result.stderr}')
        
        except Exception as e:
            # Determine result label
            result_label = self.result_label1 if path_input == self.path_input1 else self.result_label2
            result_label.setText(f'Error: {str(e)}')

def main():
    app = QApplication(sys.argv)
    ex = WineExeRunner()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
