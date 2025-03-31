import cv2
import numpy as np
import shutil
import os


ASCII_CHARS = " .:-=+*#■"
EDGE_CHARS = "-|\\/"


video_path = "video.mp4"
output_text_path = "ascii_frames.txt"


vidcap = cv2.VideoCapture(video_path)
frame_rate = 33
frames = []
time_count = 0


if not vidcap.isOpened():
    print("Error: Could not open video file.")
    exit()

while True:
    vidcap.set(cv2.CAP_PROP_POS_MSEC, time_count)
    success, frame = vidcap.read()
    if not success:
        break 

    print(f"Processing frame at {time_count}ms")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    
    ascii_width = 100  
    ascii_height = int((gray.shape[0] / gray.shape[1]) * ascii_width * 0.5)
    gray_resized = cv2.resize(gray, (ascii_width, ascii_height))

    
    contrast_factor = 1.3
    midpoint = np.median(gray_resized)
    gray_resized = np.clip(midpoint + contrast_factor * (gray_resized - midpoint), 0, 255).astype(np.uint8)

    
    sharpening_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    gray_sharpened = cv2.filter2D(gray_resized, -1, sharpening_kernel)

    
    grad_x = cv2.Sobel(gray_sharpened, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray_sharpened, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = np.sqrt(grad_x**2 + grad_y**2)
    direction = np.arctan2(grad_y, grad_x)

    
    gray_norm = gray_sharpened / 255.0
    edge_threshold = np.max(magnitude) * 0.4

    
    ascii_image = []
    for y in range(ascii_height):
        row = ""
        for x in range(ascii_width):
            if magnitude[y, x] > edge_threshold:
                angle = direction[y, x]
                if -0.5 < angle < 0.5:
                    row += "-"
                elif 0.5 < angle < 2.5:
                    row += "\\"
                elif -2.5 < angle < -0.5:
                    row += "/"
                else:
                    row += "|"
            else:
                brightness = gray_norm[y, x]
                ascii_index = int(brightness * (len(ASCII_CHARS) - 1))
                row += ASCII_CHARS[ascii_index]
        ascii_image.append(row)
    
    frames.append("\n".join(ascii_image))
    time_count += frame_rate


with open(output_text_path, "w", encoding="utf-8") as f:
    f.write("SPLIT".join(frames))

print("ASCII frames saved to ascii_frames.txt")
