# Author: Tim Poulsen, github.com/skypanther
# License: MIT
# 2018-08-22

import RPi.GPIO as gpio
import time
from picamera import PiCamera
from picamera.array import PiRGBArray

LOW = False
HIGH = True


class Multicam(object):
    """
    Arducam Multi-camera adapter board class

    Example:
    ```
        multicam = Multicam(num_boards=2)
        # optionally, set the resolution
        multicam.set_resolution(width=640, height=480)
        image = multicam.capture(cam='a')
    ```
    
    Returned image is a 'bgr' OpenCV object. 
    Default resolution is 640 x 480. 
    Default capture camera is board 1, camera A.
    """
    # Pin numbers - Arducam docs/samples use BOARD (physical) numbers
    # You can switch to BCM numbers adding the gpio_mode arg on instantiation
    channel_select_pin = 7
    b1_oe_pin_1 = 11
    b1_oe_pin_2 = 12
    b2_oe_pin_1 = 15
    b2_oe_pin_2 = 16
    b3_oe_pin_1 = 21
    b3_oe_pin_2 = 22
    b4_oe_pin_1 = 23
    b4_oe_pin_2 = 24
    # camera settings:
    iso = 400

    def __init__(self, gpio_mode='board'):
        """
        Initialize the multi-camera board by setting gpio mode and initial state
        per http://www.arducam.com/multi-camera-adapter-module-raspberry-pi/
        """
        self.camera = None
        self.resolution = (640, 480)
        self.gpio_mode = gpio_mode
        gpio.setwarnings(False)
        if gpio_mode == 'board':
            gpio.setmode(gpio.BOARD)
        else:
            self.__set_bcm_mode()
            gpio.setmode(gpio.BCM)
        # set pin modes to output
        gpio.setup(self.channel_select_pin, gpio.OUT)
        gpio.setup(self.b1_oe_pin_1, gpio.OUT)
        gpio.setup(self.b1_oe_pin_2, gpio.OUT)
        gpio.setup(self.b2_oe_pin_1, gpio.OUT)
        gpio.setup(self.b2_oe_pin_2, gpio.OUT)
        gpio.setup(self.b3_oe_pin_1, gpio.OUT)
        gpio.setup(self.b3_oe_pin_2, gpio.OUT)
        gpio.setup(self.b4_oe_pin_1, gpio.OUT)
        gpio.setup(self.b4_oe_pin_2, gpio.OUT)
        # set initial values to select board 1, camera A
        gpio.output(self.channel_select_pin, LOW)
        gpio.output(self.b1_oe_pin_1, LOW)
        gpio.output(self.b1_oe_pin_2, HIGH)
        gpio.output(self.b2_oe_pin_1, HIGH)
        gpio.output(self.b2_oe_pin_2, HIGH)
        gpio.output(self.b3_oe_pin_1, HIGH)
        gpio.output(self.b3_oe_pin_2, HIGH)
        gpio.output(self.b4_oe_pin_1, HIGH)
        gpio.output(self.b4_oe_pin_2, HIGH)
        time.sleep(0.1)

    def __set_bcm_mode(self):
        """
        Swaps gpio pin numbers to be BCM mode
        """
        self.channel_select_pin = 4
        self.b1_oe_pin_1 = 17
        self.b1_oe_pin_2 = 18
        self.b2_oe_pin_1 = 22
        self.b2_oe_pin_2 = 23
        self.b3_oe_pin_1 = 9
        self.b3_oe_pin_2 = 25
        self.b4_oe_pin_1 = 11
        self.b4_oe_pin_2 = 8
        
    def __select_camera(self, cam='a'):
        """
        Select a specific camera to use, defaults to A
        Uses letters on the Arducam board, continuing up
        the alphabet as you stack more boards
        """
        a_channels = ['a', 'c', 'e', 'g', 'i', 'k', 'm', 'o']
        b_channels = ['b', 'd', 'f', 'h', 'j', 'l', 'n', 'p']
        if cam in a_channels:
            gpio.output(self.channel_select_pin, LOW)
        elif cam in b_channels:
            gpio.output(self.channel_select_pin, HIGH)
        else:
            raise 'Invalid camera assignment'
        gpio.output(self.b1_oe_pin_1, HIGH)
        gpio.output(self.b1_oe_pin_2, HIGH)
        gpio.output(self.b2_oe_pin_1, HIGH)
        gpio.output(self.b2_oe_pin_2, HIGH)
        gpio.output(self.b3_oe_pin_1, HIGH)
        gpio.output(self.b3_oe_pin_2, HIGH)
        gpio.output(self.b4_oe_pin_1, HIGH)
        gpio.output(self.b4_oe_pin_2, HIGH)
        if cam == 'a' or cam == 'b':
            gpio.output(self.b1_oe_pin_1, LOW)
        elif cam == 'c' or cam == 'd':
            gpio.output(self.b1_oe_pin_2, LOW)
        elif cam == 'e' or cam == 'f':
            gpio.output(self.b2_oe_pin_1, LOW)
        elif cam == 'g' or cam == 'h':
            gpio.output(self.b2_oe_pin_2, LOW)
        elif cam == 'i' or cam == 'j':
            gpio.output(self.b3_oe_pin_1, LOW)
        elif cam == 'k' or cam == 'l':
            gpio.output(self.b3_oe_pin_2, LOW)
        elif cam == 'm' or cam == 'n':
            gpio.output(self.b4_oe_pin_1, LOW)
        elif cam == 'o' or cam == 'o':
            gpio.output(self.b4_oe_pin_2, LOW)
        else:
            # default to selecting camera A
            gpio.output(self.b1_oe_pin_1, LOW)
        time.sleep(0.1)

    def set_resolution(self, width=640, height=480):
        """
        Sets the capture resolution. Must be one of the supported sizes, see
        https://picamera.readthedocs.io/en/latest/fov.html#sensor-modes

        :param width: Width in whole pixels
        :param height: Height in whole pixels
        """
        w = int(width)
        h = int(height)
        self.resolution = (w, h)

    def capture(self, cam='a', image_format='bgr'):
        """
        Capture an image

        :param cam: Camera from which to capture; uses letters on the Arducam board,
            continuing up the alphabet as you stack more boards
        :return: image
        """
        self.__select_camera(cam=cam.lower())
        if self.camera is None:
            self.__initialize_camera()
        tmp_image = PiRGBArray(self.camera, size=self.resolution)
        self.camera.capture(tmp_image, image_format)
        return tmp_image.array
    
    def cleanup(self):
        if self.camera:
            self.camera.close()
            self.camera = None
        # gpio.cleanup()  # throws errors, so commented out

    def __initialize_camera(self):
        camera = PiCamera()
        camera.resolution = self.resolution
        camera.iso = self.iso
        # let the camera exposure settle
        time.sleep(1)
        # now, fix the values
        camera.shutter_speed = camera.exposure_speed
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g
        self.camera = camera
