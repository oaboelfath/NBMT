from napalm import get_network_driver
import time
import os

cisco_ios = get_network_driver('ios')
cisco_iosxr = get_network_driver('iosxr')
juniper = get_network_driver('junos')


username = 'nbmt'
password = 'nbmt123'

vios = cisco_ios('192.168.6.101', username, password)
xrv = cisco_iosxr('192.168.6.102', username, password)
vsrx = juniper('192.168.6.103', username, password)

devices = [vios, xrv, vsrx]

if not os.path.exists('running-config'):
    print('Creating "running-config" Directory')
    os.makedirs('running-config')

for device in devices:
    device.open()
    facts = device.get_facts()
    hostname = facts["hostname"]
    print("Fetching running-config for Device %s") %hostname
    config = device.get_config()
    running_config = config["running"]
    if not os.path.exists('running-config/'+hostname):
        print("Creating Directory for %s") % hostname
        os.makedirs('running-config/'+hostname)
    with open('running-config/'+hostname+'/'+hostname+'-'+time.strftime("%Y-%m-%d--%H-%M")+'.log', 'w') as file:
        print("Writing to file %s") %file.name
        file.write('\n')
        run_conf = running_config.split('\n')
        for each_line in run_conf:
            file.write(each_line+'\n')
    device.close()


