# slouchy
Slouchy uses your webcam to check if you're slouching and alert you if you are. This project is still in active development and not feature complete.

# Using
`pip install -r requirements.txt`

Tweak `slouchy.ini` to your liking

Sit upright in front of your webcam and run `setup.py` to get the baseline "upright" position for you.

Run `slouchy.py` to have a system tray icon that alerts you when you're slouching.

If it complains about multiple faces run `main.py` and you should get an output image showing everything that looks like a face to the program. Remove anything from the background that looks like a face.

# License
This software is released under the GNU GPL version 3 except for the `haarscascade_frontalface_default.xml` file which is released under the Intel License Agreement For Open Source Computer Vision Library

# Disclaimer
This software is not intended to diagnosis, cure, or prevent diseases in any way. No warranties are made or implied for its efficacy. It's simply a little program the author wanted and decided to share.