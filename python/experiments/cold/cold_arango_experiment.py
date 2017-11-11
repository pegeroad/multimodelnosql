from experiments.abstract_experiment import *
from arango import *


class ColdArangoExperiment(AbstractExperiment):
    def __init__(self, experiment_name, iterations, arango_dao=ArangoDao):
        self.name = experiment_name
        self.dao = arango_dao
        self.iterations = iterations

    def do_experiment(self, reports={}):
        reports[self.name] = {}
        self.neighbor_test(reports, self.iterations)
        self.leaf_test(reports, self.iterations)
        self.statistic_test(reports, self.iterations)
        self.shortest_path_test(reports, self.iterations)
        self.distance_test(reports, self.iterations)

    def neighbor_test(self, reports, iterations):
        experiment_name = 'get_neighbors'
        self.experiment_wrapper(reports, iterations, experiment_name, self.dao.get_neighbors_for_node, "profiles/P19", "pokec")

    def leaf_test(self, reports, iterations):
        experiment_name = 'get_leaves'
        self.experiment_wrapper(reports, iterations, experiment_name, self.dao.get_leaves, "profiles", "relations")

    def statistic_test(self, reports, iterations):
        experiment_name = "get_age_statistics"
        self.experiment_wrapper(reports, iterations, experiment_name, self.dao.get_age_group_statistic, "profiles")

    def shortest_path_test(self, reports, iterations):
        experiment_name = "get_shortest_path"
        self.experiment_wrapper(reports, iterations, experiment_name,
                                self.dao.get_shortest_path, 'profiles/P25', 'profiles/P163', 'pokec')

    def distance_test(self, reports, iterations):
        experiment_name = "get_distance"
        self.experiment_wrapper(reports, iterations, experiment_name,
                                self.dao.get_distance, 'profiles/P25', 'profiles/P163', 'pokec')