# Lists all the dependencies and their projects for the Snyk group specified in the SNYK_GROUP
# environment variable.
#
# Output will be restricted to those groups accessible by the Snyk API token in the SNYK_TOKEN
# environment variable.
#
# Output is in CSV format, one project occurence per row
#

import snyk
import os

snyktoken = os.environ['SNYK_TOKEN']
snykgroup = os.environ['SNYK_GROUP']

# this sets the session to include retries in case of api timeouts etc
client = snyk.SnykClient(snyktoken, tries=3, delay=1, backoff=1)

# remove the phantom orgs that are really the groups
orgs = [ y for y in client.organizations.all() if hasattr(y.group,'id') ]
# remove orgs that don't match the snykgroup
orgs = [ y for y in orgs if y.group.id == snykgroup ]

deps = []

for org in orgs:
  deps.append(org.dependencies.all())

for orgdeps in deps:
	for dep in orgdeps:
		for project in dep.projects:
			print(dep.name + "," + dep.version + "," + org.url + "/project/" + project.id)
 
