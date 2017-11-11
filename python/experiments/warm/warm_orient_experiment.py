from experiments.abstract_experiment import *
from orient import *


class WarmOrientExperiment(AbstractExperiment):
    def __init__(self, experiment_name, orient_dao=OrientDao):
        self.name = experiment_name
        self.dao = orient_dao

    def do_experiment(self, reports={}):
        return

