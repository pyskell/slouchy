# slouchy
Slouchy uses your webcam to check if you're slouching and alert you if you are. This project is still in active development and not feature complete.

# Using - Linux
`pip install -r requirements.txt`

Install PyQT4 and QT4 are installed: http://pyqt.sourceforge.net/Docs/PyQt4/installation.html

Tweak `slouchy.ini` to your liking.

Run `slouchy.py`

Sit upright in front of your webcam.

While sitting upright, right click on the Slouchy icon in your system try and choose setup.

Slouchy will now alert you if you're slouching

If it complains about multiple faces run `main.py` and you should get an output image showing everything that looks like a face to the program. Remove anything from the background that looks like a face.

# License
This software is released under the GNU GPL version 3 except for the `haarscascade_frontalface_default.xml` file which is released under the Intel License Agreement For Open Source Computer Vision Library

# Disclaimer
This software is not intended to diagnose, cure, or prevent diseases in any way. No warranties are made or implied for its efficacy. It's simply a little program the author wanted and decided to share.
