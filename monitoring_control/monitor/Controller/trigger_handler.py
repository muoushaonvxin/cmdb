# -*- encoding: utf-8 -*-
import pickle, time
from .redis_conn import redis_conn
from monitoring_control import settings
from monitor.models import EventLog, Trigger
from django.core.mail import send_mail


class TriggerHandler(object):

	def __init__(self):
		self.django_settings = settings
		self.redis = redis_conn()
		self.alert_counters = {}
		self.trigger_count = 0

		'''
		alert_counters = {
			1: {2:{'counter':0, 'last_alert': None},
				4:{'counter':1, 'last_alert': None}},
		}
		'''


	def start_watching(self):
		radio = self.redis.pubsub()
		radio.subscribe(self.django_settings.TRIGGER_CHAN)
		radio.parse_response()
		print("\033[43;1m************** start listening new triggers ***************\033[0m")
		while True:
			msg = radio.parse_response()
			self.trigger_consume(msg)


	def trigger_consume(self, msg):
		self.trigger_count += 1
		print("\033[41;1m********** Got a trigger msg [%s] ***********\033[0m" % self.trigger_count)
		trigger_msg = pickle.loads(msg[2])
		action = ActionHandler(trigger_msg, self.alert_counters)
		action.trigger_process()


class ActionHandler(object):


	def __init__(self, trigger_data, alert_counter_dic):
		self.trigger_data = trigger_data
		self.alert_counter_dic = alert_counter_dic


	def record_log(self, action_obj, action_operation, host_id, trigger_data):
		EventLog.objects.create(
			event_type = 0,
			host_id = host_id,
			trigger_id = trigger_data.get('trigger_id'),
			log = trigger_data
		)


	def action_email(self, action_obj, action_operation_obj, host_id, trigger_data):
		print("要发报警的数据:", self.alert_counter_dic[action_obj.id][host_id])
		print("action email:", action_operation_obj.action_type, action_operation_obj.notifiers, trigger_data)
		notifier_mail_list = [obj.email for obj in action_operation_obj.notifiers.all()]
		subject = '级别:%s -- 主机:%s' % (trigger_data.get('trigger_id'), trigger_data.get('host_id'), trigger_data.get('service_item'))

		send_mail(
			subject,
			action_operation_obj.msg_format,
			settings.DEFAULT_FROM_EMAIL,
			notifier_mail_list,
		)


	def trigger_process(self):
		print("Action Processing".center(50, '-'))
		print(self.trigger_data)

		if self.trigger_data.get('trigger_id') == None:
			if self.trigger_data.get('msg'):
				print(self.trigger_data.get('msg'))
			else:
				print("\033[41;1mInvalid trigger data %s\033[0m" % self.trigger_data)
		else:
			print("\033[33;1m%s\033[0m" % self.trigger_data)
			trigger_id = self.trigger_data.get('trigger_id')
			host_id = self.trigger_data.get('host_id')
			trigger_obj = Trigger.objects.get(id=trigger_id)
			actions_set = trigger_obj.action_set.select_related()
			print("actions_set:", actions_set)
			matched_action_list = set()
			for action in actions_set:
				for hg in action.host_groups.select_related():
					for h in hg.host_set.select_related():
						if h.id == host_id:
							matched_action_list.add(action)
							if action.id not in self.alert_counter_dic:
								self.alert_counter_dic[action.id] = {}
							print("action, ", id(action))
							if h.id not in self.alert_counter_dic[action.id]:
								self.alert_counter_dic[action.id][h.id] = {'counter': 0, 'last_alert': time.time()}
							else:
								if time.time() - self.alert_counter_dic[action.id][h.id]['last_alert'] >= action.interval:
									self.alert_counter_dic[action.id][h.id]['counter'] += 1
								else:
									print("没达到alert interval时间，不报警", action.interval, time.time() - self.alert_counter_dic[action.id][h.id]['last_alert'])


				for host in action.hosts.select_related():
					if host.id == host_id:
						matched_action_list.add(action)
						if action.id not in self.alert_counter_dic:
							self.alert_counter_dic[action.id] = {}
						if h.id not in self.alert_counter_dic[action.id]:
							self.alert_counter_dic[action.id][h.id] = {'counter': 0, 'last_alert': time.time()}
						else:
							if time.time() - self.alert_counter_dic[action.id][h.id]['last_alert'] >= action.interval:
								self.alert_counter_dic[action.id][h.id]['counter'] += 1
							else:
								print("没达到alert interval 时间，不报警", action.interval, time.time() - self.alert_counter_dic[action.id][h.id]['last_alert'])

			print("alert_counter_dic:", self.alert_counter_dic)
			print("matched_action_list:", matched_action_list)
			for action_obj in matched_action_list:
				if time.time() - self.alert_counter_dic[action_obj][host_id]['last_alert'] >= action_obj.interval:
					print("改报警了......", time.time() - self.alert_counter_dic[action_obj.id][host_id]['last_alert'], action_obj.interval)
					for action_operation in action_obj.operations.select_related().order('-step'):
						if action_operation.setp > self.alert_counter_dic[action_obj][host_id]['counter']:
							print("alert action: %s" % action.action_type, action.notifiers)
							action_func = getattr(self, 'action_%s' % action_operation.action_type)
							action_func(action_obj, action_operation, host_id, self.trigger_data)

							# 报警完成之后更新报警时间, 这样又重新计算 alert interval 了
							self.alert_counter_dic[action_obj.id][host_id]['last_alert'] = time.time()
							self.record_log(action_obj, action_operation, host_id, self.trigger_data)



