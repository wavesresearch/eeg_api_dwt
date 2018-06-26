# -*- coding: utf-8 -*-
from common_app.classifiers import rf, svm


classifiers = [lambda lp, lc: call_rf(lp, lc),
               lambda lp, lc: call_svm(lp, lc)]

def call_rf(lineData, lineClass):
    return rf.main(lineData, lineClass)


def call_svm(lineData, lineClass):
    return svm.main(lineData, lineClass)

