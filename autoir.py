import json

from importlib import import_module
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

class AutoIR(BotPlugin):
	'''Plugin utilized to automate Incident Response tasks'''

	def __init__(self, bot):
		super().__init__(bot)

		# Where possible actions are dynamically loaded
		self.actions = {}

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
				for task in self.execute_flow(alert, flow):
					yield task
					#self.send(msg.to, task)

		# This is unnecessary, but it helps me sleep at night
		raise StopIteration

	def execute_flow(self, alert, flow):
		'''
		'''
		for action in flow['actions']:
			action_name = action.get('name')
			mod = self.actions.get(action_name)
			if mod == None:
				try:
					self.actions[action_name] = import_module('actions.%s' % action_name)
					mod = self.actions.get(action_name)
				except ImportError:
					yield "Unable to find action %s, skipping task." % (action_name)
					continue
			#yield "performing action %s for alert %s" % (action_name, alert)
			try:
				yield mod.action(alert, action.get('field'), action.get('kwargs'))
			except AttributeError:
				yield "Action %s has no action function, so I'm not sure what to do here." % (action_name)