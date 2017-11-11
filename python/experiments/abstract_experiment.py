import abc

class AbstractExperiment(object):

    __metaclass__ = abc.ABCMeta

    name = None
    dao = None

    @abc.abstractmethod
    def do_experiment(self, reports={}):
        return

    def get_experiment_data(self, reports, experiment_name, experiment_function, *args):
        import inspect

        param_dict = {}
        i = 0
        param_names = inspect.getargspec(experiment_function).args
        while i < param_names.__len__() - 1:
            param_dict[param_names[i+1]] = args[i]
            i = i+1

        function_report_dict = {'function_name': experiment_function.func_name,
                                'function_parameters': param_dict, 'running_times': []}
        reports[self.name][experiment_name] = function_report_dict

    def experiment_time_wrapper(self, reports, experiment_name, experiment_function, *args):
        import time
        start_time = time.time()
        experiment_function(*args)
        end_time = time.time()
        reports[self.name][experiment_name]['running_times'].append(end_time-start_time)

    def experiment_wrapper(self, reports, iteratiorn, experiment_name, experiment_function, *args):
        self.get_experiment_data(reports, experiment_name, experiment_function, *args)
        for i in range(iteratiorn):
            self.experiment_time_wrapper(reports, experiment_name, experiment_function, *args)