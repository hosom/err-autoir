from cbapi.response import CbEnterpriseResponseAPI, Process, Binary, Sensor
import json



def action(alert, fields, kwargs):
	'''
	Perform a Carbon Black lookup.
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
		url = "https://cb.battelle.org/#search/cb.urlver=1&q=" + search + "&sort=&rows=10&start=0"
		report = "CarbonBlack\nWeb UI Query Link: %s\nTotal Number of Processes: %s" % (url,total)
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
