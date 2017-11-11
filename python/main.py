from experiments.cold.cold_cosmos_experiment import *

from experiments.cold.cold_orient_experiment import *
from experiments.warm.warm_arango_experiment import *
from reporting.report_generator import ReportGenerator
from runners.experiment_runner import *


def main():
    arango_dao = ArangoDao("http://<ip>:8529", "_system", "??", "??")

    cold_arangoexperiment = ColdArangoExperiment("cold_arango", 5, arango_dao)
    cold_orientexperiment = ColdOrientExperiment("cold_orient", None)
    cold_cosmosexperiment = ColdCosmosExperiment("cold_cosmos", None)

    warm_arangoexperiment = WarmArangoExperiment("warm_arango", 5, arango_dao)

    volume_arangoexperiment = WarmArangoExperiment("large_volume_arango", 100, arango_dao)


    experiments = []

    experiments.append(cold_arangoexperiment)
    experiments.append(cold_orientexperiment)
    experiments.append(cold_cosmosexperiment)

    experiments.append(warm_arangoexperiment)

    experiments.append(volume_arangoexperiment)

    runner = ExperimentRunner(experiments)

    runner.run_experiments()

    #print runner.report


    report_generator = ReportGenerator(runner.report)

    report_generator.write_statistics_into_report()

    print report_generator.reports


main()