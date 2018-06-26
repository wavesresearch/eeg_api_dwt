# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from common_app.models import (Catalogs, Applications)
import warnings
warnings.filterwarnings("ignore")


class CatalogsSerializer(serializers.ModelSerializer):
    application_id = serializers.PrimaryKeyRelatedField(source='application', many=False,
                                                        queryset=Applications.objects.all())

    class Meta:
        model = Catalogs
        fields = ('id', 'application_id', 'name', 'accuracy', 'classifier', 'energy_type', 'max_decomposition_level',
                  'min_channel_length', 'model', 'channels')


class HHTCatalogsSerializer(serializers.ModelSerializer):
    application_id = serializers.PrimaryKeyRelatedField(source='application', many=False,
                                                        queryset=Applications.objects.all())

    class Meta:
        model = Catalogs
        fields = ('id', 'application_id', 'name', 'accuracy', 'classifier', 'energy_type', 'model', 'channels')


class RequestValidator(serializers.Serializer):
    application_id = serializers.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super(RequestValidator, self).__init__(*args, **kwargs)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate(self, attrs):
        try:
            application_id = Applications.objects.get(pk=attrs['application_id'])
        except Applications.DoesNotExist:
            ex = ValidationError('Application does not exist')
            raise ex
        return attrs


class CatalogValidator(serializers.Serializer):
    catalog_id = serializers.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super(CatalogValidator, self).__init__(*args, **kwargs)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate(self, attrs):
        try:
            application_id = Catalogs.objects.get(pk=attrs['catalog_id'])
        except Catalogs.DoesNotExist:
            ex = ValidationError('Catalog does not exist')
            raise ex
        return attrs


