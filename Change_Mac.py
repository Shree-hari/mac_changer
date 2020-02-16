#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Enter the kind of interface you will like to have.")
    parser.add_option("-m", "--mac", dest="new_mac", help="New Mac Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Please enter an interface . Press --help for seeking help")
    elif not options.new_mac:
        parser.error("Please enter a new mac address. Press --help for more info")
    return options

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)   # Error is in this line # TypeError: cannot use a string pattern on a bytes-like object

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not find the Mac address")

def change_mac(interface, new_mac):
    print("[+] Changing Mac address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC = " + current_mac)

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] Your Mac Address has successfully changed to " + current_mac)
else:
    print("Your Mac address has failed to change")

