
from cbapi.response import CbEnterpriseResponseAPI, Process, Binary, Sensor
import json



def action(alert, field, kwargs):
	'''
	Perform a Carbon Black lookup.
	'''

	cb = CbEnterpriseResponseAPI(profile="default") 
	procs = list()
	kwargs = json.loads(kwargs)


	if cb is None:
		return 'Could not create CarbonBlack connection. API key may have not been configured for cbapi. Skipping CB action.'

	if field == 'process_name':
		query = cb.select(Process)
	elif field == 'binary_name':
		query = cb.select(Binary)
	else:
		return "%s is not a supported search type" % (field)
                                
	try:
		search = kwargs['query'] % (alert.get(field))
		print(search)
		results = query.where(search)
		for proc in results[:5]:
			procs.append(proc)
	except:
		return "Failed to search with query: %s" % (search)



	if len(procs) > 0:
		url = "https://cb.battelle.org/#search/cb.urlver=1&q=process_name%3A" + alert.get(field) + "&sort=&rows=10&start=0"
		report = "CarbonBlack\nWeb UI Query Link: %s" % (url)
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
	print(report)
	return report
