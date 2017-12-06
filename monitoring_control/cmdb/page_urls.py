# -*- encoding: utf-8 -*-
from .asset_views import QueryAsset, QueryAssetDetailBySn, DeleteAssetBySn
from .views import CmdbView
from django.conf.urls import url, include
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^control/$', CmdbView.as_view()),

    # 监控 top 页面
	url(r'^top/$', TemplateView.as_view(template_name="cmdb/top.html"), name="top"),

    # 监控 left 页面
	url(r'^left/$', TemplateView.as_view(template_name="cmdb/left.html"), name="left"),

    # 监控 main 页面
	url(r'^main/$', TemplateView.as_view(template_name="cmdb/main.html"), name="main"),

	# 资产列表
	url(r'^asset_list/$', QueryAsset.as_view()),

	# 根据之臣id取得资产
	url(r'^query_asset_detail_by_sn/$', QueryAssetDetailBySn.as_view()),

	# 跳转资产详细信息
	url(r'^query_asset_detail/$', TemplateView.as_view(template_name="cmdb/query_asset_detail.html")),

	# 根据sn号删除资产
	url(r'^delete_asset/$', DeleteAssetBySn.as_view()),
]