import json
import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.181-184
api_url = "https://10.0.15.183/restconf/data/ietf-interfaces:interfaces"

loopback_name = 'Loopback65070171'
student_id = '65070171'

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = {'Accept': 'application/yang-data+json', 'Content-Type': 'application/yang-data+json'}
basicauth = HTTPBasicAuth("admin", "cisco")


def loopback_exists():
    resp = requests.get(
        f'{api_url}/interface={loopback_name}', 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if resp.status_code >= 200 and resp.status_code <= 299:
        print("STATUS OK: {}".format(resp.status_code))
        return True
    elif resp.status_code == 404:
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return False
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def create():
    if loopback_exists():
        return f"Cannot create: Interface loopback {student_id}"

    yangConfig = {
        "ietf-interfaces:interface": {
            "name": loopback_name,
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "172.30.171.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    resp = requests.put(
        f'{api_url}/interface={loopback_name}',
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {student_id} is created successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def delete():
    if not loopback_exists():
        return f"Cannot delete: Interface loopback {student_id}"

    resp = requests.delete(
        f'{api_url}/interface={loopback_name}', 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if resp.status_code >= 200 and resp.status_code <= 299:
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {student_id} is deleted successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def enable():
    if not loopback_exists():
        return f"Cannot enable: Interface loopback {student_id}"

    yangConfig = {
        "ietf-interfaces:interface": {
            "name": loopback_name,
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "172.30.171.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    resp = requests.put(
        f'{api_url}/interface={loopback_name}', 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {student_id} is enabled successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def disable():
    if not loopback_exists():
        return f"Cannot shutdown: Interface loopback {student_id}"

    yangConfig = {
        "ietf-interfaces:interface": {
            "name": loopback_name,
            "type": "iana-if-type:softwareLoopback",
            "enabled": False,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "172.30.171.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    resp = requests.put(
        f'{api_url}/interface={loopback_name}', 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {student_id} is shutdowned successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def status():
    if not loopback_exists():
        return f"No Interface loopback {student_id}"

    api_url_status = f'{api_url}-state'

    resp = requests.get(
        api_url_status, 
        auth=basicauth, 
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()

        admin_status = ''
        oper_status = ''

        for intf in response_json['ietf-interfaces:interfaces-state']['interface']:
            if intf['name'] == loopback_name:
                admin_status = intf['admin-status']
                oper_status = intf['oper-status']
                break

        if admin_status == 'up' and oper_status == 'up':
            return f'Interface loopback {student_id} is enabled'
        elif admin_status == 'down' and oper_status == 'down':
            return f"Interface loopback {student_id} is disabled"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
