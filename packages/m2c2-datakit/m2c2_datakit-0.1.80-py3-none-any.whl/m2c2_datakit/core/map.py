import re
from m2c2_datakit.tasks import (
    color_dots,
    grid_memory,
    symbol_search,
    shopping_list,
    symbol_number_matching,
)


def expand_func_map(base_map):
    expanded_map = {}
    for key, value in base_map.items():
        lower = key.lower()
        sentence = key.capitalize()
        hyphenated = re.sub(r"\s+", "-", lower)

        # Original
        expanded_map[key] = value
        # Lowercase
        expanded_map[lower] = value
        # Sentence case
        expanded_map[sentence] = value
        # Hyphenated lowercase
        expanded_map[hyphenated] = value

    return expanded_map


DEFAULT_FUNC_MAP_SCORING = {
    "Grid Memory": [
        ("error_distance_hausdorff", grid_memory.score_hausdorff),
        ("error_distance_mean", grid_memory.score_mean_error),
        ("error_distance_sum", grid_memory.score_sum_error),
    ],
    "Symbol Search": [
        ("accuracy", symbol_search.score_accuracy),
    ],
}

DEFAULT_FUNC_MAP_SCORING = expand_func_map(DEFAULT_FUNC_MAP_SCORING)
