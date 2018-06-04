from lib import config
from lib.quicklock import lock
from sharp_eye.action import on_motion
from sharp_eye.snapcam import Camera
from sharp_eye.detector import MotionDetector


if __name__ == '__main__':
    lock()
    cam = Camera(ip_address=config['motion']['camera_address'])
    detector = MotionDetector(camera=cam, on_motion=on_motion)
    detector.run()
