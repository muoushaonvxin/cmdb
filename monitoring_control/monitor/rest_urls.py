# -*- encoding: utf-8 -*-
from django.conf.urls import url, include
from .views import Client_Config_View, Service_Data_Report

urlpatterns = [
    url(r'client/config/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/$', Client_Config_View.as_view()),
    url(r'client/service/report/$', Service_Data_Report.as_view()),
]