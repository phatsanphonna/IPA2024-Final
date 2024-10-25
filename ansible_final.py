import subprocess

def showrun():
    # read https://www.datacamp.com/tutorial/python-subprocess to learn more about subprocess
    command = ['ansible-playbook get-router-config.yaml -i inventory']

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    print(result.stderr)

    if 'ok=2' in result.stdout:
        return 'ok'
    else:
        return 'Error: Ansible'

if __name__ == '__main__':
    showrun()
