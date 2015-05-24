#!/usr/bin/env python

# May 10, 2011
# new_sys_setup.py
# Jose Juarez - 120photo@gmail.com
# The following script does the following:
# -set a new hostname for the new server
# -set a new static IP address
# -remove ssh_host keys and regenerate new keys
# -upgrade the system

import subprocess

def checkSetup():
    """
    Setup a function to check for a hidden file that tells the user
    if this setup script has alredy run. If the script has not run
    it will procede otherwise it will promto to exit or continue.
    """

def setIP():
    '''
    This function will collect network setting for this server from
    the admin and write to the /etc/networking/interfaces file.
    '''
    IP = raw_input(str("What is the IP address of this system?\n"))
    Subnet = raw_input("What is the Subnet for this system?\n")
    Gateway = raw_input("What is the Gateway for this system?\n")
    config_file = open("/home/anfadmin/Desktop/test/001", 'w')
    IP_config = """
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto eth0
iface eth0 inet static
    address %s
    netmask %s
    gateway %s
    """ % (IP, Subnet, Gateway)
    config_file.write(IP_config)
    config_file.close()

def setHost():
    """
    This function sets a new hostname for the system. Two files are modified
    first '/etc/hostname', simply the host name and not the FQDN is needed. The
    second file modified here is '/etc/hosts'. This file is a bit more comples
    and string modifiers are used to set the host name inside the config file.
    """
    new_hostname = raw_input(str("What is the DNS name of this new host?:\n"))
    host_file1 = open('/home/anfadmin/Desktop/test/002', 'w')
    host_file1.write(new_hostname)
    host_file1.close()
    host_file2 = open('/home/anfadmin/Desktop/test/003', 'w')
    host_file2_config = """
127.0.0.1	localhost
127.0.1.1	%s.annenbergfoundation.org	%s

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters 
    """ % (new_hostname, new_hostname)
    host_file2.write(host_file2_config)
    host_file2.close()
    subprocess.call('/etc/init.d/networking restart', shell=True)

def ssh_keys():
    """
    This function simply removes the ssh_host* keys from the template
    server and regenerates new keys. This is important to make sure no
    two servers have the same private keys (security people!).
    """
    print "removing old ssh keys and generating new keys"
    #command to remove old keys in /etc/ssh/ssh_host*
    subprocess.call('rm /etc/ssh/ssh_host*', shell=True)
    #command to generate new keys dpkg-reconfigure openssh-server
    subprocess.call('dpkg-reconfigure openssh-server')
    print "ok, done"

def system_upgrade():
    subprocess.call('apt-get update', shell=True)
    subprocess.call('apt-get dist-upgrade -y', shell=True)
    print """
#########
#########
Please restart your system with "sudo shutdown -r now"
#########
#########
    """

def run_functions():
    new_hostname()
    setIP()
    ssh_keys()
    system_upgrade()


run_functions()