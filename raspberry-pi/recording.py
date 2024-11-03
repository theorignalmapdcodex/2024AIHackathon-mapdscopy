import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from pathlib import Path
import os
import requests
import sounddevice as sd
import wave
import subprocess 
import threading
from gpiozero import LED

led_green = LED("GPIO19")
led_red = LED("GPIO21")

led_green.off()
led_red.off()

class AudioRecorder:
    def __init__(self, audio_file_name="demo_0.wav", fs=44100, channels=2):
        self.audio_file_name = audio_file_name
        self.fs = fs # samples per sec
        self.channels = channels # 2: recorded in stereo

    def record_audio(self, duration):
        print("Recording audio...")
        audio_data = sd.rec(int(duration * self.fs), samplerate=self.fs, channels=self.channels, dtype='int16')
        sd.wait()  # Wait until recording is finished
        print("Audio recording complete!")
        
        # Save as WAV file
        wf = wave.open(self.audio_file_name, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(2)
        wf.setframerate(self.fs)
        wf.writeframes(audio_data.tobytes())
        wf.close()

class VideoRecorder:
    def __init__(self, out_resolution=(1920, 1080)):
        # set up video quality
        self.out_resolution = out_resolution
        self.encoder = H264Encoder()
        
        # camera instance
        self.picam2 = Picamera2()
        video_config = self.picam2.create_video_configuration(main={"size": self.out_resolution})
        self.picam2.configure(video_config)
        print(f"picam2 configured with resolution {out_resolution}.")
    
    def record_video(self, duration, file_path):
        ''' Function to record video for fixed duration'''
        try:
            temp_file_path = os.path.join("data","temp_video.h264")
            self.picam2.start_recording(self.encoder, temp_file_path)
            print(f"Video recording for {duration} seconds.......")

            # set the light
            led_red.off()
            led_green.on()

            time.sleep(duration)
            self.picam2.stop_recording()

            # set the light
            led_red.on()
            led_green.off()

            print(f"Video recording complete. Converting to MP4 format...")
            
            # Convert the H264 file to MP4 using ffmpeg
            subprocess.run(["ffmpeg", "-i", temp_file_path, "-c:v", "copy", file_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Video saved to {file_path}")
        
        except Exception as e:
            print(e)
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                print("Cached video removed.")
            print("Video recording complete!")

class Recorder:
    def __init__(self, out_resolution=(1920, 1080)):
        self.out_resolution = out_resolution
        
        # integrate video and audio
        self.video_recorder = VideoRecorder(out_resolution)
        self.audio_recorder = AudioRecorder()

    def main_loop(self, duration, to_folder="data", video_file_name="demo_0.mp4", audio_file_name="demo_0.wav"):
        # set up output path
        if not os.path.exists(to_folder):
            os.makedirs(to_folder)
        
        video_out_path = os.path.join(to_folder, video_file_name)
        audio_out_path = os.path.join(to_folder, audio_file_name)

        if os.path.exists(video_out_path):
            os.remove(video_out_path)
            print("Old video file detected, removed.")
        if os.path.exists(audio_out_path):
            os.remove(audio_out_path)
            print("Old audio file detected, removed.")

        self.video_recorder.video_file_name = video_out_path
        self.audio_recorder.audio_file_name = audio_out_path

        # start thread to record video and audio at the same time
        video_thread = threading.Thread(target=self.video_recorder.record_video, args=(duration, video_out_path,))
        audio_thread = threading.Thread(target=self.audio_recorder.record_audio, args=(duration, ))

        video_thread.start()
        audio_thread.start()

        video_thread.join()
        audio_thread.join()

        print("Capture complete!")

def upload_to_server(to_folder="data", video_file_name="demo_0.mp4", audio_file_name="demo_0.wav"):
    url = "http://vcm-43401.vm.duke.edu/upload_video"
    with open(os.path.join(to_folder, video_file_name), "rb") as video_file, \
         open(os.path.join(to_folder, audio_file_name), "rb") as audio_file:
        files = {
            "video": video_file,
            "audio": audio_file
        }
        response = requests.post(url, files=files)
    if response.status_code == 201:
        print("Upload complete!")
    else:
        print(response.__dir__())
        print("Upload failed with status code", response.status_code)

if __name__ == "__main__":
    led_red.on()
    duration = 30  # Set the duration for recording
    recorder = Recorder(out_resolution=(1280,720))
    recorder.main_loop(duration)
    upload_to_server()
