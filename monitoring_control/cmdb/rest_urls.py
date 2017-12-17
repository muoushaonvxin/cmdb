# -*- encoding: utf-8 -*-
from django.conf.urls import url, include
from cmdb.view.views import AssetReport, AssetWithNoAssetId, NewAssetsApproval

urlpatterns = [
    url(r'report/asset_with_no_asset_id/$', AssetWithNoAssetId.as_view()),

    url(r'report/$', AssetReport.as_view()),

    url(r'new_asset/approval/$', NewAssetsApproval.as_view()),
]
