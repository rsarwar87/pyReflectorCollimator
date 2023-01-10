
# pyReflectorCollimator

This application utilizes a Arducam UVC USB camera (model B0197 which uses the IMX179 sensor) with focuser, to allow collimate reflector telescope.

Requirements:
dearpygui
matplotlib
numpy
opencv-python

Camera should be connected before running the application. 

If there is no output or an unexpected output, change the camera index in main.py as indicated by the comment. 

If you use Windows (tested on Windows 10) try the files in the Windows branch as they have some changed that improve the performance a lot due to some OpenCV weirdness with USB cameras on Windows. If you're on *NIX or Mac OS, you may want to try the version in the original repository if the ones in the main branch of this fork don't work for you. 

A very early build for Windows is also available in the Windows branch, in which case just download the .exe, connect camera, and run it. If it fails to show an image, that's a limitation of the build not having a camera selector. Sorry. Hope to fix in future. 


