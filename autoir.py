import json

from actions import *
from errbot import BotPlugin, botcmd

def parse_alert(alert):
	'''Parses a json string describing an alert.

	Args:
		config (str): the json string for alerts. 

	Returns:
		dict: the parsed alert, or None on error
	'''

	try:
		parsed_alert = json.loads(alert)
	except ValueError:
		return None

	return parsed_alert

def execute_flow(alert, flow):
	'''
	'''

	for action in flow['actions']:
		mod = locals().get(action.get('name'))
		if mod == None:
			yield "Action %s cannot be found" % (action.get('name'))
			continue
		yield mod.action(action.get('field'), action.get('kwargs'))
		yield "performing action %s for alert %s" % (action, alert)

class AutoIR(BotPlugin):
	'''Plugin utilized to automate Incident Response tasks'''

	def get_configuration_template(self):
		'''Define the configuration template for the plugin.
		'''
		return {
			'alerts' : [
				{
				'alert':'foo',
				'actions' : [
					{
					'name':'hello',
					'field':'bar',
					'kwargs': 'json string describing the kwargs'
					}]
				}]
		}

	@botcmd(admin_only=False)
	def alert(self, msg, args):
		'''Add the alert command to errbot. This command is used to automate
		the response to alerts.
		'''	

		alert = parse_alert(args)
		# Do some sanity checking
		if alert is None or alert.get('alert') is None:
			yield "That alert doesn't parse properly. Giving up. %s" % alert
			raise StopIteration

		for flow in self.config['alerts']:
			if flow['alert'] == alert.get('alert'):
				for task in execute_flow(alert, flow):
					yield task

		# This is unnecessary, but it helps me sleep at night
		raise StopIteration