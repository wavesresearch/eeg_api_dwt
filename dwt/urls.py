# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dwt/training$', views.DWTTraining.as_view()),
    url(r'^dwt/(?P<pk>[0-9]+)$', views.DWT.as_view()),
]
