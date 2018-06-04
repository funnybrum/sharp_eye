# !/bin/bash
cd /home/pi/scripts/surveillance
APP_CONFIG=./resources/admin.yaml python admin.py >> /var/log/admin.log
