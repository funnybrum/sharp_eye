import RPi.GPIO as GPIO


ALARM_PIN = 11
SENSOR_PIN = 12


def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ALARM_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(SENSOR_PIN, GPIO.OUT, initial=GPIO.LOW)


def sensor(active):
    """ Set the sensor status to active/inactive.
    :param active: True iff the sensor should be activated.
    """
    if active and GPIO.input(SENSOR_PIN) == GPIO.LOW:
        GPIO.output(SENSOR_PIN, GPIO.HIGH)
    if not active and GPIO.input(SENSOR_PIN) == GPIO.HIGH:
        GPIO.output(SENSOR_PIN, GPIO.LOW)


def siren(enabled):
    """ Set the siren status to enabled/disabled.
    :param enabled: True iff the alarm should be enabled.
    """
    if not enabled and GPIO.input(ALARM_PIN) == GPIO.LOW:
        GPIO.output(ALARM_PIN, GPIO.HIGH)
    if enabled and GPIO.input(ALARM_PIN) == GPIO.HIGH:
        GPIO.output(ALARM_PIN, GPIO.LOW)


# init()
# from time import sleep
# while 1:
#     sensor(True)
#     sleep(0.5)
#     siren(False)
#     sleep(0.5)
#     sensor(False)
#     siren(True)
#     sleep(1)
