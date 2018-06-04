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

A list of cameras are also provided. Check the provided example with two cameras. For each of them the following properties should be provided:

* name - the name identifying the camera.
* active - True/False to specify if by default this camera is enabled/disabled.
* snapshot - A path to image file where the snapshot from the camera will reside.
* command - A shell command for starting the camera motion detection.

### Camera
The camera config is actually a configuration for the motion detection process that operates with that camera. This process is responsible for retrieving the camera snapshots, storing them as local files and executing the motion detection logic over them.

The camera configuration resides in the following files:

* camX_mask.png - a black and white motion detection mask. A black area in that mask indicates that no motion detection is performed for that area.
* camX.yaml - the cammera settings.
* base.yaml - common settings for all cameras (email account settings and credentials).

Check the camX.yaml as start. Most of the required details are there.

The base.yaml should provide all required details for the emails. The following details should be provided:

* SET_TO_EMAIL_HERE - the email where motion detection notifications will be send.
* SET_FROM_EMAIL_HERE - the email where the motion detection emails will be coming from.
* GMAIL_ACCOUNT_USERNAME/GMAIL_ACCOUNT_PASSWORD - credentials for a gmail.com account. The account should allow simple SMTP authentication (this was a setting somewhere in the account).

## Running the surveilance system
Once everything is configured properly the recommended approach is to start a CRON job trying to start the main process (admin.sh) each few minutes. All processes are creating PID files and there is guarantee that at most one will be running at a time. The CRON job provides mechanism to restart the processes in case of failure.

Once the Admin process is started open the UI and check if the interface is working. If so - you'll be able to see up-to-date snapshots when pressing the snapshot buttons for each of the cameras.