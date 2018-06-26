# -*- coding: utf-8 -*-
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from logger import Logger
from rest_framework.exceptions import APIException
import warnings
warnings.filterwarnings("ignore")
DEPTHS = [2, 3, 4, 5, 6, 7, 8]
RANDOM_STATE = 0
C_F_V = 10


def main(dataTraining, targetTraining):
    try:
        clfArray = []
        meanScore = []
        for depth in DEPTHS:
            clf = RandomForestClassifier(max_depth=depth, random_state=RANDOM_STATE, criterion='gini'
                                         ).fit(dataTraining, targetTraining)
            scores = cross_val_score(clf, dataTraining, targetTraining, cv=C_F_V)
            meanScore.append(scores.mean())
            clfArray.append(clf)
        maxScore = max(meanScore)
        position = meanScore.index(maxScore)
        bestDepth = DEPTHS[position]
        bestClf = clfArray[position]
        Logger().log(Logger.INFO, message='RandomForest depth {0} classification result'.format(bestDepth),
                     accuracy=str(maxScore), log_now=True)
        return {"classifier": "RandomForest depth {0}".format(str(bestDepth)), "accuracy": str(maxScore), "clf": bestClf}
    except Exception as e:
        Logger().log(Logger.ERROR, ERROR=""" {0}""".format(str(e)), log_now=True)
        raise APIException
