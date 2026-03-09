import cv2
import time 
import datetime
import moviepy
import json
from moviepy.editor import VideoFileClip

def get_time_in_min_and_second(seconds):
    #Get seconds as int, return minuites and seconds as str
    return str(datetime.timedelta(seconds = seconds))


def process_video(timestamps):
    with open("stamps.json", "r") as f:
        timestamps = json.load(f)
    
    print(timestamps)
    #main_video = VideoFileClip(video_path)
    #clip = main_video.subclip()
    #return

def video_analysis(video_path, target_path):
    #Analyse the video file and create an array of tuples containing timestamps
    start = time.time()

    video = cv2.VideoCapture(video_path)
    template = cv2.imread(target_path, 0)
    frame_count = 0
    frames_analysed = 0

    timestamps = []
    detecting = False
    while True:
        ret, frame = video.read()
        if not ret:
            break

        frame_count += 1

        if frame_count % 30 == 0:
            frames_analysed += 1
            video_time_in_seconds = frame_count / 30
            video_time_true = get_time_in_min_and_second(video_time_in_seconds)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)

            threshold = 0.95
            max_val = result.max()
            if max_val >= threshold:
                if detecting == False:
                    print("Target detected at :", video_time_true)
                    # print("match score:", max_val)
                    detecting = True
                    timestamps.append(("start", video_time_in_seconds))
            else:
                if detecting == True:
                    print("Target gone at ", video_time_true)
                    detecting = False
                    timestamps.append(("stop", video_time_in_seconds))

    video.release()

    end = time.time()
    length = end - start
    total_time = get_time_in_min_and_second(length)
    print(total_time + " time taken")
    print(frames_analysed, " frames analysed")

    json_timestamps = json.dumps(timestamps)

    with open("stamps.json", "w") as f:
        json.dump(json_timestamps, f)

    return timestamps

media_path = "media/"
video_path = media_path + "umar_bautista.mp4"
target_path = media_path + "target.png"

no_Good_Name = False
if no_Good_Name == True:
    timestamps = video_analysis(video_path=video_path, target_path=target_path)

timestamps = []


process_video(timestamps=timestamps)


