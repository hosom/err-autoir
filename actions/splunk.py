import json
import sys

from subprocess import Popen, PIPE

_ENCODING = sys.getdefaultencoding()

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

	proc = Popen(cmd, stdout=PIPE, stderr=PIPE)

	output = [line.decode(_ENCODING) for line in proc.stdout]
	output = ''.join(output)

	alert['splunk'] = json.loads(output.strip("b'").strip())

	records = '\n'.join([record['_raw'] for 
		record in alert['splunk']['results']])
	return '''
```
%s
```
''' % (records)