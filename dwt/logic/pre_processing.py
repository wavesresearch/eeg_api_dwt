# -*- coding: utf-8 -*-
from __future__ import division
import pywt
import numpy as np
from rest_framework.exceptions import APIException
from logger import Logger
import warnings
warnings.filterwarnings("ignore")


def main(subject, maxDwtLevel, minChannelLen, cN):
    try:
        channels = CAR(subject, cN)
        return processing(channels, cN, maxDwtLevel, minChannelLen)
    except Exception as e:
        Logger().log(Logger.ERROR, ERROR=""" {0}""".format(str(e)), ROUTE="pp main", log_now=True)
        raise APIException


def processing(channels, cN, maxDwtLevel, minChannelLen):
    try:
        dwt_values = []
        for x in xrange(0, cN):
            dataChannel = []
            for channel in channels[:, x]:
                dataChannel.append(channel)
            [dataChannel.append(0) for _ in xrange(len(dataChannel), minChannelLen)
             if len(dataChannel) < minChannelLen]
            dwtValues = pywt.wavedec(dataChannel, 'bior2.2', level=maxDwtLevel)
            dwt_values.append(dwtValues)
        return dwt_values
    except Exception as e:
        Logger().log(Logger.ERROR, ERROR=""" {0}""".format(str(e)), ROUTE="pp processing", log_now=True)
        return e


def CAR(channels, cN):
    try:
        tam = channels.shape[0]
        for x in xrange(0, tam):
            channels[x, 0:cN] = np.array(channels[x, 0:cN] - (1 / cN) * sum(channels[x, 0:cN]))
        return channels
    except Exception as e:
        Logger().log(Logger.ERROR, ERROR=""" {0}""".format(str(e)), log_now=True)
        return e

