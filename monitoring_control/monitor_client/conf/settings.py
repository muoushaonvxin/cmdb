configs = {
    'HostIP': '8.8.8.129',
    'Server': '8.8.8.128',
    'ServerPort': 8000,
    'urls': {
        'get_configs': ['monitor/api/client/config', 'get'],
        'service_report': ['monitor/api/client/service/report/', 'post'],
    },
    'RequestTimeout': 30,
    'ConfigUpdateInterval': 300,
}
