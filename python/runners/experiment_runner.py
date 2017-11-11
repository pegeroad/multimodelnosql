from abstract_experiment_runner import *


class ExperimentRunner(AbstractExperimentRunner):

    def run_experiments(self):
        for experiment in self.experiments:
            experiment.do_experiment(self.report)