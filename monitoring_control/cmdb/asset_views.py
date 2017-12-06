# -*- encoding: utf-8 -*-
__author__ = "zhangyz"
__date__ = "2017/12/7 1:10"

from django.shortcuts import render, HttpResponse
from django.views.generic import View
from .Controller import create_asset, check_token, date_encoder
from .models import Asset, Server, CPU, Disk, RAM, NIC, RaidAdaptor, NetworkDevice
from .models import NewAssetApprovalZone, Manufactory
import json


class QueryAsset(View):
	'''
	查询当前的所有资产
	'''
	def get(self, request):
		asset_list = Asset.objects.all()
		return render(request, 'cmdb/query_assets.html', {'asset_list': asset_list})


class QueryAssetDetailBySn(View):
	def get(self, request):
		asset = request.GET.get("sn", "")

		try:
			asset = Asset.objects.get(sn=asset)
			manufactory = Manufactory.objects.get(id=asset.manufactory_id)

			asset_info = {
				"id": asset.id,
				"asset_type": asset.asset_type,
				"name": asset.name,
				"sn": asset.sn,
				"manufactory": manufactory.manufactory,
				"management_ip": asset.management_ip,
				"contract": asset.contract,
				"trade_date": asset.trade_date,
				"expire_date": asset.expire_date,
				"price": asset.price,
				"business_unit": asset.business_unit,
				"admin": asset.admin,
				"idc": asset.idc,
				"memo": asset.memo,
				"create_date": asset.create_date,
				"update_date": asset.update_date,
			}

			return HttpResponse(json.dumps(asset_info, cls=date_encoder.DateEncoder), content_type="application/json")
		except Exception as e:
			return HttpResponse(json.dumps(e), content_type="application/json")


# 根据sn号删除对应资产
class DeleteAssetBySn(View):
	def post(self, request):
		asset = request.POST.get("sn", "")

		if Asset.objects.get(sn=asset).delete():
			return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
		return HttpResponse(json.dumps({"status": "error"}), content_type="application/json")
