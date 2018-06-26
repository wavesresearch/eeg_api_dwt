# -*- coding: utf-8 -*-
from __future__ import division
import math
import numpy as np
from logger import Logger
from rest_framework.exceptions import APIException
import warnings
warnings.filterwarnings("ignore")


def get_energy(dataTraining, energy_type):
    try:
        feats = []
        for subject in dataTraining:
            energyValues = []
            for channel in subject:
                energyValues += eval(energy_type)(channel)
            feats.append(energyValues)
        return feats
    except Exception as e:
        Logger().log(Logger.ERROR, ERROR=""" {0}""".format(str(e)), ROUTE="get_energy", log_now=True)
        raise APIException


def instantaneous(c_data):
    try:
        IE = []
        for data in c_data:
            IE.append(np.log10((float(1) / float(len(data))) * float(sum(i ** 2 for i in data))))
        return IE
    except Exception as e:
        Logger().log(Logger.ERROR, ERROR=""" {0}""".format(str(e)), log_now=True)
        return e


def teager(c_data):
    try:
        TE = []
        for data in c_data:
            sum_values = sum(abs(data[x]**2) if x == 0
                             else abs(data[x]**2 - data[x - 1] * data[x + 1])
                             for x in xrange(0, len(data) - 1))
            TE.append(np.log10((float(1) / float(len(data))) * float(sum_values)))
        return TE
    except Exception as e:
        Logger().log(Logger.ERROR, ERROR=""" {0}""".format(str(e)), log_now=True)
        return e
