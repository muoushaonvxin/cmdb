# -*- coding: utf8 -*-

import datetime
from tools.log.settings import email, password_record

def make_log_email(msg):
	with open(email, 'a+') as f:
		f.write(msg)
	f.close()


def make_log_ssh(msg):
	with open(password_record['ssh'], 'a+') as f:
		f.write(msg)
	f.close()