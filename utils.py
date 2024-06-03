from config import BLACK, WHITE


def interpolate_color(value, max_value):
    """
    interpolates a color between green and red based on a given value and maximum value (min is 0).
    """
    if value == -1:
        return WHITE, (0, 0, 0, 128) 
    distance = abs(value - max_value)
    if distance > max_value:
        distance = max_value
    ratio = distance / max_value
    red = int(255 * (1 - ratio))
    green = int(255 * ratio)
    return BLACK, (red, green, 0, 128)
