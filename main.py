"""
This is a little personal project I've written up to skip all the bullshit in the big bald pink guy's second favourite fight promotion.
It creates a condensed version of the event, through magic (mostly cv2 and moviepy)
"""
import cv2
import time 
import datetime
from tqdm import tqdm
from moviepy.editor import VideoFileClip, concatenate_videoclips

def get_time_in_min_and_second(seconds):
    # Get seconds as int, return mins and seconds as str
    return str(datetime.timedelta(seconds = seconds))


def process_video(timestamps):
    # Takes 2d array of timestamps, applies them to main video, renders output into chosen folder
    # Get the clips, use moviepy to cut them out from the main video, stick them together into a new file, then render it out
    print("Processing video")
    main_video = VideoFileClip(video_path)
    clips = [main_video.subclip(start, stop) for start, stop in timestamps]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    

def video_analysis(video_path, target_path):
    # Generates 2d array of timestamps
    # Use cv2 to scan through a video looking for a target, in this case, a certain MMA promotion's fight timer
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
    # Honestly it's wack that this i has to be there for tqdm to work
    # I could very much be wrong about that, but I can't be bothered reading, too busy making spaghet
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
                    timestamps.append([(start_time-4), video_time_in_seconds])

    video.release()

    end = time.time()
    length = end - start
    total_time = get_time_in_min_and_second(length)

    print(total_time + " time taken")
    print(frames_analysed, " frames analysed")

    # Could ditch this, but I like it, and it's my code
    for segment in timestamps:
        print(segment)

    return timestamps

# There's probably a cleaner way of doing this that isn't just globals, but again, it's my code, and I'll do what I want.
media_path = "media/"
video_path = media_path + "umar_bautista.mp4"
output_video_path = media_path + "output.mp4"
target_path = media_path + "target.png"

timestamps = video_analysis(video_path=video_path, target_path=target_path)

process_video(timestamps)


