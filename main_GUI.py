import threading
from watchdog.observers import Observer

from Wplace.config import ConfigHandler
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
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

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Display config parameters
        self.input_fields = {}
        for key, value in self.config_data.items():
            label = QLabel(key)
            input_field = QLineEdit(str(value))
            input_field.textChanged.connect(lambda text, k=key: self.update_temp_data(k, text))
            self.layout.addWidget(label)
            self.layout.addWidget(input_field)
            self.input_fields[key] = input_field

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

    def update_temp_data(self, key, text):
        try:
            self.temp_data[key] = eval(text)  # Convert to Python type if possible
        except:
            self.temp_data[key] = text

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
