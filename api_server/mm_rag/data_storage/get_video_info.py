import pathlib
from moviepy.editor import VideoFileClip


def get_video_info(video_uri: str) -> dict:
    # if video_uri is pathlib.Path, then convert it to string
    if isinstance(video_uri, pathlib.Path):
        video_uri = str(video_uri)
        
    clip = VideoFileClip(video_uri)
    duration = clip.duration
    fps = clip.fps
    width, height = clip.size

    return {
        "duration": duration,
        "fps": fps,
        "size": {"width": width, "height": height},
    }
