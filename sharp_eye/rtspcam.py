import cv2
import numpy
import time
from lib.lib import (
    log,
    get_pid_process_name,
    check_background_process,
    kill
)
from StringIO import StringIO
from subprocess import Popen
from lib.quicklock import register_sub_process
from os.path import getmtime


STREAMING_COMMAND = '/usr/local/bin/ffmpeg -nostats -loglevel 0 -i rtsp://%s:554/12 -y -r 2 -updatefirst 1 %s'


class Camera(object):
    """
    Camera object that can be used to communicate with the camera. I.e. - get video stream, download snapshot...
    """

    def __init__(self, ip_address, snapshot_file, timeout=5):
        """
        Initialize camera object.
        :param ip_address: the camera ip
        :param timeout: timeout of getting snapshot
        """
        self.snapshot_file = snapshot_file
        self.streaming_process_pid = None
        self.last_snapshot_timestamp = None
        self.streaming_process_name = None
        self.streaming_command = STREAMING_COMMAND % (ip_address, self.snapshot_file)
        self._verify_streaming()

    def _verify_streaming(self, force_restart=False):
        """
        Check if the background streaming process is running and if not - start it.
        :param force_restart: if True - kill the old streaming process and start new one.
        """
        if self.streaming_process_pid:
            background_process_running = \
                check_background_process(self.streaming_process_pid, self.streaming_process_name)

            if not force_restart and background_process_running:
                return

            if force_restart and background_process_running:
                log('Killing background process, force_restart=%s' % force_restart)
                kill(self.streaming_process_pid)
                self.streaming_process_pid = None
                self.streaming_process_name = None

        try:
            log('Starting background process')
            import os
            DEVNULL = open(os.devnull, 'wb')
            LOG = open('/tmp/ffm.log', 'wb')
            streaming_pid = Popen(self.streaming_command.split(' '), stdin=DEVNULL).pid
            register_sub_process(streaming_pid)
            self.streaming_process_pid = streaming_pid
            self.streaming_process_name = get_pid_process_name(streaming_pid)
            log('Started background process')
            # Wait till the streaming process starts working
            self.snapshot(10, 1, ignore_errors=True)
            log('Started background verified')
        except Exception as e:
            log('Failed to run RTSP client: %s' % repr(e))

    def snapshot(self, retries=0, retry_delay=1, ignore_errors=False):
        """
        Get snapshot from the camera.
        :param retries: how many retries to be done for getting the snapshot
        :param retry_delay: delay (sec) between retries
        :return: StringIO
        """
        import pdb; pdb.set_trace()
        self._verify_streaming()

        while retries > 0 and self.last_snapshot_timestamp == getmtime(self.snapshot_file):
            time.sleep(retry_delay)
            retries -= 1

        if retries >= 1:
            with open(self.snapshot_file, 'r') as img_input:
                return StringIO(img_input.read())
        elif not ignore_errors:
            self._verify_streaming(force_restart=True)

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
        return result


if __name__ == '__main__':
    cam = Camera('192.168.0.10', '/tmp/cam_test.bmp')
    while True:
        cam.snapshot()
