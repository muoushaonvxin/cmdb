from django.shortcuts import render, HttpResponse
from django.views.generic import View
import json
from .Controller import monitor_ctl, redis_conn, data_optimization, data_processing
from .models import Host
from users.models import UserProfile

# Create your views here.

class ClientConfig(View):
    def get(self, request, client_ip):
        client_obj = monitor_ctl.ClientHandler(client_ip)
        client_config = client_obj.fetch_configs()
        if client_config:
            return HttpResponse(json.dumps(client_config), content_type="application/json")


class DataReport(View):
    def post(self, request):
        print(request.POST)

        # 连接redis 的实例对象
        REDIS_OBJ = redis_conn.redis_conn()

        try:
            print('host=%s, service=%s' % (request.POST.get('client_ip'),request.POST.get('service_name')))

            # 对客户端汇报过来的数据进行存储
            data = json.loads(request.POST['data'])
            client_ip = request.POST.get('client_ip')
            service_name = request.POST.get('service_name')
            data_saveing_obj = data_optimization.DataStore(client_ip, service_name, data, REDIS_OBJ)

            # 获取触发器，并触发报警
            host_obj = Host.objects.get(ip_addr=client_ip)
            trigger_obj = monitor_ctl.GetTrigger(host_obj)
            service_triggers = trigger_obj.get_trigger_config()
            print("service trigger::", service_triggers)

            trigger_handler = data_processing.DataHandler(connect_redis=False)
            for trigger in service_triggers:
                trigger_handler.load_service_data_and_calulating(host_obj, trigger, REDIS_OBJ)

        except Exception as e:
            print('err --- >', str(e))

        return HttpResponse()