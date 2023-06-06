from ansible import get_package_facts_ansible, normalize_package_facts

ip = ["192.168.100.77", "192.168.100.80"]
data = get_package_facts_ansible(ip)
print(normalize_package_facts(data, ip))