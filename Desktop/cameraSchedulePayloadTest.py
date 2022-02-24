import schedule
import time
import pi camera

#functions
def takeVideo():
    timeName = time.strftime('%d%b%Y(%H:%M)', time.localtime())
    print(f'Recording Videos at {timeName}')
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_recording(f'{timeName}Camera1.h264', splitter_port=0)
        camera.start_recording(f'{timeName}Camera2.h264')
        camera.start_recording(f'{timeName}Camera3.h264', splitter_port=2)
        camera.start_recording(f'{timeName}Camera4.h264', splitter_port=3)
        camera.wait_recording(120)
        camera.stop_recording(splitter_port=0)
        camera.stop_recording()
        camera.stop_recording(splitter_port=2)
        camera.stop_recording(splitter_port=3)
    
    timeName = time.strftime('%d%b%Y(%H:%M)', time.localtime())
    print(f'Done Recording Videos at {timeName}')

#schedule
schedule.every().day.at("16:24").do(takeVideo)

#24 hours
while True:
        schudule.run_pending()
        time.sleep(1)