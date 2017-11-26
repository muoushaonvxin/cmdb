# -*- encoding: utf-8 -*-
from django.conf.urls import url, include
from django.views.generic import TemplateView

urlpatterns = [
	# 监控控制台
    url(r'^control/$', TemplateView.as_view(template_name="monitor/control.html"), name="control"),

    # 监控 top 页面
	url(r'^top/$', TemplateView.as_view(template_name="monitor/top.html"), name="top"),

    # 监控 left 页面
	url(r'^left/$', TemplateView.as_view(template_name="monitor/left.html"), name="left"),

    # 监控 main 页面
	url(r'^main/$', TemplateView.as_view(template_name="monitor/main.html"), name="main"),

	# news
	url(r'^news/$', TemplateView.as_view(template_name="monitor/news.html"), name="news"),
]