# slouchy
Slouchy uses your webcam to check if you're slouching and alert you if you are. This project is still in active development and not feature complete.

# Requirements
You need to install the following system-wide:

* Python 2.7
* [Qt4](http://doc.qt.io/qt-4.8/installation.html) and [PyQt4](http://pyqt.sourceforge.net/Docs/PyQt4/installation.html)
* [OpenCV](http://docs.opencv.org/doc/tutorials/introduction/table_of_content_introduction/table_of_content_introduction.html)
* [OpenCV-Python](https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_setup/py_table_of_contents_setup/py_table_of_contents_setup.html#py-table-of-content-setup)

On Debian-based distros the below apt-get should work:

`apt-get install python2.7 python2.7-dev libqt4-core libqt4-dev opencv-data libopencv-core2.4 libopencv-dev python-opencv`

On Mac:

`brew tap homebrew/science`

`brew install python qt pyqt opencv`

For all systems additional dependencies need to be installed via:

`pip install -r requirements.txt`

# Using

Tweak `slouchy.ini` to your liking.

Run `python slouchy.py`

Sit upright in front of your webcam.

While sitting upright, right click on the Slouchy icon in your system tray and choose setup.

Slouchy will now alert you if you're slouching

# License
This software is released under the GNU GPL version 3 except for the `haarscascade_frontalface_default.xml` file which is released under the Intel License Agreement For Open Source Computer Vision Library

# Disclaimer
This software is not intended to diagnose, cure, or prevent diseases in any way. No warranties are made or implied for its efficacy. It's simply a little program the author wanted and decided to share.
