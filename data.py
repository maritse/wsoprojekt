import json
import requests
from config import OSV_API_URL, NIST_API_URL, API_CVE_SEARCH_URL
from utils import create_cpe

######################################################################

# OSV API

######################################################################
def download_api(package, vendor, version=None):
	version = version if version else None
	# OSV
	data_osv = download_api_osv(package, version)

	#cve-search --> outdated
	#data_cve_search = download_api_cve_search(package_name, vendor)

	#cve-search last 30
	data_last_cve_search = download_last_api_cve_search()

def download_api_osv(package_name, version=None):
	if version:
		response = requests.post(OSV_API_QUERY_URL,data={"package": {"name": package_name, "version": version}})
	else:
 		response = requests.post(OSV_API_QUERY_URL,data={"package": {"name": package_name}})

	if data.status_code != 200:
		return None

	data = response.json()
	print(data)
	return data
'''
def download_api_cve_search(package_name, vendor):
	url_with_params = CVE_SEARCH_URL + "/" + vendor + "/" + package_name
	response = requests.get(url_with_params)
	if reponse.status_code != 200:
		return None
	data = response.json()
	print(data)
	return data

def download_last_api_cve_search():
	response = requests.get(CVE_SEARCH_URL + "last")
	if response.status_code != 200:
		return None
	data = response.json()
	print(data)
	return data
'''
######################################################################

# api.cvesearch.com 

######################################################################
def download_api_cvesearch(keyword):
	response = requests.get(API_CVE_SEARCH_URL + "?prisma=" + keyword)
	if response.status_code != 200:
		return None
	data = response.json()
	return data

def normalize_api_cvesearchdata(data, keyword):
	pass


######################################################################3

# 	NIST API

#######################################################################
def download_api_nist(vendor, product, version, part=None):
	cpe = create_cpe(vendor, product, version, part) # TODO
	#print(cpe)
	response = requests.get(NIST_API_URL + "?cpename=" + cpe)
	if response.status_code != 200:
		return None
	data = response.json()
	return data

def normalize_data_nist(data, vendor, product, version):
	vulnerabilities = data["vulnerabilities"]
	data = []
	for row in vulnerabilities:
		row = row["cve"]
		one = {
			"vendor": vendor,
			"product": product,
			"version": version,
			"cve-id": row["id"],
			"description": row["descriptions"][0]["value"],
			"access-vector": row["metrics"]["cvssMetricV2"][0]["cvssData"]["accessVector"],
			"attack-complexity": row["metrics"]["cvssMetricV2"][0]["cvssData"]["accessComplexity"],
			"authentication": row["metrics"]["cvssMetricV2"][0]["cvssData"]["authentication"],
			"cvss-score": row["metrics"]["cvssMetricV2"][0]["cvssData"]["baseScore"],
			"confidentialityImpact": row["metrics"]["cvssMetricV2"][0]["cvssData"]["confidentialityImpact"],
			"availabilityImpact": row["metrics"]["cvssMetricV2"][0]["cvssData"]["availabilityImpact"],
			"severity": row["metrics"]["cvssMetricV2"][0]["baseSeverity"]
		}
		data.append(one)
	return data

def get_all_cve_data():
	pass


