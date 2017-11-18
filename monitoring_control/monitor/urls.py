from django.conf.urls import url, include
from monitor import rest_urls, page_urls

urlpatterns = [
	# 接受客户端发过来的数据
    url(r'api/', include(rest_urls), name="api"),

    # 监控页面的跳转
    url(r'page/', include(page_urls), name="page"),
]