# coding:utf-8
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QPushButton, QLineEdit, QComboBox, QFileDialog
from qfluentwidgets import FluentIcon, setFont, InfoBarIcon
from PySide6.QtCore import QTimer
from pathlib import Path
import os
from Wplace.find_last_png import find_last_one

from sub.home_ui import Ui_Form


class HomeInterface(Ui_Form, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        # Ensure the widget has a layout
        self.setLayout(QVBoxLayout())

        # Initialize layout and components
        self.image_labels = {}
        self.init_toolbar()
        self.init_image_windows()

        # Timer for periodic updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_images)
        self.timer.start(1000)  # Update every 1 second

    def init_toolbar(self):
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

        self.run_button = QPushButton("运行 EXE", self)
        self.run_button.clicked.connect(self.run_selected_exe)
        toolbar_layout.addWidget(self.run_button)

        self.layout().addLayout(toolbar_layout)

    def init_image_windows(self):
        self.image_layout = QGridLayout()
        self.layout().addLayout(self.image_layout)

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
            label.setFixedSize(200, 150)
            layout.addWidget(label)

            caption = QLabel(name)
            layout.addWidget(caption)

            widget.setLayout(layout)
            self.image_layout.addWidget(widget, *pos)

            self.image_labels[name] = label

    def update_images(self):
        base_folder = Path(self.base_folder_input.text())

        folders_and_patterns = {
            "timeline_cropped": {"folder": base_folder / 'timeline_cropped_png', "pattern": r'^\d{8}_\d{6}\.png$'},
            "timeline_color_finish": {"folder": base_folder / 'timeline_color', "pattern": r'^finish_all_\d{8}_\d{6}\.png$'},
            "timeline_color_mask": {"folder": base_folder / 'timeline_color', "pattern": r'^mask_all_\d{8}_\d{6}\.png$'},
            "timeline_color_todo": {"folder": base_folder / 'timeline_color', "pattern": r'^todo_all_\d{8}_\d{6}\.png$'}
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

    def run_selected_exe(self):
        exe_name = self.exe_dropdown.currentText()
        base_folder = Path(self.base_folder_input.text())
        exe_paths = {
            "main.exe": f"{base_folder}/main.exe",
            "image_process.exe": f"{base_folder}/image_process.exe",
            "config_GUI.exe": f"{base_folder}/config_GUI.exe"
        }

        exe_path = exe_paths.get(exe_name)
        if exe_path and os.path.exists(exe_path):
            os.startfile(exe_path)
        else:
            print(f"Executable not found: {exe_path}")
