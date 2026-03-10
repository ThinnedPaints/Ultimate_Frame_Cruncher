import cv2
import time 
import datetime
import moviepy
import json
import ast
from tqdm import tqdm
from moviepy.editor import VideoFileClip, concatenate_videoclips

def get_time_in_min_and_second(seconds):
    #Get seconds as int, return minuites and seconds as str
    return str(datetime.timedelta(seconds = seconds))


def process_video(timestamps):
    print("Processing video")
    for timestamp in timestamps:
        timestamp[0] = timestamp[0]-90
    main_video = VideoFileClip(video_path)
    clips = [main_video.subclip(start, stop) for start, stop in timestamps]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_video_path, codec="h264_nvenc", audio_codec="aac")
    

def video_analysis(video_path, target_path):
    start = time.time()

    video = cv2.VideoCapture(video_path)
    template = cv2.imread(target_path, 0)

    frame_count = 0
    frames_analysed = 0
    total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

    timestamps = []
    detecting = False
    start_time = None

    threshold = 0.95

    for i in tqdm(range(int(total_frames))):
        ret, frame = video.read()
        if not ret:
            break

        frame_count += 1

        if frame_count % 30 == 0:
            frames_analysed += 1

            video_time_in_seconds = frame_count / 30
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
            max_val = result.max()

            if max_val >= threshold:
                if not detecting:
                    detecting = True
                    start_time = video_time_in_seconds

            else:
                if detecting:
                    detecting = False
                    timestamps.append([start_time, video_time_in_seconds])

    video.release()

    end = time.time()
    length = end - start
    total_time = get_time_in_min_and_second(length)

    print(total_time + " time taken")
    print(frames_analysed, " frames analysed")

    for segment in timestamps:
        print(segment)

    return timestamps

media_path = "media/"
video_path = media_path + "umar_bautista.mp4"
output_video_path = media_path + "output.mp4"
target_path = media_path + "target.png"

no_Good_Name = True
if no_Good_Name == True:
    timestamps = video_analysis(video_path=video_path, target_path=target_path)

process_video(timestamps)


