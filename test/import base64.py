import base64
import csv
import requests
import cv2
import numpy as np
from datetime import datetime
import os

IMG_PATH = "image.jpg"
API_KEY = os.environ["API_KEY"]
DISTANCE_TO_OBJECT = 1000  # mm
HEIGHT_OF_HUMAN_FACE = 250  # mm
GAZE_DETECTION_URL = "http://127.0.0.1:9001/gaze/gaze_detection?api_key=" + API_KEY

def detect_gazes(frame: np.ndarray):
    img_encode = cv2.imencode(".jpg", frame)[1]
    img_base64 = base64.b64encode(img_encode)
    resp = requests.post(
        GAZE_DETECTION_URL,
        json={
            "api_key": API_KEY,
            "image": {"type": "base64", "value": img_base64.decode("utf-8")},
        },
    )
    gazes = resp.json()[0]["predictions"]
    return gazes


def draw_gaze(img: np.ndarray, gaze: dict):
    # draw face bounding box
    face = gaze["face"]
    x_min = int(face["x"] - face["width"] / 2)
    x_max = int(face["x"] + face["width"] / 2)
    y_min = int(face["y"] - face["height"] / 2)
    y_max = int(face["y"] + face["height"] / 2)
    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (255, 0, 0), 3)

    # draw gaze arrow
    _, imgW = img.shape[:2]
    arrow_length = imgW / 2
    dx = -arrow_length * np.sin(gaze["yaw"]) * np.cos(gaze["pitch"])
    dy = -arrow_length * np.sin(gaze["pitch"])
    cv2.arrowedLine(
        img,
        (int(face["x"]), int(face["y"])),
        (int(face["x"] + dx), int(face["y"] + dy)),
        (0, 0, 255),
        2,
        cv2.LINE_AA,
        tipLength=0.18,
    )

    # draw keypoints
    for keypoint in face["landmarks"]:
        color, thickness, radius = (0, 255, 0), 2, 2
        x, y = int(keypoint["x"]), int(keypoint["y"])
        cv2.circle(img, (x, y), thickness, color, radius)

    # draw label and score
    label = "yaw {:.2f}  pitch {:.2f}".format(
        gaze["yaw"] / np.pi * 180, gaze["pitch"] / np.pi * 180
    )
    cv2.putText(
        img, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3
    )

    return img

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    gaze_data_folder = "C:/junior/ATR_Project/gaze_data"
    os.makedirs(gaze_data_folder, exist_ok=True)  # Create gaze_data folder if it doesn't exist
    csv_file_path = os.path.join(gaze_data_folder, "gaze_report.csv")
    screenshot_folder = os.path.join(gaze_data_folder, "screenshots")
    os.makedirs(screenshot_folder, exist_ok=True)  # Create screenshots folder if it doesn't exist
    
    with open(csv_file_path, 'w', newline='') as csv_file:
        fieldnames = ['Date','Timestamp', 'Yaw', 'Pitch', 'Screenshot_Path']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        screenshot_timer = datetime.now()

        try:
            while True:
                _, frame = cap.read()

                gazes = detect_gazes(frame)

                if len(gazes) == 0:
                    continue

                # draw face & gaze
                gaze = gazes[0]
                draw_gaze(frame, gaze)

                image_height, image_width = frame.shape[:2]

                length_per_pixel = HEIGHT_OF_HUMAN_FACE / gaze["face"]["height"]

                dx = -DISTANCE_TO_OBJECT * np.tan(gaze['yaw']) / length_per_pixel
                # 100000000 is used to denote out of bounds
                dx = dx if not np.isnan(dx) else 100000000
                dy = -DISTANCE_TO_OBJECT * np.arccos(gaze['yaw']) * np.tan(gaze['pitch']) / length_per_pixel
                dy = dy if not np.isnan(dy) else 100000000
                
                timestamp = datetime.now()
                timestamp_str = timestamp.strftime("%Y-%m-%d_%H-%M-%S")
                screenshot_filename = f"screenshot_{timestamp_str}.jpg"
                screenshot_path = os.path.join(screenshot_folder, screenshot_filename)
                cv2.imwrite(screenshot_path, frame)
                
                gaze_point = int(image_width / 2 + dx), int(image_height / 2 + dy)
                
                cv2.circle(frame, gaze_point, 25, (0, 0, 255), -1)

                cv2.imshow("gaze", frame)

                # Save screenshot path to CSV every microsecond
                writer.writerow({
                    'Date': timestamp.date(),
                    'Timestamp': timestamp.time(),
                    'Yaw': gaze['yaw'],
                    'Pitch': gaze['pitch'],
                    'Screenshot_Path': screenshot_path
                })

                # Reset screenshot timer
                screenshot_timer = datetime.now()

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        except Exception as e:
            print("An error occurred:", e)

    # Release the video capture and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
