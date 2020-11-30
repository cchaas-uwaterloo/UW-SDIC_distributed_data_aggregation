import numpy as np
from scipy.signal import find_peaks
from collections import namedtuple
from scipy.stats import kurtosis
from numba import jit, cuda, njit


'''
brief : calculates the mean value of a set of data points
args :
data_list_ (list(namedtuple('dataPoint', ['value', 'timestamp']))) list of tuples with the data values and timestamps
stamp_value_ (string) default param, with no input argument, sets timestamp of returned point to leading edge of passed
                      list, set to 'trailing' to get trailing edge timestamp
returns : 
derived_point (namedtuple('dataPoint', ['value', 'timestamp'])) tuple with derived data value and timestamp 
'''


def calculateMean(data_list_, stamp_value_='leading'):
    if stamp_value_ == 'leading':
        timestamp = data_list_[0].timestamp
    else:
        timestamp = data_list_[(len(data_list_)-1)].timestamp

    value = getNPArrayCPU(data_list_)
    mean = np.mean(value)

    dataPoint = namedtuple('dataPoint', ['value', 'timestamp'])
    derived_point = dataPoint(mean, timestamp)

    return derived_point


'''
brief : calculates Root Mean Squared value of set of data points
args :
data_list_ (list(namedtuple('dataPoint', ['value', 'timestamp']))) list of tuples with the data values and timestamps
stamp_value_ (string) default param, with no input argument, sets timestamp of returned point to leading edge of passed
                      list, set to 'trailing' to get trailing edge timestamp
returns : 
derived_point (namedtuple('dataPoint', ['value', 'timestamp'])) tuple with derived data value and timestamp
'''


def calculateRMS(data_list_, stamp_value_='leading'):
    if stamp_value_ == 'leading':
        timestamp = data_list_[0].timestamp
    else:
        timestamp = data_list_[(len(data_list_) - 1)].timestamp

    value = getNPArrayCPU(data_list_)
    rms = np.sqrt(np.mean(value**2))

    dataPoint = namedtuple('dataPoint', ['value', 'timestamp'])
    derived_point = dataPoint(rms, timestamp)

    return derived_point


'''
brief : calculates variance of set of data points
args :
data_list_ (list(namedtuple('dataPoint', ['value', 'timestamp']))) list of tuples with the data values and timestamps
stamp_value_ (string) default param, with no input argument, sets timestamp of returned point to leading edge of passed
                      list, set to 'trailing' to get trailing edge timestamp
returns : 
derived_point (namedtuple('dataPoint', ['value', 'timestamp'])) tuple with derived data value and timestamp 
'''


def calculateVariance(data_list_, stamp_value_='leading'):
    if stamp_value_ == 'leading':
        timestamp = data_list_[0].timestamp
    else:
        timestamp = data_list_[(len(data_list_) - 1)].timestamp

    value = getNPArrayCPU(data_list_)
    var = np.var(value, dtype=np.float64)

    dataPoint = namedtuple('dataPoint', ['value', 'timestamp'])
    derived_point = dataPoint(var, timestamp)

    return derived_point


'''
brief : calculates Crest Factor value of set of data points
args :
data_list_ (list(namedtuple('dataPoint', ['value', 'timestamp']))) list of tuples with the data values and timestamps
mode_ (string) solution variation, options: base, avg (average), inter (interpolated)
stamp_value_ (string) default param, with no input argument, sets timestamp of returned point to leading edge of passed
                      list, set to 'trailing' to get trailing edge timestamp
returns : 
derived_point (namedtuple('dataPoint', ['value', 'timestamp'])) tuple with derived data value and timestamp
'''


def calculateCrestFactor(data_list_, mode_, stamp_value_='leading'):
    if stamp_value_ == 'leading':
        timestamp = data_list_[0].timestamp
    else:
        timestamp = data_list_[(len(data_list_) - 1)].timestamp

    value = getNPArrayCPU(data_list_)

    if mode_ == 'base':
        peak = np.max(np.abs(value))  # largest recorded absolute value
    if mode_ == 'avg':
        list_v = list(find_peaks(np.abs(value), 0)[1].values())[0]
        peak = sum(list_v)
        peak /= len(list_v)
    if mode_ == 'inter':
        peak = np.percentile(np.abs(value), 100.0, interpolation='midpoint')  # interpolated largest absolute value
    rms = np.sqrt(np.mean(value**2))

    crest_factor = peak/rms
    # crest_factor_db = 20 * np.log10(crest_factor)

    dataPoint = namedtuple('dataPoint', ['value', 'timestamp'])
    derived_point = dataPoint(crest_factor, timestamp)

    return derived_point


'''
brief : calculates Peak to Peak value of set of data points
args :
data_list_ (list(namedtuple('dataPoint', ['value', 'timestamp']))) list of tuples with the data values and timestamps
mode_ (string) solution variation, options: base, avg (average), inter (interpolated)
stamp_value_ (string) default param, with no input argument, sets timestamp of returned point to leading edge of passed
                      list, set to 'trailing' to get trailing edge timestamp
returns : 
derived_point (namedtuple('dataPoint', ['value', 'timestamp'])) tuple with derived data value and timestamp 
'''


def calculatePkPk(data_list_, mode_, stamp_value_='leading'):
    if stamp_value_ == 'leading':
        timestamp = data_list_[0].timestamp
    else:
        timestamp = data_list_[(len(data_list_) - 1)].timestamp

    value = getNPArrayCPU(data_list_)

    if mode_ == 'base':
        max_val = np.max(value)  # maximum recorded value
        min_val = np.min(value)  # minimum recorded value
    if mode_ == 'avg':
        list_v_p = list(find_peaks(value, 0)[1].values())[0]
        max_val = sum(list_v_p)
        max_val /= len(list_v_p)
        list_v_n = list(find_peaks((-value), 0)[1].values())[0]
        min_val = sum(list_v_n)
        min_val /= len(list_v_n)
        min_val *= -1
    if mode_ == 'inter':
        max_val = np.percentile(value, 100.0, interpolation='midpoint')
        min_val = np.percentile((-value), 100.0, interpolation='midpoint')
        min_val *= -1

    ptp = max_val - min_val

    dataPoint = namedtuple('dataPoint', ['value', 'timestamp'])
    derived_point = dataPoint(ptp, timestamp)

    return derived_point


'''
brief : calculates Kurtosis value of set of data points
args :
data_list_ (list(namedtuple('dataPoint', ['value', 'timestamp']))) list of tuples with the data values and timestamps
stamp_value_ (string) default param, with no input argument, sets timestamp of returned point to leading edge of passed
                      list, set to 'trailing' to get trailing edge timestamp
returns : 
derived_point (namedtuple('dataPoint', ['value', 'timestamp'])) tuple with derived data value and timestamp 
'''


def calculateKurtosis(data_list_, fisher_, stamp_value_='leading'):
    if stamp_value_ == 'leading':
        timestamp = data_list_[0].timestamp
    else:
        timestamp = data_list_[(len(data_list_) - 1)].timestamp

    value = getNPArrayCPU(data_list_)

    kur = kurtosis(value, fisher=fisher_)

    dataPoint = namedtuple('dataPoint', ['value', 'timestamp'])
    derived_point = dataPoint(kur, timestamp)

    return derived_point


'''
brief : calculates Cumulative Sum value of set of data points
args :
data_list_ (list(namedtuple('dataPoint', ['value', 'timestamp']))) list of tuples with the data values and timestamps
stamp_value_ (string) default param, with no input argument, sets timestamp of returned point to leading edge of passed
                      list, set to 'trailing' to get trailing edge timestamp
returns : 
derived_point (namedtuple('dataPoint', ['value', 'timestamp'])) tuple with derived data value and timestamp 
'''


def calculateCSum(data_list_, stamp_value_='leading'):
    if stamp_value_ == 'leading':
        timestamp = data_list_[0].timestamp
    else:
        timestamp = data_list_[(len(data_list_) - 1)].timestamp

    value = getNPArrayCPU(data_list_)

    c_sum_arr = np.cumsum(value)
    length = len(c_sum_arr)
    c_sum = c_sum_arr[length-1]

    dataPoint = namedtuple('dataPoint', ['value', 'timestamp'])
    derived_point = dataPoint(c_sum, timestamp)

    return derived_point


'''
brief : calculates the standard deviation of a set of points
args :
data_list_ (list(namedtuple('dataPoint', ['value', 'timestamp']))) list of tuples with the data values and timestamps
stamp_value_ (string) default param, with no input argument, sets timestamp of returned point to leading edge of passed
                      list, set to 'trailing' to get trailing edge timestamp
returns : 
derived_point (namedtuple('dataPoint', ['value', 'timestamp'])) tuple with derived data value and timestamp 
'''


def calculateStdev(data_list_, stamp_value_='leading'):
    if stamp_value_ == 'leading':
        timestamp = data_list_[0].timestamp
    else:
        timestamp = data_list_[(len(data_list_)-1)].timestamp

    value = getNPArrayCPU(data_list_)
    stdev = np.std(value)

    dataPoint = namedtuple('dataPoint', ['value', 'timestamp'])
    derived_point = dataPoint(stdev, timestamp)

    return derived_point


@njit
def getNPArrayGPU(data_list_):
    arr = np.empty(len(data_list_))
    for point_index, point in enumerate(data_list_):
        arr[point_index] = point.value
    return arr


def getNPArrayCPU(data_list_):
    arr = np.empty(len(data_list_))
    for point_index, point in enumerate(data_list_):
        arr[point_index] = point.value
    return arr
