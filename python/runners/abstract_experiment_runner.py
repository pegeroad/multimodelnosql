import abc


class AbstractExperimentRunner(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, experiments):
        self.experiments = experiments
        self.report = {}

    @abc.abstractmethod
    def run_experiments(self):
        return
