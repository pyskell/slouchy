from configobj import ConfigObj

# Local imports
from main import video_device, calculate_y_ratio, take_picture, detect_face

# Set initial values
def setup():
  config = ConfigObj('slouchy.ini')

  # #video_device can be an int or a string, so try int, and if not assume string
  # try:
  #   video_device = int(config['MAIN']['video_device'])
  # except ValueError:
  #   video_device = str(config['MAIN']['video_device'])

  maybe_image     = take_picture(video_device)
  maybe_face      = detect_face(maybe_image)
  maybe_y_ratio = calculate_y_ratio(maybe_face)

  if maybe_y_ratio.success:
    config['MAIN']['y_ratio_reference'] = str(maybe_y_ratio.result)
    print("Reference value detected as:", maybe_y_ratio.result)
  else:
    print("Error:", maybe_y_ratio.result)
    return maybe_y_ratio

  config.write()

if __name__ == '__main__':
  setup()