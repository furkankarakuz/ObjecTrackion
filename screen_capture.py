from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
from ultralytics import YOLO
from telegram_process import bot
import numpy as np
import pyautogui
import torch
import cv2
import asyncio
import logging
import time


device = torch.device('cpu')
model = YOLO("yolov8s.pt", verbose=False)


model.to(device)
loop = asyncio.get_event_loop()

logging.getLogger("ultralytics").setLevel(logging.CRITICAL)
logging.getLogger("telegram").setLevel(logging.CRITICAL)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", filename="app.log", filemode="a")


class ScreenCaptureThread(QThread):
    update_frame = pyqtSignal(QImage)

    def __init__(self, region: int, width: int, height: int, fps: int, objects: list, message: str, notif_check: bool) -> None:
        """ScreenCaptureThread

        Initialize TelegramBot ScreenCaptureThread

        Args:
            region (int): Region Value for Screen Capture
            width (int): Width Value for Screen Capture
            height (int): Height Value for Screen Capture
            fps (int): FPS Value for Screen Capture
            objects (list): Filter Objects
            message (str): Message Text
            notif_check (bool): Notification Check
        """
        super(ScreenCaptureThread, self).__init__(None)
        self.region = region
        self.width = width
        self.height = height
        self.fps = fps
        self.objects = objects
        self.message = message
        self.notif_check = notif_check
        self.running = False
        self.start_time = time.time()
        self.interval = 30

        self.new_allowed_count = {key: {"current_value": 0, "max_value": 0} for key in self.objects}

    def run(self) -> None:
        """Run

        This method, does screen sharing
        """
        self.running = True
        self.qt_img = None
        while self.running:
            frame = self.get_screen_frame(self.region)
            frame = cv2.resize(frame, (self.width, self.height))
            annotated_frame, _ = self.process_frame(frame)

            rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            self.qt_img = QImage(rgb_frame.data, w, h, ch * w, QImage.Format_RGB888)
            self.update_frame.emit(self.qt_img)

            if self.fps > 0:
                self.msleep(int(1000 / self.fps))

    def stop(self) -> None:
        """STOP

        This method, stops screen sharing
        """
        self.running = False
        self.wait()

    @staticmethod
    def get_screen_frame(region: tuple[int, int, int, int]) -> cv2.typing.MatLike:
        """Get Screen Frame

        This method, gets screen for frame with OpenCV

        Args:
            region (tuple[int, int, int, int]): X, y, width and height of Screen Sharing

        Returns:
            MatLike: Converts a color (BGR) image to grayscale format.
        """
        screenshot = pyautogui.screenshot(region=region)
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2RGB)

    def process_frame(self, frame: cv2.typing.MatLike) -> tuple[None, list]:
        """Process Frame

        This method, detects the filtered object and sends a notification message on telegram if you want.

        Args:
            frame (_type_): Frame

        Returns:
            tuple[None, list]: Frame and Results
        """
        results = model(frame)
        names = model.names

        filtered_boxes = [box for box in results[0].boxes if names[int(box.cls)] in self.objects]
        self.new_allowed_count = {key: {"current_value": 0, "max_value": self.new_allowed_count[key]["max_value"]} for key in self.objects}

        for box in filtered_boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_name = names[int(box.cls)]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
            cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            self.new_allowed_count[class_name]["current_value"] += 1

        for class_name in self.objects:
            if self.new_allowed_count[class_name]["current_value"] > 0:
                current_time = time.time()
                if (current_time - self.start_time >= self.interval or self.new_allowed_count[class_name]["current_value"] > self.new_allowed_count[class_name]["max_value"]) and (self.qt_img is not None):
                    if self.notif_check:
                        self.start_time = time.time()
                        self.qt_img.save("image.png")
                        loop.run_until_complete(bot.send_message(self.message, "image.png"))
                    self.new_allowed_count[class_name]["max_value"] = self.new_allowed_count[class_name]["current_value"]
                logging.info(self.new_allowed_count)

        return frame, results
