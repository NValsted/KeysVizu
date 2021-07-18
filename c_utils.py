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


def valid_color_gradient(color_gradient):
    """
    Ensures stops are sorted and within the bounds [0, 1], as well as
    making sure the color values are valid.
    """
    idx_map = []
    new_stops = []
    new_rgba = []
    for _ in range(len(color_gradient["stops"])):  # number of steps expected to be low, so runtime is acceptable altough inefficient
        lo_idx = color_gradient["stops"].index(min(color_gradient["stops"]))
        idx_map.append(lo_idx)
        new_stops.append(
            min(max(color_gradient["stops"][lo_idx], 0), 1)
        )
        new_rgba.append(
            list(
                map(
                    lambda x: min(max(x, 0), 1),
                    color_gradient["RGBA"][lo_idx]
                )
            )
        )
    
        color_gradient["stops"][lo_idx] = float("inf")

    color_gradient["stops"] = new_stops
    color_gradient["RGBA"] = new_rgba

    return color_gradient, idx_map
