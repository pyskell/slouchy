# slouchy
Slouchy uses your webcam to check if you're slouching and alert you if you are. This project is still in active development and not feature complete.

# Using
`pip install -r requirements.txt`

`pip install --upgrade --trusted-host wxpython.org --pre -f http://wxpython.org/Phoenix/snapshot-builds/ wxPython_Phoenix`

Sit upright in front of your webcam and run `setup.py` to get the baseline "upright" position for you.

Tweak `slouchy.ini` to your liking

Run `slouchy.py` to have a system tray icon that alerts you when you're slouching.

If it complains about multiple faces run `main.py` and you should get an output image showing everything that looks like a face to the program.

# License
This software is released under the GNU GPL version 3 except for the `haarscascade_frontalface_default.xml` file which is released under the Intel License Agreement For Open Source Computer Vision Library