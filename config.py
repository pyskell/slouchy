from configobj import ConfigObj

# Local imports
#from main import video_device, determine_posture, take_picture, detect_face
from arg  import get_arguments

# Get all command-line arguments. arg.get_arguments() returns a Namespace
# object containg True or False values for the interface mode (GUI or CLI)
# and numeric/string values for selectively overiding the slouchy.ini settings
args = get_arguments()

# Determin if the user wants status output on the command line
text_mode = args.text_mode

# Load settings from the config file (default to slouchy.ini)
config = ConfigObj(args.config_file) if args.config_file\
        else ConfigObj('slouchy.ini')

# Dict-ize args (for looping)
args = vars(args)

# Overide config file settings per the command line
for key, val in args.iteritems():
    if key in config['MAIN'].keys():
        globals()[key] = args[key] if args[key] else config['MAIN'][key]

# Some settings need to be floats (not strings)
for i in ['distance_reference', 'thoracolumbar_tolerance',\
        'cervical_tolerance', 'camera_warm_up']:
    globals()[i] = float(globals()[i])

# video_device can be either an int or str, so try int but fall back on str
try:
  video_device = int(video_device)
except ValueError:
  video_device = str(video_device)


# Set initial values
def setup():
  config = ConfigObj('slouchy.ini')

  maybe_image     = take_picture(video_device)
  maybe_face      = detect_face(maybe_image)
  maybe_current_posture = determine_posture(maybe_face)

  if maybe_current_posture.success:
    config['MAIN']['posture_reference'] = str(maybe_current_posture.result)
    print("Reference value detected as:", maybe_current_posture.result)
  else:
    print("Error:", maybe_current_posture.result)
    return maybe_current_posture

  config.write()
