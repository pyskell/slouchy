from configobj import ConfigObj

# Local imports
#from main import video_device, determine_posture, take_picture, detect_face
from arg  import get_arguments

# Get all command-line arguments, which specify the interface mode (GUI or CLI)
# and overide the settings in slouchy.ini
args = get_arguments()
print args
text_mode = args.text_mode

# Load settings from slouchy.ini
config                  = ConfigObj('slouchy.ini')
distance_reference      = float(config['MAIN']['distance_reference'])
thoracolumbar_tolerance = float(config['MAIN']['thoracolumbar_tolerance'])
cervical_tolerance      = float(config['MAIN']['cervical_tolerance'])
face_cc_path            = str(config['MAIN']['face_cascade_path'])
eye_cc_path             = str(config['MAIN']['eye_cascade_path'])
camera_warm_up          = args.warm_up_time if args.warm_up_time\
        else int(config['MAIN']['camera_warm_up'])

# video_device can be either an int or str, so try int but fall back on str
try:
  video_device = int(config['MAIN']['video_device'])
except ValueError:
  video_device = str(config['MAIN']['video_device'])

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

#if __name__ == '__main__':
#  setup()
