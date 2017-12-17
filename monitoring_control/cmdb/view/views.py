from django.shortcuts import render, HttpResponse
from django.views.generic import View
from cmdb.Controller import create_asset, check_token, date_encoder
from cmdb.models import Asset, Server, CPU, Disk, RAM, NIC, RaidAdaptor, NetworkDevice
from cmdb.models import NewAssetApprovalZone, Manufactory
import json


# 如果已经有资产了，就在这个方法里面进行汇报
class AssetReport(View):
	@check_token.token_required
	def get(self, request):
		return HttpResponse(json.dumps('---test---'), content_type="application/json")

	@check_token.token_required
	def post(self, request):
		ass_handler = create_asset.Asset(request)
		if ass_handler.data_is_valid():
			print('------ asset data valid: ')
			ass_handler.data_inject()
		return HttpResponse(json.dumps(ass_handler.response), content_type="application/json")


# 没有资产的机器使用客户端来汇报信息
class AssetWithNoAssetId(View):
	def get(self, request):
		return HttpResponse('---test---')

	def post(self, request):
		ass_handler = create_asset.Asset(request)
		res = ass_handler.get_asset_id_by_sn()
		return HttpResponse(json.dumps(res), content_type="application/json")


# 资产入库
class NewAssetsApproval(View):
	def get(self, request):
		ids = request.GET.get('ids')
		id_list = ids.split(',')
		new_assets = NewAssetApprovalZone.objects.filter(id__in=id_list)
		return render(request, 'cmdb/new_asset_approval.html', {'new_assets': new_assets})

	def post(self, request):
		print(request.POST)

		request.POST = request.POST.copy()
		approved_asset_list = request.POST.getlist('approved_asset_list')
		approved_asset_list = NewAssetApprovalZone.objects.filter(id__in=approved_asset_list)

		response_dic = {}

		for obj in approved_asset_list:
			request.POST['asset_data'] = obj.data
			ass_handler = create_asset.Asset(request)
			if ass_handler.data_is_valid_without_id():
				ass_handler.data_inject()
				obj.approved = True
				obj.save()
			response_dic[obj.id] = ass_handler.response

		return render(request, 'cmdb/new_asset_approval.html', {'new_assets': approved_asset_list,
																'response_dic': response_dic})





# 资产管理页面

class CmdbView(View):
    def get(self, request):
        return render(request, "cmdb/control.html")
















