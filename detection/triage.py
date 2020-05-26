from detection.data_pipe import DataPipe


class Triage(DataPipe):
    def __init__(self, threshold=[0.13, 0.87]):
        DataPipe.__init__(self, "localhost:9092")
        self.threshold_ben = threshold[0]
        self.threshold_phish = threshold[1]

    def decision_maker(self, prob_ben, prob_phish):
        if (prob_ben == self.threshold_ben) or (prob_phish == self.threshold_ben):
            return 0
        elif (prob_ben <= self.threshold_ben and prob_phish >= self.threshold_phish) or \
            (prob_ben >= self.threshold_phish and prob_phish <= self.threshold_ben):
            return 0
        return 1
