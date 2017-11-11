from experiments.abstract_experiment import *


class WarmCosmosExperiment(AbstractExperiment):
    def __init__(self, cosmos_dao, experiment_name):
        self.name = experiment_name
        self.dao = cosmos_dao

    def do_experiment(self, reports={}):
        print "cosmos experiment"
