import threading
from watchdog.observers import Observer

from Wplace.config import ConfigHandler
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QGroupBox, QScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence
import yaml

config_path = 'config.yaml'


class ConfigEditor(QMainWindow):
    def __init__(self, config_path):
        super().__init__()
        self.config_path = config_path
        self.setWindowTitle("Config Editor")
        self.resize(600, 400)

        # Load config
        self.config_data = self.load_config()
        self.temp_data = self.config_data.copy()

        # Use a scroll area for better navigation
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.central_widget = QWidget()
        scroll_area.setWidget(self.central_widget)
        self.setCentralWidget(scroll_area)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Display config parameters with nested support
        self.input_fields = {}
        self.display_config(self.config_data, self.layout)

        # Buttons
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_config)
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_config)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.reset_button)

        # Enable undo/redo for input fields
        for input_field in self.input_fields.values():
            input_field.setUpdatesEnabled(True)

    def load_config(self):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def save_config(self):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(self.temp_data, f)
        self.config_data = self.temp_data.copy()

    def reset_config(self):
        example_path = 'config_example.yaml'
        with open(example_path, 'r', encoding='utf-8') as f:
            self.temp_data = yaml.safe_load(f)
        for key, value in self.temp_data.items():
            self.input_fields[key].setText(str(value))

    def display_config(self, config, parent_layout, prefix=""):
        for key, value in config.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                group_box = QGroupBox(key)
                group_layout = QVBoxLayout()
                group_box.setLayout(group_layout)
                parent_layout.addWidget(group_box)
                self.display_config(value, group_layout, full_key)
            else:
                label = QLabel(key)
                input_field = QLineEdit(str(value))
                input_field.setMinimumWidth(300)  # Set appropriate size
                input_field.textChanged.connect(lambda text, k=full_key: self.update_temp_data(k, text))
                parent_layout.addWidget(label)
                parent_layout.addWidget(input_field)
                self.input_fields[full_key] = input_field

    def update_temp_data(self, key, text):
        keys = key.split('.')
        temp = self.temp_data
        for k in keys[:-1]:
            temp = temp.setdefault(k, {})
        try:
            temp[keys[-1]] = eval(text)  # Convert to Python type if possible
        except:
            temp[keys[-1]] = text

    def keyPressEvent(self, event):
        # Capture Ctrl+Z for undo and Ctrl+Y for redo
        if event.matches(QKeySequence.Undo):
            print("Undo key detected")
            focused_widget = self.focusWidget()
            if isinstance(focused_widget, QLineEdit):
                focused_widget.undo()
                print("Undo performed")
        elif event.matches(QKeySequence.Redo):
            print("Redo key detected")
            focused_widget = self.focusWidget()
            if isinstance(focused_widget, QLineEdit):
                focused_widget.redo()
                print("Redo performed")
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    reload_event = threading.Event()
    cfg = ConfigHandler(config_path, reload_event)
    observer = Observer()
    observer.schedule(cfg, path='.', recursive=False)
    observer.start()

    app = QApplication([])
    editor = ConfigEditor('config.yaml')
    editor.show()
    app.exec()
