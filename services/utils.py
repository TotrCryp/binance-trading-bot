def scale_to_range(value, min_val, max_val, new_min=-10, new_max=10):
    if max_val == min_val:
        return 0
    scaled = (value - min_val) / (max_val - min_val)
    return scaled * (new_max - new_min) + new_min


def percentage_difference(old_value, new_value):
    difference = new_value - old_value
    percentage_diff = ((difference / new_value) * 100)
    return percentage_diff


def add_percent(numeric_value, percent_value):
    percent = numeric_value * percent_value / 100
    price_with_percent = numeric_value + percent
    return price_with_percent


class BathDivider:
    def __init__(self, remnant, batch_list):
        self._remnant = remnant
        self._batch_list = batch_list

    def get_batch(self, current_stage):
        if current_stage == len(self._batch_list):
            return self._remnant
        part = round(self._remnant * self._batch_list[current_stage] / sum(self._batch_list[current_stage:]))
        return part

    def set_remnant(self, remnant):
        self._remnant = remnant
