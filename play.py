import time
import os

ASCII_FILE = "ascii_frames.txt"
FRAME_DELAY = 0.033

if __name__ == "__main__":
    with open(ASCII_FILE, "r", encoding="utf-8") as f:
        frame_raw = f.read().replace(".", " ")
    
    frames = frame_raw.split("SPLIT")
    
    init_time = time.time()
    total_frames = len(frames)
    
    while True:
        frame_index = int((time.time() - init_time) / FRAME_DELAY)
        if frame_index >= total_frames:
            break
        os.system("clear")
        print(frames[frame_index])
        time.sleep(FRAME_DELAY)
    
    print("Plis subscribe.")
