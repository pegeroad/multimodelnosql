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
        if args.__len__() > 0:
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
        result = None
        if args.__len__() > 0:
            result = experiment_function(*args)
        else:
            result = experiment_function()
        end_time = time.time()
        reports[self.name][experiment_name]['running_times'].append(end_time-start_time)

    def experiment_wrapper(self, reports, iteration, experiment_name, experiment_function, *args):
        print "Run " + self.name + ":" + experiment_name
        self.get_experiment_data(reports, experiment_name, experiment_function, *args)
        for i in range(iteration):
            self.experiment_time_wrapper(reports, experiment_name, experiment_function, *args)

    def validate_number_of_data(self):
        # original number of edges and nodes according to the
        # pokec data set: https://snap.stanford.edu/data/soc-pokec.html
        node_number = 1632803
        edge_number = 30622564
        # the fault tolerance of the difference in percent
        tolerance = 1.0
        actual_edge_numb = self.dao.get_edge_count()
        actual_node_numb = self.dao.get_node_count()

        node_ratio = (actual_node_numb / float(node_number)) * 100
        edge_ratio = (actual_edge_numb / float(edge_number)) * 100

        if not ((node_ratio > 100 - tolerance) and (edge_ratio > 100 - tolerance)):
            raise ValueError("Data set is incorrect, not enough number of edges or nodes was provided.")
