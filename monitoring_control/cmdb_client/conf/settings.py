# -*- encoding: utf-8 -*-

import os
BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

Params = {
	'server': '8.8.8.128',
	'port': 8000,
	'request_timeout': 30,
	
	'urls': {
		'asset_report_with_no_id': '/cmdb/asset/report/asset_with_no_asset_id/', # 没有资产id进行报告
		'asset_report': '/cmdb/asset/report/', # 资产id报告
	},
	
	'asset_id': '%s/var/.asset_id' % BaseDir,
	'log_file': '%s/logs/linux_run_log' % BaseDir,
	'windows_log_file': '%s\\logs\\windows_run_log' % BaseDir,

	'auth': {
		'user': 'jinxueyin@163.com',
		'token': 'abc',
	},

	'commit_interval': 3,
}