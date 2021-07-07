# This script should be renamed
import json


def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)

    return data


def load_config():
    config_dict = load_json('config.json')
    return config_dict


def interpolate_color(color_gradient, t):
    for i, stop in enumerate(color_gradient["stops"]):  # Ensure stops are sorted
        if t < stop:
            if i == 0:
                return color_gradient["RGBA"][0]
            t_range = stop - color_gradient["stops"][i-1]
            sub_t = (t - color_gradient["stops"][i-1]) / t_range
            color = [
                color_gradient["RGBA"][i-1][rgba] * (1 - sub_t)
                + color_gradient["RGBA"][i][rgba] * sub_t
                for rgba in range(4)
            ]
            return color

    return color_gradient["RGBA"][-1]
