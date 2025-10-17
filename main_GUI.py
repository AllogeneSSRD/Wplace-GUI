from pathlib import Path
from Wplace.find_last_png import find_last_one, find_color
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QPushButton, QLineEdit, QComboBox, QFileDialog, QScrollArea
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
import os
import subprocess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer GUI")

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Toolbar
        self.create_toolbar()

        # Image display area
        self.image_layout = QGridLayout()
        self.main_layout.addLayout(self.image_layout)

        self.image_labels = {}
        self.setup_image_windows()

        # Timer for periodic updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_images)
        self.timer.start(5000)  # Update every 5 seconds

    def create_toolbar(self):
        toolbar_layout = QHBoxLayout()

        # Base folder input
        self.base_folder_input = QLineEdit(self)
        self.base_folder_input.setPlaceholderText("Enter base folder path")
        toolbar_layout.addWidget(self.base_folder_input)

        self.load_button = QPushButton("Reload Base Folder", self)
        self.load_button.clicked.connect(self.reload_base_folder)
        toolbar_layout.addWidget(self.load_button)

        # Dropdown for exe selection
        self.exe_dropdown = QComboBox(self)
        self.exe_dropdown.addItems(["main_exe", "image_process_exe", "config_GUI_exe"])
        toolbar_layout.addWidget(self.exe_dropdown)

        self.run_button = QPushButton("Run EXE", self)
        self.run_button.clicked.connect(self.run_selected_exe)
        toolbar_layout.addWidget(self.run_button)

        # Switch interface button
        self.switch_button = QPushButton("Switch Interface", self)
        self.switch_button.clicked.connect(self.switch_interface)
        toolbar_layout.addWidget(self.switch_button)

        self.main_layout.addLayout(toolbar_layout)

    def setup_image_windows(self):
        # Define positions and labels
        positions = {
            "timeline_cropped": (0, 0, 2, 2),
            "timeline_color_finish": (0, 2, 1, 1),
            "timeline_color_mask": (1, 2, 1, 1),
            "template": (2, 0, 1, 1),
            "timeline_color_todo": (2, 1, 1, 1)
        }

        for name, pos in positions.items():
            widget = QWidget()
            layout = QVBoxLayout()

            label = QLabel("No Image")
            label.setStyleSheet("background-color: lightgray; border: 1px solid black;")
            label.setFixedSize(200, 200)  # Placeholder size
            layout.addWidget(label)

            caption = QLabel(name)
            layout.addWidget(caption)

            widget.setLayout(layout)
            self.image_layout.addWidget(widget, *pos)

            self.image_labels[name] = label

    def update_images(self):
        # Use the find_last_one function to get the latest image paths
        base_folder = Path(self.base_folder_input.text())

        # Define folders and patterns
        folders_and_patterns = {
            "timeline_cropped": {"folder": base_folder / 'timeline_cropped_png', "pattern": r'^(\d{8})_(\d{6}).png$'},
            "timeline_color_finish": {"folder": base_folder / 'timeline_color', "pattern": r'^finish_all_(\d{8})_(\d{6}).png$'},
            "timeline_color_mask": {"folder": base_folder / 'timeline_color', "pattern": r'^mask_all_(\d{8})_(\d{6}).png$'},
            # "template": {"folder": base_folder, "pattern": r'template.png'},
            "timeline_color_todo": {"folder": base_folder / 'timeline_color', "pattern": r'^todo_all_(\d{8})_(\d{6}).png$'}
        }

        for name, config in folders_and_patterns.items():
            folder = str(config["folder"].resolve())
            pattern = config["pattern"]
            image_path = find_last_one(folder, pattern)
            label = self.image_labels[name]

            if image_path and os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                label.setPixmap(pixmap.scaled(label.size().width(), label.size().height()))
            else:
                label.clear()
                label.setText("No Image")

    def reload_base_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Base Folder")
        if folder:
            self.base_folder_input.setText(folder)
            # Add logic to reload base folder

    def run_selected_exe(self):
        exe_name = self.exe_dropdown.currentText()
        exe_path = f"path/to/{exe_name}.exe"  # Replace with actual paths
        if os.path.exists(exe_path):
            subprocess.Popen(exe_path, shell=True)

    def switch_interface(self):
        # Placeholder for switching interface logic
        print("Switching interface")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
