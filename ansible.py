import json
import os
import subprocess

from config import ANSIBLE_PLAYBOOK_PATH


# https://www.linuxtopic.com/2019/02/ansible-playbook-get-hosts-information.html
# ansible facts

def check_ansible_installed():
	result = os.system("which ansible")
	if result != 0:
		print("Ansible is not installed")
		return None
	return True

def check_playbook_exist(path):
	if not check_ansible_installed():
		print("Ansible does not exists")
		return
	if not os.path.isfile(ANSIBLE_PLAYBOOK_PATH):
		print("Playbook does not exists")
		return

def check_host_are_up():
	result = os.system("ansible all -m ping")
	if result != 0:
		print("Not all hosts are up")
		return

def get_host_facts_ansible(host_ips):
	#if not check_playbook_exist(playbook_path):
	#	print("Cannot load the playbook file")
	#	return
	if not check_ansible_installed():
		print("Not found - ansible binary")
		return
	results = []
	for one in host_ips:
		result_command = subprocess.run("ansible {} -m ansible.builtin.setup".format(one).split(), stdout=subprocess.PIPE).stdout.decode('utf-8')
		result_command = result_command[result_command.index("{"):]
		result_command_json = json.loads(result_command)
		results.append(result_command_json)
	
	# Add support for multiple IP addresses
	# result_command_json["ansible_facts"], host_ip
	return results


def normalize_facts(data, host_ips):
	# https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_vars_facts.html
	hosts_info = []
	for one in data:
		one = one["ansible_facts"]
		#print(one["ansible_distribution"])
		info_host = {
			"os": one["ansible_distribution"],
			"os_version": one["ansible_distribution_version"],
			"kernel_version": one["ansible_kernel"],
			"product_name": one["ansible_product_name"],
			"product_version": one["ansible_product_version"]
		}
		if one["ansible_distribution"] == "Ubuntu":
			info_host["os"] = "ubuntu_linux"
		hosts_info.append(info_host)

	for i in range(len(hosts_info)):
		hosts_info[i]["ip_address"] = host_ips[i]

	return hosts_info

def get_services_ansible(host_ips):
	if not check_ansible_installed():
		print("Not found - ansible binary")
		return
	results = []
	for one in host_ips:
		result_command = subprocess.run("ansible {} -m ansible.builtin.service".format(one).split(), stdout=subprocess.PIPE).stdout.decode('utf-8')
		result_command = result_command[result_command.index("=>"):]
		result_command_json = json.loads(result_command)
		results.append(result_command_json)
	return results
# TODO func normalize_services

def get_package_facts_ansible(host_ips):
	'''
	The function only returns the data related to the `net` category.
	'''
	if not check_ansible_installed():
		print("Not found - ansible binary")
		return
	
	results = []
	for one in host_ips:
		result_command = subprocess.run("ansible {} -m ansible.builtin.package_facts".format(one).split(), stdout=subprocess.PIPE).stdout.decode('utf-8')
		result_command = result_command[result_command.index("{"):]
		result_command_json = json.loads(result_command)
		results.append(result_command_json)
	return results

def normalize_package_facts(data, host_ips):
	results = []
	for i in range(len(data)):
		data_filtered = {}
		data_packages = data[i]["ansible_facts"]["packages"]
		for one in data_packages:
			if data_packages[one][0]["category"] == "net":
				data_filtered[one] = {
					"product_name": data_packages[one][0]["name"],
					"version": data_packages[one][0]["version"],
					"ip_address": host_ips[i]
				}
				if data_packages[one][0]["origin"] == "Ubuntu":
					data_filtered[one]["vendor"] = "ubuntu_linux"
		results.append(data_filtered)
	return results


def get_all_host_data(hosts_ip):
	#services = get_services_ansible()
	package_facts = get_package_facts_ansible(hosts_ip)
	host_facts = get_host_facts_ansible(hosts_ip)

	#services_normalized = normalize_facts(services)
	package_facts_normalized = normalize_package_facts(package_facts, hosts_ip)
	host_facts_normalized = normalize_facts(host_facts, hosts_ip)

	return host_facts_normalized, package_facts_normalized
