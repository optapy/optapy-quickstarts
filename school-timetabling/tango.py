SEQUENCE_1 = [0x8AE234, 0xFCE94F, 0x729FCF, 0xE9B96E, 0xAD7FA8]
SEQUENCE_2 = [0x73D216, 0xEDD400, 0x3465A4, 0xC17D11, 0x75507B]

color_dict = dict()
next_color_count = 0


def pick_color(item):
  color = color_dict.get(item)
  if color is not None:
    return color
  
  color = next_color()
  color_dict[item] = color
  return color


def next_color():
  global next_color_count
  color = None
  color_index = next_color_count % len(SEQUENCE_1)
  shade_index = next_color_count // len(SEQUENCE_1)
  
  if shade_index == 0:
    color = SEQUENCE_1[color_index]
  elif shade_index == 1:
    color = SEQUENCE_2[color_index]
  else:
    shade_index -= 3
    floor_color = SEQUENCE_2[color_index]
    ceil_color = SEQUENCE_1[color_index]
    base = (shade_index // 2) + 1
    divisor = 2
    while base >= divisor:
      divisor *= 2
    
    base = (base * 2) - divisor + 1
    shadePercentage = base / divisor;
    color = build_percentage_color(floor_color, ceil_color, shade_percentage)
  next_color_count += 1
  hex_string = hex(color)[2:]
  return f"#{hex_string}"


def build_percentage_color(floor_color, ceil_color, shade_percentage):
  red = (floor_color & 0xFF0000) + int(shade_percentage * ((ceil_color & 0xFF0000) - (floor_color & 0xFF0000))) & 0xFF0000
  green = (floor_color & 0x00FF00) + int(shade_percentage * ((ceil_color & 0x00FF00) - (floor_color & 0x00FF00))) & 0x00FF00
  blue = (floor_color & 0x0000FF) + int(shade_percentage * ((ceil_color & 0x0000FF) - (floor_color & 0x0000FF))) & 0x0000FF
  return red | green | blue