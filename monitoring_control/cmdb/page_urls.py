# -*- encoding: utf-8 -*-
from django.conf.urls import url, include
from .views import CmdbView

urlpatterns = [
    url(r'^main/$', CmdbView.as_view()),
]