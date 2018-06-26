# -*- coding: utf-8 -*-
from sklearn import svm
from sklearn.model_selection import cross_val_score
from logger import Logger
from rest_framework.exceptions import APIException
import warnings
warnings.filterwarnings("ignore")
C_F_V = 10


def main(dataTraining, targetTraining):
    try:
        clfArray = []
        meanScore = []
        kernels = ['linear', 'poly', 'rbf', 'sigmoid']
        for kernel in kernels:
            clf = svm.SVC(kernel=kernel, probability=True).fit(dataTraining, targetTraining)
            scores = cross_val_score(clf, dataTraining, targetTraining, cv=C_F_V)
            meanScore.append(scores.mean())
            clfArray.append(clf)
        maxScore = max(meanScore)
        position = meanScore.index(maxScore)
        bestKernel = kernels[position]
        bestClf = clfArray[position]
        Logger().log(Logger.INFO, message='{0} SVM classification result'.format(bestKernel),
                     accuracy=str(maxScore), log_now=True)
        return {"classifier": "{0} SVM".format(bestKernel), "accuracy": str(maxScore), "clf": bestClf}
    except Exception as e:
        Logger().log(Logger.ERROR, ERROR=""" {0}""".format(str(e)), log_now=True)
        raise APIException
