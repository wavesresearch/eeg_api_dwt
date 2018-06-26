# -*- coding: utf-8 -*-
from common_app.serializers import CatalogsSerializer
from rest_framework.exceptions import APIException
from dwt.logic.classifier_selector import main as cs
from logger import Logger

TO_RESPONSE = ["id", "application_id", "name", "classifier", "accuracy", "energy_type",
               "channels", 'max_decomposition_level', 'min_channel_length']


def async_dwt(self, incoming_message):
    try:
        response = {}
        model_data = cs(incoming_message['data'])
        for key in model_data:
            incoming_message.update({key: model_data[key]})
        serializer = CatalogsSerializer(data=incoming_message)
        if serializer.is_valid():
            serializer.save()
            for key in TO_RESPONSE:
                response.update({key: serializer.data[key]})
        Logger().log(Logger.INFO, ACTION='{0}'.format(response), log_now=True)
    except Exception as e:
        Logger().log(Logger.ERROR, ERROR=""" {0}""".format(str(e)), ROUTE='async_dwt', log_now=True)
        raise APIException
