#!/bin/bash
if (($# == 1))
then
    fswebcam -d /dev/video0 -r 640x480 -S 10 -F 10 $1
else
    echo 'Richtige Benutzung: takePicture.sh <Dateiname>'
fi
