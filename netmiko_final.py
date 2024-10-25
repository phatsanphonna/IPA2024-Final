from netmiko import ConnectHandler
from pprint import pprint

device_ip = "10.0.15.183"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
}


def gigabit_status():
    ans = ""
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        ans = ''
        result = ssh.send_command("sh ip int br", use_textfsm=True)
        
        pprint(result)

        result = filter(lambda x: x['interface'].startswith('GigabitEthernet'), result)

        for status in result:
            if status["interface"].startswith('GigabitEthernet'):
                ans += f"{status['interface']} {status['status']}, "
        
                if status['status'] == "up":
                    up += 1
                elif status['status'] == "down":
                    down += 1
                elif status['status'] == "administratively down":
                    admin_down += 1
        
        ans = ans[:-2]
        
        ans += f" -> {up} up, {down} down, {admin_down} administratively down"

        print(ans)
        return ans

if __name__ == '__main__':
    gigabit_status()
