# -*- encoding: utf-8 -*-
import subprocess

def monitor():
	try:
		shell_command = ''
		result = subprocess.Popen(shell_command,shell=True,stdout=subprocess.PIPE).stdout.readlines()

		value_dict = {'status': 0, 'data': {}}
	except Exception as e:
		value_dict = {'status': 250, 'data': {}}
		return value_dict
	return value_dict
		

