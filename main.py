from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QLabel, QSpinBox, QDialog, QHBoxLayout, QGridLayout, QLineEdit, QTextEdit, QCheckBox
from screen_capture import ScreenCaptureThread
from screen_process import get_size
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys


class MainDialog(QDialog):
    def __init__(self):
        super(MainDialog, self).__init__(None)

        """MainDialog

        Initialize Desktop App
        """

        self.size = get_size()
        h_box = QHBoxLayout()

        self.image = QLabel("Screen")
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setStyleSheet("border: 1px solid black;font-size: 50px;")
        self.image.setScaledContents(True)
        h_box.addWidget(self.image, 10)

        self.width_spin = QSpinBox()
        self.width_spin.setRange(1024, 7680)
        self.width_spin.setValue(self.size[0])

        self.height_spin = QSpinBox()
        self.height_spin.setRange(600, 4320)
        self.height_spin.setValue(self.size[1])

        self.fps_spin = QSpinBox()
        self.fps_spin.setRange(1, 60)
        self.fps_spin.setValue(30)

        self.start_button = QPushButton("Start", clicked=self.start_capture)
        self.stop_button = QPushButton("Stop", clicked=self.stop_capture)
        self.stop_button.setEnabled(False)

        self.object_list = QLineEdit()
        self.object_list.setPlaceholderText("person,car")

        self.message = QTextEdit()
        self.message.setText("Test Message")

        self.active_message = QCheckBox("Active Notification Message")

        v_box = QVBoxLayout()
        v_box.addStretch()

        grid = QGridLayout()
        grid.addWidget(QLabel("Width Spin : "), 0, 0)
        grid.addWidget(self.width_spin, 0, 1)
        grid.addWidget(QLabel("Height Spin : "), 1, 0)
        grid.addWidget(self.height_spin, 1, 1)
        grid.addWidget(QLabel("FPS Value : "), 2, 0)
        grid.addWidget(self.fps_spin, 2, 1)
        grid.addWidget(QLabel("Select Objects : "), 3, 0, 1, 2)
        grid.addWidget(self.object_list, 4, 0, 1, 2)
        grid.addWidget(QLabel("Notif Message : "), 5, 0, 1, 2)
        grid.addWidget(self.message, 6, 0, 1, 2)
        grid.addWidget(self.active_message, 7, 0, 1, 2)
        grid.addWidget(self.start_button, 8, 0, 1, 2)
        grid.addWidget(self.stop_button, 9, 0, 1, 2)

        v_box.addLayout(grid)
        v_box.addStretch()

        h_box.addLayout(v_box)

        self.setLayout(h_box)
        self.setWindowTitle("Desktop APP")

        self.showMaximized()
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.show()

    def start_capture(self) -> None:
        """Start Capture

        This method, starts screen capture
        """
        self.update_buttons()
        width, height = self.width_spin.value(), self.height_spin.value()
        region = (0, 0, width, height)
        fps = self.fps_spin.value()

        self.capture_thread = ScreenCaptureThread(region, width, height, fps, self.object_list.text().split(","), self.message.toPlainText(), self.active_message.isChecked())
        self.capture_thread.update_frame.connect(self.update_image)
        self.capture_thread.start()

    def stop_capture(self) -> None:
        """Stop Capture

        This method, stops screen capture
        """
        self.update_buttons()
        if self.capture_thread is not None and self.capture_thread.isRunning():
            self.close_capture()

    def update_image(self, qt_image: Qt.QImage) -> None:
        """Update Image

        This method, updates image in the QLabel

        Args:
            qt_image (QImage): Image object for Qt
        """
        self.image.setPixmap(QPixmap.fromImage(qt_image))

    def update_buttons(self) -> None:
        """Update Buttons

        This method updates the activation of the buttons
        """
        self.start_button.setEnabled(not self.start_button.isEnabled())
        self.stop_button.setEnabled(not self.start_button.isEnabled())

    def close_capture(self) -> None:
        """Close Capture

        This method, closes screen captures
        """
        self.capture_thread.stop()
        self.capture_thread.update_frame.disconnect(self.update_image)
        self.capture_thread = None
        self.image.clear()


app = QApplication(sys.argv)
window = MainDialog()
sys.exit(app.exec())
