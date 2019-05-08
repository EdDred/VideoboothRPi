# VideoboothRPi
Python3 app to be used on the Raspberry Pi (3) to record video or take a photo

Web (based on Flask) and Tkinter fronted support.

The program is intended to be run on a Raspberry Pi. In my case an Rpi3b+

Functionality:

When user presses a web button or GPIO button 'Video Opnemen' it will record a video with audio and copy it to a mounted usb drive
When user presses a web button or GPIO button 'Foto maken' a photo will be taken.
Support for playing the last video is supported via Web or Tkinter interface

User can not delete a file

The base is the Picam library: https://github.com/iizukanao/picam
Reason for this is that it produces a synchronized mp4 Video/Audio file which proved to be a challenge on the Raspberry pi
This Picam is run as a service as shown in the repository.

For taking a Picture, i used the standard Raspistill command, since that is not supported in Picam.
For it to work the picam service is temporarily stopped and restarted after taking the picture.

Prerquesites:
1. picam installed and setup to run as a service
2. Usb stick mounted
3. link from static directory to /mnt/...
Since I want to use this when not being connected to internet, I need to do the following:
4. at startup: set the correct date : sudo date -s '2017-02-05 15:30:00'
5. start the service: /usr/bin/python3 /home/pi/Videobooth/Web_videobooth.py

Example:

<img src="Example_image/videbooth_example.jpg">




