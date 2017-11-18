# -*- encoding: utf-8 -*-

import os, datetime

BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
record_time = datetime.datetime.now().strftime('%Y-%m-%d')

email = '%s/email/logs/email-%s-record' % (BaseDir, record_time)

password_record = {
	'ssh': '%s/password/ssh/ssh-%s-record' % (BaseDir, record_time),
}