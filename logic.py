from ansible import get_all_host_data
from data import download_api_nist, normalize_data_nist
from utils import PORT_MAPPING
from pfsense import add_new_rule
from config import IP_ADDRESSES, IP_ADDRESSES_MAPPING
ips = IP_ADDRESSES
ips_mapping = IP_ADDRESSES_MAPPING

def run_turn():
    # get information about the host
    hosts_facts, package_facts = get_all_host_data(ips)

    #print(hosts_facts)
    #print(package_facts)
    print(ips)
    status_list = []
    for one in hosts_facts:
        status = {}
        status["ip"] = one["ip_address"]
        status["os"] = one["os"]
        status["version"] = one["os_version"].replace(".", "")
        status['threats'] = []

        # generate request to the NIST API
        if status["os"] == "ubuntu_linux":
            producent = "Canonical"
        elif "windows" == status["os"].lowercase():
            producent = "Microsoft"
        data_nist = download_api_nist(
            producent,
            status["os"],
            status["version"]
        )
        normalized_data_nist = normalize_data_nist(
            data_nist,
            producent,
            status["os"],
            status["version"]
        )
        
        # scale 0 - 4
        # 0 - no risk
        # 1 - medium severity
        # 2 - medium/high severity
        # 3 - high severity
        # 4 - cirtical severity
        for cve in normalized_data_nist:
            if cve["severity"] in ["MEDIUM", "HIGH", "CRITICAL"]:
                if cve["access-vector"] == "NETWORK":
                    if cve["attack-complexity"] in ["LOW", "NONE"]:
                        if cve["authentication"] == "NONE":
                            if float(cve["cvss-score"]) > 7.5:
                                if cve["confidentialityImpact"] == "COMPLETE" or cve["availabilityImpact"] == "COMPLETE":
                                    opinion = 4
                                else:
                                    opinion = 3
                            else:
                                opinion = 3
                        else:
                            opinion = 2
                    else:
                        opinion = 2
                else: 
                    opinion = 1
            else:
                opinion = 1
            if cve["access-vector"] == "NETWORK":
                cve["opinion"] = opinion
                status["threats"].append(cve) # only network vulns

        network_ports = []
        for threat in status["threats"]:
            description = threat["description"].lower()
            for port in PORT_MAPPING.keys():
                if port in description:
                    threat["port-to-block"] = PORT_MAPPING[port] 

        status_list.append(status)
    # blocking procedure
    rules_status = False
    for one in status_list:
        for threat in one["threats"]:
            if threat["port-to-block"]:
                #add_new_rule(one["ip"], threat["port-to-block"])
                #print("Nowa reguła została dodana")
                rules_status = True
    if rules_status:
        print("Rules have been added")
    print(status_list[0]["threats"][0])
    return status_list


run_turn()

