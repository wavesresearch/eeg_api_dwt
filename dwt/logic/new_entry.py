# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from common_app.models import Catalogs
from common_app.pre_processing import energy as en
from logger import Logger
from classifier_selector import get_feats
import numpy as np
import pickle
import warnings
warnings.filterwarnings("ignore")


def main(entries, pk):
    try:
        Logger().log(Logger.INFO, ACTION='Incoming new event', EVENT=pk, log_now=True)
        response_params = {}
        model = Catalogs.objects.get(pk=pk).model
        maxDwtLevel = Catalogs.objects.get(pk=pk).max_decomposition_level
        minChannelLength = Catalogs.objects.get(pk=pk).min_channel_length
        channels = Catalogs.objects.get(pk=pk).channels
        energy = Catalogs.objects.get(pk=pk).energy_type
        clf = pickle.loads(model)
        for entry in entries:
            entryNp = np.array(entry, np.float64)
            if channels == entryNp.shape[1]:
                vecFeat, channelsTmp = get_feats([entry], maxDwtLevel, minChannelLength)
                vec_feat_energy = en.get_energy(vecFeat, energy)
                prediction = clf.predict(vec_feat_energy)
                accuracyP = max(max(clf.predict_proba(vec_feat_energy)))
                response_params = {
                    "catalog_id": pk,
                    "class": prediction[0],
                    "predicted_prob": accuracyP
                }
        return response_params
    except Exception as e:
        Logger().log(Logger.ERROR, ERROR=""" {0}""".format(str(e)), ROUTE="DWT NewMsg main", log_now=True)
        return e
