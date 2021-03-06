# -*- encoding: utf-8 -*-
import json
import hashlib
import time
from django.shortcuts import render, HttpResponse
from monitoring_control import settings
from users.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist


def json_date_handler(obj):
	if hasattr(obj, 'isoformat'):
		return obj.strftime("%Y-%m-%d")


def json_datetime_handler(obj):
	if hasattr(obj, 'isoformat'):
		return obj.strftime("%Y-%m-%d %H:%M:%S")


def gen_token(username, timestamp, token):
	token_format = "%s\n%s\n%s" % (username, timestamp, token)
	obj = hashlib.md5() 
	obj.update(token_format.encode())
	print(obj)
	return obj.hexdigest()[10:17]


def token_required(func):
	def wrapper(*args, **kwargs):
		response = {
			"errors": []
		}

		get_args = args[1].GET
		username = get_args.get("user")
		token_md5_from_client = get_args.get("token")
		timestamp = get_args.get("timestamp")

		if not username or not timestamp or not token_md5_from_client:
			response['errors'].append({"auth_failed": "This api requires token authentication!"})
			return HttpResponse(json.dumps(response), content_type="application/json")

		try:
			user_obj = UserProfile.objects.get(email=username)
			token_md5_from_server = gen_token(username, timestamp, user_obj.token)
			if token_md5_from_client != token_md5_from_server:
				response['errors'].append({"auth_failed": "Invalid username or token_id"})
			else:
				if abs(time.time() - int(timestamp)) > settings.TOKEN_TIMEOUT:
					response['errors'].append({"auth_failed": "The token is expired!"})
				else:
					pass
				print("\033[41;1m;%s ---client:%s\033[0m" % (time.time(), timestamp), time.time() - int(timestamp))
		except ObjectDoesNotExist as e:
			response['errors'].append({"auth_failed": "Invalid username or token_id"})
		
		if response['errors']:
			return HttpResponse(json.dumps(response), content_type="application/json")
		else:
			return func(*args, **kwargs)

	return wrapper