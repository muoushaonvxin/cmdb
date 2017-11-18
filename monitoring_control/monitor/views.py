from django.shortcuts import render, HttpResponse
from django.views.generic import View
import json
# Create your views here.
from .Controller import monitorControll, redis_conn, data_optimization, data_processing
from monitor import models
from users import models


# 连接redis 的实例对象
REDIS_OBJ = redis_conn.redis_conn()

class Client_Config_View(View):
    def get(self, request, client_ip):
        client_obj = monitorControll.ClientHandler(client_ip)
        client_config = client_obj.fetch_configs()
        if client_config:
            print("客户端IP ---> {0}\n客户端配置 ---> {1}".format(client_ip, client_config))
            return HttpResponse(json.dumps(client_config), content_type="application/json")


class Service_Data_Report(View):
    def post(self, request):
        print(request.POST)
        try:
            print('host=%s, service=%s' % (request.POST.get('client_ip'), request.POST.get('service_name')))
            data = json.loads(request.POST['data'])
            client_ip = request.POST.get('client_ip')
            service_name = request.POST.get('service_name')
            data_save_obj = data_optimization.DataStore(client_ip, service_name, data, REDIS_OBJ)

            # 获取触发器，并触发报警
            host_obj = models.Host.objects.get(ip_addr=client_ip)
            trigger_obj = monitorControll.GetTrigger(host_obj)
            service_triggers = trigger_obj.get_trigger()
            
            trigger_handler = data_processing.DataHandler(settings, connect_redis=False)
            for trigger in service_triggers:
                trigger_handler.load_service_data_and_calulating(host_obj, trigger, REDIS_OBJ)
            print("service trigger::", service_triggers)
            
        except Exception as e:
            print('err --- >', e)

        return HttpResponse(json.dumps("-----report success-----"), content_type="application/json")





# 监控页面的数据展示

class MonitorView(View):
    def get(self, request):
        return render(request, "monitor/control.html", {})
