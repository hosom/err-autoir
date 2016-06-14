import requests

from configparser import ConfigParser

_VTAPI = 'https://www.virustotal.com/vtapi/v2/'

def action(alert, field, kwargs):
	'''Perform a virus total lookup of a hash.
	'''

	config = ConfigParser()
	config.read('/etc/err/virustotal.conf')

	_VT_APIKEY = config.get('VirusTotal', 'apikey')

	if _VT_APIKEY is None:
		return 'Your VirusTotal API key has not been configured. Skipping VirusTotal action'

	return alert.get(field)

	parameters = {
		'resource' : alert.get(field),
		'apikey' : _VT_APIKEY
	}

	r = requests.post('%sfile/report' % (_VTAPI),
						data=parameters)
	report = r.json()
	if report.get('response_code') == 1:
		return '''
```
VirusTotal
%s
%s/%s
```
For more information see: %s
''' % (report['scan_date'], 
		report['positives'], 
		report['total'],
		report['permalink'])
	else:
		return '''
```
VirusTotal
File not found.
```
'''