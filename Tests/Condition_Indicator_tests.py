import numpy as np
from Operations import calculateRMS, calculateVariance, calculatePkPk, calculateCrestFactor, calculateCSum, \
    calculateKurtosis, calculateMean, calculateStdev
from collections import namedtuple
from numba import njit


def calculateMeantest(data_list_):
    mean_leading = calculateMean(data_list_)
    print("Mean point leading: ", mean_leading)
    mean_trailing = calculateMean(data_list_, 'trailing')
    print("Mean point trailing: ", mean_trailing)


def calculateRMStest(data_list_):
    rms_leading = calculateRMS(data_list_)
    print("RMS point leading: ", rms_leading)
    rms_trailing = calculateRMS(data_list_, 'trailing')
    print("RMS point trailing: ", rms_trailing)


def calculateVariancetest(data_list_):
    var = calculateVariance(data_list_)
    print("Variance point: ", var)


def calculateCrestFactortest(data_list_):
    cf_base = calculateCrestFactor(data_list_, 'base')
    cf_avg = calculateCrestFactor(data_list_, 'avg')
    cf_inter = calculateCrestFactor(data_list_, 'inter')

    print("CF point - base: ", cf_base)
    print("CF point - average: ", cf_avg)
    print("CF point - interpolated: ", cf_inter)

def calculatePkPktest(data_list_):
    pk_base = calculatePkPk(data_list_, 'base')
    pk_avg = calculatePkPk(data_list_, 'avg')
    pk_inter = calculatePkPk(data_list_, 'inter')

    print("Pk point - base: ", pk_base)
    print("Pk point - average: ", pk_avg)
    print("Pk point - interpolated: ", pk_inter)


def calculateKurtosistest(data_list_):
    kurt_ff = calculateKurtosis(data_list_, False)
    kurt_ft = calculateKurtosis(data_list_, True)
    print("Kurtosis point (Fisher False): ", kurt_ff)
    print("Kurtosis point (Fisher True): ", kurt_ft)


def calculateCSumtest(data_list_):
    c_sum = calculateCSum(data_list_)
    print("Cumulative Sum point: ", c_sum)


def calculateStdevtest(data_list_):
    stdev_leading = calculateStdev(data_list_)
    print("Stdev point leading: ", stdev_leading)
    stdev_trailing = calculateStdev(data_list_, 'trailing')
    print("Stdev point trailing: ", stdev_trailing)


# Main
DataPoint = namedtuple('DataPoint', ['value', 'timestamp'])

# Test data set (timestamp format just a placeholder)
data_point_add_1 = DataPoint(0.6, '2020-11-06 19:58:01.2800')
data_point_add_2 = DataPoint(0.7, '2020-11-06 19:58:02.2800')
data_point_add_3 = DataPoint(0.8, '2020-11-06 19:58:03.2800')
data_point_add_4 = DataPoint(-0.6, '2020-11-06 19:58:04.2800')
data_point_add_5 = DataPoint(-0.7, '2020-11-06 19:58:05.2800')
data_point_add_6 = DataPoint(-0.8, '2020-11-06 19:58:06.2800')
data_point_add_7 = DataPoint(1.0, '2020-11-06 19:58:07.2800')
data_point_add_8 = DataPoint(0.0, '2020-11-06 19:58:08.2800')

data_list_test = [data_point_add_1,
                  data_point_add_2,
                  data_point_add_3,
                  data_point_add_4,
                  data_point_add_5,
                  data_point_add_6,
                  data_point_add_7,
                  data_point_add_8]

calculateMeantest(data_list_test)

calculateRMStest(data_list_test)

calculateVariancetest(data_list_test)

calculateCrestFactortest(data_list_test)

calculatePkPktest(data_list_test)

calculateKurtosistest(data_list_test)

calculateCSumtest(data_list_test)

calculateStdevtest(data_list_test)

