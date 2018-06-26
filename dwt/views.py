# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from logger import Logger
from rest_framework.views import APIView
from common_app.serializers import (RequestValidator, CatalogValidator)
from rest_framework import status
from rest_framework.response import Response
from dwt.logic.async_process import async_dwt
from dwt.logic import new_entry
import threading


class DWTTraining(APIView):
    """
    Training a model with feature extraction based on Discrete Wavelet Transform
    """

    def post(self, request):
        """

        :param request:
        :return:
        """
        try:
            Logger().clear_default_params()
            Logger().log(
                Logger.INFO, message='DWT endpoint called: POST method', req='eeg/dwt/training', log_now=True)
            incoming_data = request.data
            if self.validate_params(incoming_data):
                validate = {"application_id": incoming_data['application_id']}
                req_serializer = RequestValidator(data=validate)
                if req_serializer.is_valid():
                    t = threading.Thread(target=async_dwt, args=(self, incoming_data))
                    t.setDaemon(False)
                    t.start()
                    Logger().log(Logger.INFO, ACTION='ACCEPTED Data', log_now=True)
                    return Response(status=status.HTTP_202_ACCEPTED)
            Logger().log(Logger.ERROR, ACTION='An Error occurred:',
                         log_now=True)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            Logger().log(Logger.ERROR, ACTION='An Error occurred with : ' + e.message,
                         log_now=True)
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def validate_params(cls, data):
        requested_params = ['application_id', 'name', 'data']
        if all(param in data for param in requested_params):
            return True
        else:
            return False


class DWT(APIView):
    """
    Using the best classifier for a new entry
    """
    def post(self, request, pk):
        """

        :param request:
        :param pk: catalog(classifier) id
        :return: {catalogId, pClass, predict_proba}
        """
        try:
            responseC = {}
            incoming_data = eval(request.body)
            if self.validate_params(incoming_data):
                message = incoming_data["entry"]
                validate = {"catalog_id": pk}
                req_serializer = CatalogValidator(data=validate)
                if req_serializer.is_valid():
                    responseC = new_entry.main(message, pk)
                    Logger().log(Logger.INFO, INFO=""" {0}""".format(responseC), log_now=True)
                    return Response(responseC, status=status.HTTP_200_OK)
            return Response(responseC, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            Logger().log(Logger.ERROR, ERROR=""" {0}""".format(str(e)), ROUTE="Dwt", log_now=True)
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def validate_params(cls, data):
        requested_params = ['entry']
        if all(param in data for param in requested_params):
            return True
        else:
            return False
