import json

from io import StringIO
from subprocess import Popen, PIPE

def action(alert, field, kwargs):
	'''
	'''
	try:
		kwargs = json.loads(kwargs)
	except ValueError:
		return "Received invalid kwargs in configuration."

	search = kwargs.get('query')

	try:
		search = search % (alert.get(field))
	except TypeError:
		return "Unable to compile query string."

	cmd = ["/usr/bin/python2", 
		"/usr/local/bin/splunk/search.py",
		search,
		"--config=/etc/err/splunk.conf",
		"--output_mode=json"]

	output = StringIO()
	proc = Popen(cmd, stdout=PIPE, stderr=PIPE)

	for line in proc.stdout:
		output.write(line)

	return output.getvalue()