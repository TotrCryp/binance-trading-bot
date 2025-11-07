class DepositDivider:
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
