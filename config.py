# -*- coding: utf-8 -*-
from configobj import ConfigObj

# Local import
from arg import get_arguments

# Get all command-line arguments. arg.get_arguments() returns a Namespace
# object containg True or False values for the interface mode (GUI or CLI)
# and numeric/string values for selectively overiding the slouchy.ini settings
args = get_arguments()

# Determine if the user wants status output on the command line
text_mode = args.text_mode

# Load settings from the config file (default to slouchy.ini)
if args.config_file:
  config_file = ConfigObj(args.config_file) 
else:
  config_file = ConfigObj('slouchy.ini')

# Dict-ize args (for looping)
args = vars(args)

# Overide config file settings per the command line
for key, val in args.iteritems():
  if key in config_file['MAIN'].keys():
    globals()[key] = args[key] if args[key] else config_file['MAIN'][key]

# Some settings need to be floats (not strings)
for i in ['distance_reference', 'thoracolumbar_tolerance',\
          'cervical_tolerance', 'camera_warm_up']:
  globals()[i] = float(globals()[i])

# poll_rate needs to be an int
globals()['poll_rate'] = int(globals()['poll_rate'])

# video_device can be either an int or str, so try int but fall back on str
video_device = globals()['video_device']
try:
  video_device = int(video_device)
except ValueError:
  video_device = str(video_device)
