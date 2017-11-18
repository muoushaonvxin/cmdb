# -*- encoding: utf-8 -*-
import pickle, time

from TimeSpace.ServerHandler import Redis_conn

class TriggerHandler(object):

	def __init__(self, django_settings):
		self.django_settings = django_settings
		self.redis = Redis_conn.redis_conn(self.django_settings)
		self.alert_counters = {}
		alert_counters = {
			1: {2:{'counter':0, 'last_alert': None},
				4:{'counter':1, 'last_alert': None}},
		}


	def start_watching(self):
		radio = self.redis.pubsub()
		radio.subscribe(self.django_settings.TRIGGER_CHAN)
		radio.parse_response()
		print("\033[43;1m************** start listening new triggers ***************\033[0m")
		self.trigger_count = 0
		while True:
			msg = radio.parse_response()
			self.trigger_consume(msg)


	def trigger_consume(self, msg):
		self.trigger_count += 1
		print("\033[41;1m********** Got a trigger msg [%s] ***********\033[0m" % self.)
		trigger_msg = pickle.loads(msg[2])
		action = ActionHandler(trigger_msg, self.alert_counters)
		action.trigger_process()



class ActionHandler(object):

	def __init__(self, trigger_data, alert_counter_dic):
		self.trigger_data = trigger_data

	def trigger_process(self):
		print("Action Processing".center(50, '-'))
		print(self.trigger_data)
		if self.trigger_data.get('trigger_id') == None:
			if self.trigger_data.get('msg'):
				print(self.trigger_data.get('msg'))
			else:
				print("\033[41;1mInvalid trigger data %s\033[0m" % self.trigger_data)
		else:
			trigger_id = self.trigger_data.get('trigger_id')
			host_id = self.trigger_data.get('host_id')
			trigger_obj = models.Trigger.objects.get(id=trigger_id)
			actions_set = trigger_obj.action_set.select_related()
			matched_action_list = ()
			for action in actions_set:
				for hg in action_host_groups.select_related():
					for h in hg.host_set.select_related():
						if h.id == host_id:
							matched_action_list.add(action)
							if action.id not in self.alert_counter_dic:
								self.alert_counter_dic[action] = {h.id:{'counter': 0, 'last_alert': time.time()}}

				for host in action.hosts.select_related():
					if host.id == host_id:
						matched_action_list.add(action)
						self.alert_counter_dic.setdefault(action, {host.id:{'counter': 0, 'last_alert': time.time()}})


			for action_obj in matched_action_list:
				if time.time() - self.alert_counter_dic[action_obj][host_id]['last_alert'] >= action_obj.interval:
					for action_operation in action_obj.operations.select_related().order('-step'):
						if action_operation.setp > self.alert_counter_dic[action_obj][host_id]['counter']:
							print("alert action: %s" % action.action_type, action.notifiers)






























