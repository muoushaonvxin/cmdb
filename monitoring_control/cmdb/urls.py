from django.conf.urls import url, include
from cmdb import page_urls
from cmdb import rest_urls

urlpatterns = [
	url(r'^asset', include(rest_urls), name="asset"),

	# cmdb 资产管理页面的跳转
    url(r'^page/', include(page_urls), name="page"),
]






























