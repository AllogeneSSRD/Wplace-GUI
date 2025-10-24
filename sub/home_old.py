from pathlib import Path
from Wplace.find_last_png import find_last_one, find_color
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QPushButton, QLineEdit, QComboBox, QFileDialog, QScrollArea
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
import os
import subprocess

from PySide6 import QtCore, QtGui, QtWidgets


class HomeInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

    def setupUi(self, HomeInterface):
        # Main layout
        HomeInterface.setObjectName("FocusInterface")
        self.central_widget = QWidget()
        # self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Toolbar
        self.create_toolbar()

        # Image display area
        self.image_layout = QGridLayout()
        self.main_layout.addLayout(self.image_layout)

        self.image_labels = {}
        HomeInterface.setup_image_windows()

        # Timer for periodic updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_images)
        self.timer.start(1000)  # Update every 1 second

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
        self.exe_dropdown.addItems(["main.exe", "image_process.exe", "config_GUI.exe"])
        toolbar_layout.addWidget(self.exe_dropdown)

        # self.run_button = QPushButton("运行 EXE", self)
        # self.run_button.clicked.connect(self.run_selected_exe)
        # toolbar_layout.addWidget(self.run_button)

        # Switch interface button
        # self.switch_button = QPushButton("查看单色mask", self)
        # self.switch_button.clicked.connect(self.switch_interface)
        # toolbar_layout.addWidget(self.switch_button)

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
            # layout.setSpacing(20)  # Increase spacing between elements

            label = QLabel("No Image")
            label.setStyleSheet("background-color: lightgray; border: 1px solid black;")
            label.setFixedSize(300, 225)  # Placeholder size
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
            "timeline_color_todo": {"folder": base_folder / 'timeline_color', "pattern": r'^todo_all_(\d{8})_(\d{6}).png$'}
        }

        # Handle template separately
        template_path = base_folder / 'template.png'
        if template_path.exists():
            pixmap = QPixmap(str(template_path))
            template_label = self.image_labels["template"]
            template_label.setPixmap(pixmap.scaled(template_label.size().width(), template_label.size().height()))

            # Adjust child window sizes based on template aspect ratio
            aspect_ratio = pixmap.width() / pixmap.height()
            new_width = int(225 * aspect_ratio)
            new_height = 225

            for name in ["timeline_color_finish", "timeline_color_mask", "timeline_color_todo", "template"]:
                label = self.image_labels[name]
                label.setFixedSize(new_width, new_height)

            # Set timeline_cropped to be twice the size of other windows
            timeline_cropped_label = self.image_labels["timeline_cropped"]
            timeline_cropped_label.setFixedSize(new_width * 2, new_height * 2)

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