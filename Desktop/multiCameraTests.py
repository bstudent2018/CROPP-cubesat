import time
import picamera

timeName = time.strftime('%d%b%Y(%H:%M)', time.localtime())
print(f'Recording Videos at {timeName}')
with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.start_recording(f'{timeName}Camera1.h264', splitter_port=0)
    camera.start_recording(f'{timeName}Camera2.h264', splitter_port=1)
    camera.start_recording(f'{timeName}Camera3.h264', splitter_port=2)
    camera.start_recording(f'{timeName}Camera4.h264', splitter_port=3)
    camera.wait_recording(10)
    camera.stop_recording(splitter_port=0)
    camera.stop_recording(splitter_port=1)
    camera.stop_recording(splitter_port=2)
    camera.stop_recording(splitter_port=3)
print(f'Done Recording Videos')