import cv2
from multicam import Multicam

mcam = Multicam(gpio_mode='bcm')


# cv2.waitKey(0)
# mcam.cleanup()

cv2.imshow('Cam A', mcam.capture(cam='b'))
# cv2.imshow('Cam B', mcam.capture(cam='b'))
# cv2.imshow('Cam C', mcam.capture(cam='c'))
# cv2.imshow('Cam D', mcam.capture(cam='d'))
# cv2.imshow('Cam E', mcam.capture(cam='e'))
# cv2.imshow('Cam F', mcam.capture(cam='f'))
cv2.waitKey(0)
mcam.cleanup()
