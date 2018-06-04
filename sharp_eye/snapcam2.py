import urllib2
import cv2
import numpy
import time
from StringIO import StringIO
from lib import config


class Camera(object):
    """
    Camera object that can be used to communicate with the camera. I.e. - get video stream, download snapshot...
    """

    def __init__(self, ip_address, timeout=5):
        """
        Initialize camera object.
        :param ip_address: the camera ip
        :param timeout: timeout of http calls
        """
        # self.url = 'http://%s' % ip_address
        self.url = 'http://192.168.0.50/cgi-bin/api.cgi?cmd=Snap&channel=0&rs=foo&user=admin&password='
        self.timeout = timeout
        self.save_all = config.get('save_all_snapshots', False)
        self.count = 0

    def snapshot(self, retries=0, retry_delay=1):
        """
        Get snapshot from the camera.
        :param retries: how many retries to be done for getting the snapshot
        :param retry_delay: delay (sec) between retries
        :return: StringIO
        """
        snapshot_url = self.url

        while True:
            # log('Camera %s - getting frame' % config['identifier'])
            data = urllib2.urlopen(snapshot_url,
                                   timeout=self.timeout).read()
            if data:
                # log('Camera %s - got frame' % config['identifier'])
                return StringIO(data)
            else:
                if retries:
                    retries -= 1
                    time.sleep(retry_delay)
                    # log('Camera %s - got no frame, retrying' % config['identifier'])
                else:
                    # log('Camera %s - got no frame, no more retries' % config['identifier'])
                    pass

                    return None

    def snapshot_img(self, retries=0, retry_delay=1):
        """
        Get snapshot from the camera.
        :param retries: how many retries to be done for getting the snapshot
        :param retry_delay: delay (sec) between retries
        :return: cv2 image object representing the snapshot
        """
        img_fd = self.snapshot(retries, retry_delay)
        if not img_fd:
            return None

        img_array = numpy.fromstring(img_fd.getvalue(), dtype=numpy.uint8)
        result = cv2.imdecode(img_array, flags=cv2.IMREAD_UNCHANGED)
        if self.save_all:
            self.count += 1
            cv2.imwrite('%s/frame_%04d.jpg' % (config['snapshot_history'], self.count),
                        cv2.resize(result, (0, 0), fx=0.25, fy=0.25))

        return result


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2 and sys.argv[1]:
        cam = Camera('192.168.0.10')
        data = cam.snapshot()
        fd = open(sys.argv[1], 'w')
        fd.write(data.read())
        fd.close()
    else:
        print 'Specify file name as 1st argument'