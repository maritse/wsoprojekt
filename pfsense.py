import json
import os
import subprocess

from config import PFSENSE_ADDRESS

def add_new_rule(source, port, action="block", interface="wan", protocol="tcp", destination="NET:lan"):
    command_string = 'ansible-playbook {} -i ./playbook/services.yaml --extra-vars "action_pfsense={} interface_pfsense={} protocol_pfsense={} source_pfsense={} dest_ansible={} port_pfsense={}"'.format(PFSENSE_ADDRESS, action, interface, protocol, source, destination, port)
    command_list = command_string.split()
    result_command = subprocess.run(command_list, stdout=subprocess.PIPE).stdout.decode('utf-8')
    if "SUCCESS" not in str(result_command):
        print("Nie udało się nadać nowej reguły na firewall")
        return None
    result_command = result_command[result_command.index("{"):]
    result_command_json = json.loads(result_command)
    return result_command_json
