from sharp_eye.snapcam2 import Camera
from time import sleep
from datetime import datetime
import cv2
import numpy

DELAY = 1.0


cam = Camera(ip_address='192.168.0.136', timeout=3)

images = 0
times = []


def get_snapshot():
    snapshot_start = datetime.now()
    img = cam.snapshot_img(retries=3)
    if (datetime.now() - snapshot_start).total_seconds() < DELAY:
        sleep(DELAY - (datetime.now() - snapshot_start).total_seconds())
    return img


for i in range(1, 999201):
    start = datetime.now()
    img = get_snapshot()
    time = (datetime.now() - start).total_seconds()
    times.append(time)
    if img is None:
        print '%s: %s No image ...' % (i, time)
        continue
    images += 1
    round_time = round(time, 2)
    print '%s: %s - %s : stats {avg: %.2f, delayed: %s, max_delay: %.2f avg_delay: %.2f} ' % (
        i,
        round_time,
        img.shape,
        numpy.mean(times),
        len([x for x in times if x > DELAY + 0.5]),
        max(times),
        numpy.mean([x for x in times if x > DELAY + 0.5])
    )

print 'Got %s images' % images
print 'Average image retrieval time - %s' % numpy.mean(times)