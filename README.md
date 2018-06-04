# Sharp eye

## Summary

Sharp eye is a basic surveillance system. If a motion is detected an email is send with snapshot showing what is moving.

## Architecture
The application requires Python 2.7. There are mulitple running processes:

* One for the Admin interface
* One for each attached camera

The resource requirement is quite low - this runs stable on Raspberry Pi 2 with load of around 0.2 . The moiton detection is based on snapshots received from the cameras. With the cameras that I'm using the highest frame rate is 8 seconds per frame (this explains the low CPU load).

## Requirements
* A hardware where this can runs on (most SBC are enough).
* Internet connection for sending emails and providing access to the Admin UI.
* WiFi cameras that can provide snapshots.
* SMTP account for the motion notification system.

## Settings

### Admin interface
The settings are in `./resources/admin.yaml`.

The Admin interface runs over HTTPS. As such - it needs a certificate and key file in PEM format. Put them in `./resources/key.pem` and `./resources/cert.pem`. The password for the SSL key should also be provided.

Additional password for accessing the Admin UI should be provided. Again in the same YAML file. The placeholder for it should be pretty obvious.