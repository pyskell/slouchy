from configobj import ConfigObj

# Local imports
from main import video_device, determine_posture, take_picture, detect_face

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

if __name__ == '__main__':
  setup()
