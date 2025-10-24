from pathlib import Path

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QPushButton, QLineEdit, QFileDialog, QScrollArea
from PySide6.QtCore import QTimer, Qt

from qfluentwidgets import ScrollArea

from Wplace.find_last_png import find_color

from sub.mask_ui import Ui_Form

class MaskInterface(Ui_Form, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        # Ensure the widget has a layout
        self.setLayout(QVBoxLayout())

        self.init_toolbar()

        # Initialize scroll area for displaying images
        self.scroll_area = ScrollArea(self)
        self.scroll_widget = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        # Timer for periodic updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_images)
        self.timer.start(60000)  # Update every 60 seconds

        # Load and display images
        self.load_images()

    def init_toolbar(self):
        toolbar_layout = QHBoxLayout()

        # Base folder input
        self.base_folder_input = QLineEdit(self)
        self.base_folder_input.setPlaceholderText("Enter base folder path")
        toolbar_layout.addWidget(self.base_folder_input)

        self.load_button = QPushButton("Reload Base Folder", self)
        self.load_button.clicked.connect(self.reload_base_folder)
        toolbar_layout.addWidget(self.load_button)

        self.layout.addLayout(toolbar_layout)

    def reload_base_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Base Folder")
        if folder:
            self.base_folder_input.setText(folder)
            self.load_images()  # Reload images after changing the directory

    def load_images(self):
        base_folder = Path(self.base_folder_input.text())
        if not base_folder.exists():
            print("Base folder does not exist:", base_folder)
            return

        timeline_color_folder = base_folder / 'timeline_color'
        if not timeline_color_folder.exists():
            print("Timeline color folder does not exist:", timeline_color_folder)
            return

        timeline_color_list = find_color(timeline_color_folder, r'^_mask_#(\d{2}).*.png$')
        print("Loading images from:", timeline_color_folder)
        print("Found images:", len(timeline_color_list))

        template_path = base_folder / 'template.png'
        if template_path.exists():
            pixmap = QPixmap(str(template_path))
            aspect_ratio = pixmap.width() / pixmap.height()
            new_width = int(180 * aspect_ratio)
            new_height = 180
        else:
            print("Template image not found at:", template_path)
            new_width = 200
            new_height = 150

        # Clear the previous layout
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        if not timeline_color_list:
            print("No images found in timeline_color folder.")
            empty_label = QLabel("No images to display.")
            empty_label.setAlignment(Qt.AlignCenter)
            self.scroll_layout.addWidget(empty_label)
            self.scroll_widget.adjustSize()
            self.scroll_area.update()
            return

        # Populate the grid with images and labels
        for index, image_path in enumerate(timeline_color_list):
            if not Path(image_path).exists():
                print("Image does not exist:", image_path)
                continue

            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                print("Failed to load image:", image_path)
                continue

            image_label = QLabel()
            image_label.setPixmap(pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio))  # Scale images to adjusted size
            caption_label = QLabel(Path(image_path).name)

            row = index // 4
            col = index % 4
            self.scroll_layout.addWidget(image_label, row * 2, col)
            self.scroll_layout.addWidget(caption_label, row * 2 + 1, col)

        self.scroll_widget.adjustSize()
        self.scroll_area.update()
        print("Images successfully loaded and displayed.")
