import time, threading, json
import requests
from conf import settings
from plugins import plugin_api
import json


class ClientHandlers(object):


    def __init__(self):
        self.monitor_services = {}


    def forever_run(self):
        exit_flag = False
        config_latest_update_time = 0

        while not exit_flag:
            if time.time() - config_latest_update_time > settings.configs["ConfigUpdateInterval"]:
                self.load_latest_config()
                print("Latest_config:", self.monitor_services)
                config_latest_update_time = time.time()

            for service_name, val in self.monitor_services["services"].items():
                if len(val) == 2:
                    self.monitor_services["services"][service_name].append(0)

                monitor_interval = val[1]
                last_invoke_time = val[2]

                if time.time() - last_invoke_time > monitor_interval:
                    print("---->", last_invoke_time, "---->", time.time())
                    self.monitor_services["services"][service_name][2] = time.time()
                    t = threading.Thread(target=self.invoke_plugin, args=(service_name, val))
                    t.start()
                    print("start monitor service: [{ServiceName}]".format(ServiceName=service_name))
                else:
                    print("Going to monitor service [{ServiceName}] in [{interval}] secs".format(ServiceName=service_name, interval=monitor_interval - (time.time() - last_invoke_time)))
                    time.sleep(1)


    def load_latest_config(self):
        '''
        从服务端获取最新的监控配置
        '''
        request_type = settings.configs["urls"]["get_configs"][1]
        request_url = "%s/%s" % (settings.configs["urls"]["get_configs"][0], settings.configs["HostIP"])
        latest_config = self.url_request(request_type, request_url)
        latest_config = json.loads(latest_config)
        self.monitor_services.update(latest_config)


    def invoke_plugin(self, service_name, val):
        # 获取插件名称
        plugin_name = val[0]

        if hasattr(plugin_api, plugin_name):
            func = getattr(plugin_api, plugin_name)
            plugin_callback = func()

            report_data = {
                "client_ip": settings.configs['HostIP'],
                "service_name": service_name,
                "data": json.dumps(plugin_callback),
            }

            request_action = settings.configs["urls"]["service_report"][1]
            request_url = settings.configs["urls"]["service_report"][0]
            self.url_request(request_action, request_url, params=report_data)
        else:
            print("\033[31mCannot find service [%s]' plugin name [%s] in plugin_api\033[0m" % (service_name, plugin_name))


    def url_request(self, action, request_url, **extra_data):
        abs_url = "http://{ip_addr}:{port}/{url}".format(ip_addr=settings.configs["Server"],
                                                         port=settings.configs["ServerPort"],
                                                         url=request_url
                                                         )

        # print("\033[31m{abs_url}\033[0m".format(abs_url=abs_url), type(extra_data), extra_data)

        if action in ('get', "GET"):
            try:
                r = requests.get(abs_url, timeout=settings.configs["request_timeout"])
                r_data = r.json()
                return r_data
            except requests.RequestException as e:
                print(e)

        elif action in ('post', 'POST'):
            try:
                data = json.dumps(extra_data['params'])
                # r = requests.post(url=abs_url, data=extra_data["params"])
                r = requests.post(url=abs_url, data=data)
                r_data = r.json()
                print("\033[31;1m[%s]:[%s]\033[0m response:\n%s,%s" % (action, abs_url, r_data, data))
                return r_data
            except Exception as e:
                print(e)

























