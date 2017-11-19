from experiments.warm.warm_arango_experiment import *
from experiments.warm.warm_orient_experiment import *
from reporting.report_generator import ReportGenerator
from runners.experiment_runner import *


def pwd():
    import os
    return os.path.dirname(os.path.realpath(__file__))


def str2bool(v):
    import argparse
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser(prog='Multi Model DB performance tester',
                                     description='Runs performance tests against ArangoDB and OrientDB')
    parser.add_argument('name', help='name of the test')
    parser.add_argument('--cold_test', help='runs cold tests', type=str2bool, default=False)
    parser.add_argument('--warm_test', help='runs warm tests', type=str2bool, default=False)
    parser.add_argument('--volume_test', help='runs volume tests', type=str2bool, default=False)
    args = parser.parse_args()
    test_name = args.name
    cold_test = args.cold_test
    warm_test = args.warm_test
    volume_test = args.volume_test
    if (cold_test and warm_test) or (cold_test and volume_test):
        raise argparse.ArgumentTypeError(
            "Cold tests can't be executed with warm tests without restarting the database servers.")
    return cold_test, test_name, volume_test, warm_test


def main():
    cold_test, test_name, volume_test, warm_test = parse_arguments()

    #create dao-s
    arango_dao = ArangoDao("http://52.232.62.29:8529", "_system", "root", "root")
    orient_dao = OrientDao("plocal:pokec", "52.232.67.219")

    #create tests
    cold_arango_experiment = ColdArangoExperiment("cold_arango", 5, arango_dao)
    cold_orient_experiment = ColdOrientExperiment("cold_orient", 5, orient_dao)

    warm_arango_experiment = WarmArangoExperiment("warm_arango", 5, arango_dao)
    warm_orient_experiment = WarmOrientExperiment("warm_orient", 5, orient_dao)

    volume_arango_experiment = WarmArangoExperiment("large_volume_arango", 100, arango_dao)
    volume_orient_experiment = WarmOrientExperiment("large_volume_orient", 100, orient_dao)

    experiments = []

    if cold_test:
        print "run cold tests"
        experiments.append(cold_arango_experiment)
        experiments.append(cold_orient_experiment)

    if warm_test:
        print "run warm tests"
        experiments.append(warm_arango_experiment)
        experiments.append(warm_orient_experiment)

    if volume_test:
        print "run volume tests"
        experiments.append(volume_arango_experiment)
        experiments.append(volume_orient_experiment)

    # run tests
    runner = ExperimentRunner(experiments)
    runner.run_experiments()

    # create report
    report_generator = ReportGenerator(
        pwd() + '/results/' + str(test_name) + '_results.json', runner.report)

    report_generator.write_statistics_into_report()
    #save report
    report_generator.save_report_as_json_file()


if __name__ == "__main__":
    main()
