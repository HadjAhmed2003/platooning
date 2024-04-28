from datetime import datetime
import keyboard
import cv2
from PIL import ImageGrab
import os
import csv

def main():
    print("Press 'q' to quit.")

    # Initialize camera
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Unable to access the camera.")
        return

    # Define video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    dt = datetime.now()
    video_fname = "C:/junior/ATR_Project/player_video/video_{}.avi".format(dt.strftime("%Y%m%d_%H%M%S"))
    out = cv2.VideoWriter(video_fname, fourcc, 7.0, (640, 480))

    # Create folders if they don't exist
    os.makedirs("C:/junior/ATR_Project/player_pictures", exist_ok=True)
    os.makedirs("C:/junior/ATR_Project/player_video", exist_ok=True)
    os.makedirs("C:/junior/ATR_Project/screenshots", exist_ok=True)

    # Create and open CSV file for data
    csv_file_path = "C:/junior/ATR_Project/atr_player_data.csv"
    with open(csv_file_path, mode='w', newline='') as csvfile:
        fieldnames = ['Date', 'Time', 'Screenshot Path', 'Player Picture Path']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            if keyboard.is_pressed('q'):
                print("Exiting the program...")
                break

            try:
                # Capture camera frame
                ret, frame = cam.read()
                if ret:
                    out.write(frame)  # Write frame to video

                    # Capture screen
                    screen = ImageGrab.grab()
                    screen_dt = datetime.now()
                    date_str = screen_dt.strftime("%Y-%m-%d")
                    time_str = screen_dt.strftime("%H:%M:%S.%f")
                    screen_fname = "C:/junior/ATR_Project/screenshots/pic_{}.{}.png".format(date_str, time_str.replace(':', '-'))
                    screen.save(screen_fname, 'png')

                    # Capture picture
                    pic_fname = "C:/junior/ATR_Project/player_pictures/pic_{}.png".format(time_str.replace(':', '-'))
                    cv2.imwrite(pic_fname, frame)

                    # Write data to CSV
                    writer.writerow({'Date': date_str,
                                     'Time': time_str,
                                     'Screenshot Path': screen_fname,
                                     'Player Picture Path': pic_fname})

                else:
                    print("Error: Unable to capture camera frame.")
                    continue

            except Exception as e:
                print(f"Error occurred: {e}")

    # Release video writer and camera
    out.release()
    cam.release()

if __name__ == "__main__":
    main()
q