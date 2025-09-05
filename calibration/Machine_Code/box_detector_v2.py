import cv2
import numpy as np
import os
from skimage.metrics import structural_similarity as compare_ssim # type: ignore
import time


class BoxDetector:
    def __init__(self, camera_index=0, ref_path="/home/pi/Automatic_Pipeting_Machine/reference_images/All.png"):
        self.blocks = {
             "Tip Box": (25, 45, 200, 120),
        "Reagent Box": (10, 235, 200, 100),
        "Plate Box": (270, 140, 120, 170),
        "Ejection Box": (430, 30, 170, 290)
        }
        self.thresholds = {
            "Tip Box": 0.75,
            "Reagent Box": 0.7,
            "Plate Box": 0.7,
            "Ejection Box": 0.6
        }
        self.ref_path = ref_path
        self.camera_index = camera_index
        self.reference_rois = {}
        self.cap = None
        self._load_reference_image()

    def _preprocess(self, gray_img):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return clahe.apply(gray_img)

    def _is_box_present(self, current_roi, reference_roi, threshold):
        gray_cur = self._preprocess(cv2.cvtColor(current_roi, cv2.COLOR_BGR2GRAY))
        gray_ref = self._preprocess(cv2.cvtColor(reference_roi, cv2.COLOR_BGR2GRAY))
        gray_cur = cv2.resize(gray_cur, (gray_ref.shape[1], gray_ref.shape[0]))
        score, _ = compare_ssim(gray_cur, gray_ref, full=True)
        return score > threshold, score

    def _load_reference_image(self):
        if not os.path.exists(self.ref_path):
            raise FileNotFoundError(f"Reference image not found: {self.ref_path}")
        full_reference = cv2.imread(self.ref_path)
        if full_reference is None:
            raise IOError("Failed to read reference image.")
        for name, (x, y, w, h) in self.blocks.items():
            self.reference_rois[name] = full_reference[y:y+h, x:x+w]
    
    def save_img_before_use():
        return 0

    

    def detect_once(self, show_feed=False):
        self.cap = cv2.VideoCapture(self.camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera.")
        
        for _ in range(5):
            self.cap.read()
            time.sleep(0.3)

        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to grab frame.")

        missing_boxes = []
        results = {}

        for name, (x, y, w, h) in self.blocks.items():
            roi = frame[y:y+h, x:x+w]
            present, score = self._is_box_present(roi, self.reference_rois[name], self.thresholds[name])
            results[name] = (present, score)
            if not present:
                missing_boxes.append(name)

            if show_feed:
                color = (0, 255, 0) if present else (0, 0, 255)
                label = f"{name}: {'Y' if present else 'N'} ({score:.2f})"
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, label, (x, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        if show_feed:
            cv2.imshow("Box Detection", frame)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()

        self.cap.release()
        all_present = len(missing_boxes) == 0
        return 5 if all_present else len(missing_boxes), missing_boxes, results



# x = BoxDetector()
# x.detect_once(True)