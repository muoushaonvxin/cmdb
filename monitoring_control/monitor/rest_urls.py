# -*- encoding: utf-8 -*-
from django.conf.urls import url, include
from monitor.view.views import ClientConfig, DataReport

urlpatterns = [
    # 客户端通过将自己的ip地址汇报过来，获取需要被监控的配置
    url(r'client/config/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/$', ClientConfig.as_view()),

    # 监控客户端将收集到的信息汇报给服务端
    url(r'client/service/report/$', DataReport.as_view()),
]