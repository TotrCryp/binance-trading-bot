
class DepositDivider:
    current_proportions_list = []
    rounding_accuracy = 0

    @classmethod
    def update_proportions_list(cls, new_proportions_list):
        if cls.current_proportions_list != new_proportions_list:
            cls.current_proportions_list = new_proportions_list

    @classmethod
    def update_rounding_accuracy(cls, rounding_accuracy):
        cls.rounding_accuracy = rounding_accuracy

    def __init__(self, remnant):
        self.remnant = remnant

    def set_remnant(self, remnant):
        self.remnant = remnant

    def get_bath(self, current_stage):
        if current_stage == len(self.current_proportions_list):
            return self.remnant

        index = current_stage - 1
        part = self.remnant * self.current_proportions_list[index] / sum(self.current_proportions_list[index:])
        return round(part, self.rounding_accuracy)
