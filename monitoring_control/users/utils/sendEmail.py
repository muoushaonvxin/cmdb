# -*- encoding: utf-8 -*-
from random import Random
from users.models import EmailVerifyRecord

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
    	str += chars[random.randint(0, length)]
    return str


def send_email(email, send_type='notify'):
	email_record = EmailVerifyRecord()
	code = random_str(16)
	email_record.code = code
	email_record.email = email
	email_record.send_type = send_type
	email_record.save()

	email_title = ""
	email_body = ""

	if send_type == "nitify":
		email_title = '报警通知'
		email_body = '请查看控制台'
		