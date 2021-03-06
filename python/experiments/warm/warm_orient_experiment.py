from dao.orient import *
from experiments.cold.cold_orient_experiment import ColdOrientExperiment


class WarmOrientExperiment(ColdOrientExperiment):
    def __init__(self, experiment_name, iterations, orient_dao=OrientDao):
        self.name = experiment_name
        self.dao = orient_dao
        self.iterations = iterations

    def do_experiment(self, reports={}):
        reports[self.name] = {}
        self.validate_number_of_data()
        self.neighbor_test(reports, 1)
        self.neighbor_test(reports, self.iterations)
        self.leaf_test(reports, 1)
        self.leaf_test(reports, self.iterations)
        self.statistic_test(reports, 1)
        self.statistic_test(reports, self.iterations)
        self.shortest_path_test(reports, 1)
        self.shortest_path_test(reports, self.iterations)
        self.distance_test(reports, 1)
        self.distance_test(reports, self.iterations)

