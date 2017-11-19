from dao.orient import *
from experiments.abstract_experiment import *


class ColdOrientExperiment(AbstractExperiment):
    def __init__(self, experiment_name, iterations, orient_dao=OrientDao):
        self.name = experiment_name
        self.dao = orient_dao
        self.iterations = iterations

    def do_experiment(self, reports={}):
        reports[self.name] = {}
        self.validate_number_of_data()
        self.neighbor_test(reports, self.iterations)
        self.leaf_test(reports, self.iterations)
        self.statistic_test(reports, self.iterations)
        self.shortest_path_test(reports, self.iterations)
        self.distance_test(reports, self.iterations)

    def neighbor_test(self, reports, iterations):
        experiment_name = 'get_neighbors'
        self.experiment_wrapper(reports, iterations, experiment_name, self.dao.get_neighbors_for_node, 'P19', 'Relation')

    def leaf_test(self, reports, iterations):
        experiment_name = 'get_leaves'
        self.experiment_wrapper(reports, iterations, experiment_name, self.dao.get_leaves, "Profile", "Relation")

    def statistic_test(self, reports, iterations):
        experiment_name = "get_age_statistics"
        self.experiment_wrapper(reports, iterations, experiment_name, self.dao.get_age_group_statistic, "Profile")

    def shortest_path_test(self, reports, iterations):
        experiment_name = "get_shortest_path"
        self.experiment_wrapper(reports, iterations, experiment_name,
                                self.dao.get_shortest_path, 'P1554217', 'P891887', 'Profile')

    def distance_test(self, reports, iterations):
        experiment_name = "get_distance"
        self.experiment_wrapper(reports, iterations, experiment_name,
                                self.dao.get_distance, 'P1554217', 'P891887', 'Profile')