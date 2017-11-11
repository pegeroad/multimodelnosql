from statistics import Statistics


class ReportGenerator(object):

    def __init__(self, reports={}):
        self.reports = reports

    def get_running_time_list_from_report(self, db_experiment_name, experiment_name):
        return self.reports[db_experiment_name][experiment_name]['running_times']

    def filter_values_from_list_excluded_by_intervall(self, list=[], intervall=()):
        return [val for val in list if val < intervall[0] or val > intervall[1]]

    def write_statistics_into_report(self):
        for ok,ov in self.reports.items():
            for ik in ov:
                time_list = self.get_running_time_list_from_report(ok, ik)
                mean, std, min, max = Statistics.get_avg_of_list(time_list), Statistics.get_standard_deviation_of_list(time_list), \
                                      Statistics.get_min_of_list(time_list),Statistics.get_max_of_list(time_list)

                confidence_intervall = Statistics.get_confidence_intervall_of_list(mean, std, time_list)
                filtered_list = self.filter_values_from_list_excluded_by_intervall(time_list, confidence_intervall)
                self.reports[ok][ik]['averrage'] = mean
                self.reports[ok][ik]['deviation'] = std
                self.reports[ok][ik]['confidence_intervall'] = confidence_intervall
                self.reports[ok][ik]['min'] = min
                self.reports[ok][ik]['max'] = max
                self.reports[ok][ik]['excluded_by_confidence_intervall'] = filtered_list
