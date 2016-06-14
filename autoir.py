import json

from errbot import BotPlugin, botcmd

def parse_config(config):
	'''Parses a json string describing automatic actions into a dictionary.

	Args:
		config (str): the json string for alert flows. 

	Returns:
		dict: the parsed configuration, or None on error
	'''

	try:
		parsed_config = json.loads(config)
	except ValueError:
		return None

	return parse_config

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
					'kwargs': {'some_arg':'test'}
					}]
				}]
			]
		}

	@botcmd(admin_only=False)
	def alert(self, msg, args):
		'''Add the alert command to errbot. This command is used to automate
		the response to alerts.
		'''	

		return 'Hello, World!'