from cbapi.response import CbEnterpriseResponseAPI, Process, Binary, Sensor
import json



def action(alert, fields, kwargs):
	'''Perform a Carbon Black lookup.

	This depends on a configuration file that will be stored at 
	/etc/carbonblack/credentials.response

	[default]
	url=https://cb.battelle.org/
	token=<APIKEY>
	ssl_verify=False

	Args:
		alert (dict): The alert that is being automated.
		fields (list): A list of fields in the alert dict to perform the
		query with.
		kwargs (str): Normally kwargs would be a dict, however, due to 
		complications in errbot, in this case it is a string that parses
		with python's json parser.

	Returns:
		str: the query response from carbon black.
	'''

	cb = CbEnterpriseResponseAPI(profile="default") 
	procs = list()
	kwargs = json.loads(kwargs)


	if cb is None:
		return 'Could not create CarbonBlack connection. API key may have not been configured for cbapi. Skipping CB action.'

	parameters = [alert.get(field) for field in fields]

	query = cb.select(Process)
	search = kwargs['query'] % tuple(parameters)   
	try:
		results = query.where(search)
		total = len(results)
		for proc in results[:5]:
			procs.append(proc)
	except:
		return "Failed to search with query: %s" % (search)


	if len(procs) > 0:
		report = ''
		for proc in procs:
			report += '''
\`\`\`

HostName: %s\n
UserName: %s\n
Cmdline: %s\n
Process Analysis Link: %s\n

\`\`\`
'''  % (proc.hostname,proc.username,proc.cmdline,proc.webui_link)

	else:
		report= '''
```
CarbonBlack
No results returned.
```
'''
	alert['cb'] = report
	return report
