import subprocess
import json
import os
import sys
import paramiko
import time


def get_sensors(target):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    sock = paramiko.ProxyCommand(
        "ssh -p 8022 -W " + target["host"] + ":22 -q cloud@se-flem-001.kthcloud.com")

    client.connect(
        target["host"], username=target["user"], sock=sock
    )
    stdin, stdout, stderr = client.exec_command('sensors -j')
    stdin.close()

    temps = stdout.read().decode("utf-8")

    return json.loads(temps)


def update_all_hosts(inventory):
    # Get sensor values
    for target in inventory:

        target["last-update"] = time.time()
        target["active"] = True
        dump(inventory)
        target["sensors"] = get_sensors(target)
        dump(inventory)
        target["active"] = False
        dump(inventory)

    return inventory


def dump(targets):
    f = open('data.json', 'a', encoding='utf-8')
    f.seek(0)  # sets  point at the beginning of the file
    f.truncate()  # Clear previous content
    f.write(json.dumps(targets, ensure_ascii=False, indent=4))
    f.close()  # Close file


def main():
    # Get config
    config = open("config.json")
    config = json.load(config)
    inventory = config["inventory"]

    while True:
        inventory = update_all_hosts(inventory)


if __name__ == "__main__":
    main()
