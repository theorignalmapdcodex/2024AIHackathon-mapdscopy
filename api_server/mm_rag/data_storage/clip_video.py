import pathlib
from moviepy.video.io.VideoFileClip import VideoFileClip


def clip_video(video_uri: str, start_time: int, end_time: int, output_uri: str):
    if isinstance(video_uri, pathlib.Path):
        video_uri = str(video_uri)
    if isinstance(output_uri, pathlib.Path):
        output_uri = str(output_uri)

    # clip video from start_time to end_time and save it to output_uri
    clip = VideoFileClip(video_uri).subclip(start_time, end_time)
    clip.write_videofile(output_uri)
    clip.close()
