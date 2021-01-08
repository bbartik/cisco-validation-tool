from napalm import get_network_driver
from getpass import getpass
import pdb

username = input("Enter username: ")
password = getpass("Enter password: ")

with open("devices.txt", "r") as f:
    hosts = f.read().splitlines()

for h in hosts:
    driver = get_network_driver('ios')
    device = driver(h, username, password)
    device.open()
    config = device.get_config()
    with open(f"configs/{h}.conf", "w") as f:
        f.write(config["running"])
