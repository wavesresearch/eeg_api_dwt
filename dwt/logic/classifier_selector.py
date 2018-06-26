# -*- coding: utf-8 -*-
from logger import Logger
import pre_processing as pp
from common_app import call_method
from common_app.pre_processing import energy as en
from rest_framework.exceptions import APIException
import pickle
import numpy as np
import pywt
import warnings
warnings.filterwarnings("ignore")
MIN_LENGTH = 80
MIN_DWT_LEVEL = 4
ENERGY_TYPES = ['instantaneous', 'teager']


def get_dwt_values(minChannelLength):
    bior = pywt.Wavelet('bior2.2')
    maxDwtLevel = pywt.dwt_max_level(minChannelLength, bior)
    if minChannelLength < MIN_LENGTH:
        minChannelLength = MIN_LENGTH
        maxDwtLevel = MIN_DWT_LEVEL
    return maxDwtLevel, minChannelLength


def get_feats(dataTraining, maxDwtLevel, minChannelLength):
    channels = 0
    vecFeats = []
    for subject in dataTraining:
        subject = np.array(subject, np.float64)
        channels = subject.shape[1]
        vecFeat = pp.main(subject, maxDwtLevel, minChannelLength, channels)
        vecFeats.append(vecFeat)
    return vecFeats, channels


def selector(dataTraining, targetTraining):
    try:
        MIN_CHANNEL_LENGTH = 1000000
        for instance in dataTraining:
            instance = np.array(instance, np.float64)
            if instance.shape[0] < MIN_CHANNEL_LENGTH:
                MIN_CHANNEL_LENGTH = instance.shape[0]
        maxDwtLevel, minChannelLength = get_dwt_values(MIN_CHANNEL_LENGTH)
        classArray = []
        accuracyArray = []
        clfArray = []
        channels = 0
        etypeArray = []
        vecFeat, channels = get_feats(dataTraining, maxDwtLevel, minChannelLength)
        for classifier in call_method.classifiers:
            for energy in ENERGY_TYPES:
                Logger().log(Logger.INFO,
                             message='Process data with classifiers using energy_type {0}'.format(energy),
                             log_now=True)
                vec_feat_energy = en.get_energy(vecFeat, energy)
                results = classifier(vec_feat_energy, targetTraining)
                etypeArray.append(energy)
                classArray.append(results["classifier"])
                accuracyArray.append(results["accuracy"])
                clfArray.append(results["clf"])
        maxAccuracy = max(accuracyArray)
        pos = accuracyArray.index(maxAccuracy)
        bClassifier = classArray[pos]
        energy_t = etypeArray[pos]
        bestClf = clfArray[pos]
        model = pickle.dumps(bestClf)
        return {"model": model, "classifier": bClassifier, "accuracy": maxAccuracy, "energy_type": energy_t,
                "max_decomposition_level": maxDwtLevel, "min_channel_length": minChannelLength, "channels": channels}
    except Exception as e:
        Logger().log(Logger.ERROR, ERROR=""" {0}""".format(str(e)), ROUTE='classifier selector', log_now=True)
        return e


def main(request):
    try:
        dataTraining = request["data"]
        targetTraining = eval(request["target"])
        return selector(dataTraining, targetTraining)
    except Exception as e:
        Logger().log(Logger.ERROR, ERROR=""" {0}""".format(str(e)), ROUTE='classifier selector MAIN', log_now=True)
        raise APIException

