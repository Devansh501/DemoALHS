from PyQt5.QtCore import QThread, pyqtSignal
from .box_detector_v2 import BoxDetector
import time

class BoxDetectionThread(QThread):
    detection_result = pyqtSignal(int, list)  # status_code, missing_boxes

    def __init__(self, parent=None, interval=1):
        super().__init__(parent)
        self.detector = BoxDetector()
        self._running = True
        self.interval = interval  # seconds between retries

    def run(self):
        if self._running: # while 
            status, missing, _ = self.detector.detect_once()
            self.detection_result.emit(status, missing)
            # if status == 5:
            #     break
            time.sleep(self.interval)

    def stop(self):
        self._running = False

    def show_screen(self):
        self.detector.detect_once(True)


# detection = BoxDetectionThread()
# detection.show_screen()