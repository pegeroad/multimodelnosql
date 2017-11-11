from scipy import stats
import numpy as np
import math


class Statistics(object):
    @staticmethod
    def get_avg_of_list(list=[]):
        return np.mean(list)

    @staticmethod
    def get_standard_deviation_of_list(list=[]):
        return np.std(list)

    @staticmethod
    def get_confidence_intervall_of_list(mean, std, list=[]):
        R = stats.t.interval(0.95, len(list) - 1, loc=mean, scale=std / math.sqrt(len(list)))
        return R

    @staticmethod
    def get_min_of_list(list=[]):
        return np.min(list)

    @staticmethod
    def get_max_of_list(list=[]):
        return np.max(list)