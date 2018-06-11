2. COA
----
2.1 The Certified OpenStack Administrator

https://www.openstack.org/coa
	- 6 months of experiance
	- Skills needed to provide every day support and management of the openstack cloud
	- Practical exam based on Newton release
	- 2.5 hours and 76% Passing Score
	
Exam Requirements:
	- Getting to know openstack
	- Identity Management
	- Dashboard
	- Compute
	- Object storage
	- Block Storage
	- networking
	- Heat
	- Troubleshooting
	- Image Management

In this course will discuss below:
	- Getting to know OpenStack (3 % )
		- Understand the components that make up the cloud
		- Use the OpenStack API/CLI
	- Dashboard(3%)
		- Verify operation of the Dashboard
		
Lab Environment (Single Node)

2.2 OpenStack backend Services:
--

grep CONFIG_MARIADB_PW /root/answers.txt
mysql -u root -p$(grep MARIADB_PW answers.txt | cut -f2 -d=)

show databases;

# rabbitmqctl list_users
	guest [administrator]
# grep '^rabbit_password' /etc/nova/nova.conf

# Create Python Script to Test Rabbit Credentials

2.3 Verify Back-end Services
----

# Check the MariaDB password
cat answers.txt

# grep CONFIG_MARIADB_PW andwers.txt

# mysql -u root -p$(grep CONFIG_MARIADB_PW answers.txt | cut -f2 -d=)
# show databases;

# use cinder;
# show databases;

ctrl+l to come back to the screen

## rabbitmqctl list_users
# grep rabbit_password /etc/nova/nova.conf

# cat test_rabbit.py

# ./test_rabbit.py

2.4 OpenStack Services
-----------

# OpenStack-Status
# source keystonerc_admin && openstack-status

# reboot

# openstack-status

## restarting keystone services
# systemctl restart httpd.service
# systemctl status httpd.service 

# openstack-status

# systemctl restart neutron-server.service

# openstack-status

# source keystone_admin
# openstack-status

# openstack u 

## tab completion

# openstack complete 
# openstack complete >> keystonerc_admin

3.1PackStackInstallOfOpenStack
----
# OpenStack CLI Authentication
# Creating a Virtual Machine from CLI
# Creating a Virtual Machine from the Dashboard
# OpenStack Logs

## Understand OpenStack Credentials Files

## CLI Authentication
# openstack --os-username demo --os-tenant-name demo --os-password Password1 --os-auth-url http://192.168.56.5:5000/v2.0 token issue

3.2  Authentication from the CLI
--------

# openstack token issue

# openstack --os-username demo --os-password Password1 --os-tenant-name demo --os-auth-url http://192.168.56.5:5000/v2.0 token issue

# vim adminrc

# openstack complete > complete
# cp adminrc demorc

# vim demorc
# source demorc

3.3 Creating Virtual Machines from the CLI
----
# source demorc
# openstack server list
# openstack server delete <server name>
# openstack image list
# openstack network list
# openstack flavor list

## Creaate instance
# openstack help create server
# openstack create server --image cirros --flavor m1.tiny --nic net-id=private myvm

# openstack server list
# ip netns
<<copy qrouter>>
# ip netns exec <<copied qrouter>> ping 10.0.0.6

# openstack server delete myvm

3.5 Working with Logs
----------
- Log Files

tail -fn0 /var/log/nova/nova-compute.log/nova/nova-compute.log

#  tail -f /var/log/nova/nova-compute.log/nova/nova-compute.log

tail -fn0 /var/log/nova/nova-compute.log/nova/nova-compute.log

## Change the log level to capture only warnings and errors

# vi /etc/nova/nova.conf

	/verbos
	verbose=True
	
	# change the value from True to False
	verbose=False
:wq!

## Restart nova-compute service
# systemctl restart openstack-nova-compute.service

# tail -fn0 /var/log/nova/nova-compute.log

4.1Securing MariaDB and MySQL
----
	- Database Service
	- Securting MariaDB / MySQL
	- Backing Up Databases
	- Message Queue Service
## OpenStack Databases
MariaDB && MySQL

## Secure MySQL /MariaDB

## Login to the mysql
# mysql

## check the present login user
	> SELECT USER();
	
# quit

# grep MARIADB_PW answers.txt

# mysql_secure_installation
	-> Enter the root user login --> Change the password --> remove ananonymas account --> reload previleges
	
# mysql -u root -p

# grep sql_connection /etc/nova/nova.conf

4.2 Backup Your OpenStack Databases
-----

## back-up all the databases
# mysqldump --opt-all-databases -p > /tmp/alldb.sql 

## back-up only neutron database
# mysqldump --opt neutron -p > /tmp/neutrondb.sql

#mysqlshow ## Shortcut to show Databases;

## get all the databases details
# mysqlshow -p

# mysqldump --opt-all-databases -p > /tmp/all.sql 

### Less out the last argument
# less !$

#mysqldump --opt neutron -p > /tmp/net.sql
# less !$

4.3 Monitoring Your RabbitMQ Server
-------
Monitoring Rabbit

# rabbitmq-plugins list
# rabbitmq-plugins enable reabbitmq_management
# systemctl restart rabbitmq-server
# http://192.168.56.5:15672

## rabbitmqctl status
## enable the plug-in to have graphical interface
# rabbitmq-plugins list

# rabbitmq-plugins enable rabbitmq_management

## Restart the service
# systemctl restart rabbitmq-server.service

## Login to GUI
http://192.168.56.5:15672

Username : guest
Password : guest

5.1 OpenStack Versioning
----
	-	Keystone identity service
	-	Versioning in OpenStack
	- 	Apache WSGI Module
	-	Service Endpoints

- Authentication: Credentials
- Authorization: Tokens
- Catalog: Endpoint registry
- Resourcing: Data on projects
- Assignment: Role Assignment
- Policies: Rule based management

-- Openstack Versioning
	-	Prior to the Liberty we used to have version number like : 2015.1
	-	with Liberty release we are getting the version like : 8.0.1
	
## Discover the keystone version
# keystone-manage --version

5.2 Keystone Endpoints
----------
## Apache Module

# systemctl status openstack-keystone

Main configuration file
# head /etc/httpd/conf.d/10-keystone_wsgi_main.conf

# Admin configuration file
# head /etc/httpd/conf.d/10-keystone_wsgi_admin.conf

## Keystone Ports

# Admin port : 35357
# Main Project : 5000

## Discovering Keystone
# source adminrc
# openstack endpoint list
# openstack endpoint show <<keystone id>>

## Keystone Configuration:
# sed -i 's/^verbose\s*True/verbose = False/' /etc/keystone/keystone.conf

# systemctl restart httpd

# grep '^connection' /etc/keystone/keystone.conf

5.3 Keystone Configuration
------
# systemctl status openstack-keystone.service

# Admin configuration
#head /etc/httpd/conf.d/10-keystone_wsgi_admin.conf

# Main configuration
#head /etc/httpd/conf.d/10-keystone_wsgi_main.conf

# ss -ntl

## source adminrc

# openstack endpoint list

# openstack endpoint list <<id of the endpont>>

## get the verbose configuration in keystone configuration file
# grep '^verbose' /etc/keystone/keystone.conf

# sed -i 's/^verbose\s*=\s*True/verbose = False/' !$
==> output : sed -i 's/^verbose\s*=\s*True/verbose = False/' /etc/keystone/keystone.conf

# !g	(or)
# grep '^verbose' /etc/keystone/keystone.conf

# systemctl restart httpd

## check database connection
# grep '^connection' !$	(or)
#grep '^connection' grep '^verbose' /etc/keystone/keystone.conf

--
6.1Understanding Glance in OpenStack
---
	- Glance Imae Service
	- Glance Endpoints
	- Cinder Volume Service
	- Cinder Enndpoints
	- Add a Volume to an instance
	
## The Image Service(glance) enables users to discover, register and retrive virtual machines images. Thease images are used to provision new instances. Images can be stored in the filesystem or an openstack Object Store

## Glance Images
# Openstack server create --image cirros --
# glance-manage --version
# source adminrc
# openstack image list
# openstack endpoint list

6.2 Working with Glance
-----

# glance-manager --version

# soruce adminrc
# openstack image list

# openstack image show cirros
<<Copy the file value>>

# ls -lh /var/lib/glance/images/<<id of the image>>

## openstack endpoint list

# openstack endpont show glance

6.3 Understanding Cinder the Volume Service for OpenStack
---
Cinder Software Defined Storage

# cinder-manage --version
# cinder-manage service list
# openstack endpoint list

# cinder-manage --version
# cinder-manage service list

# opentack endpoint list
# openstack endpoint show <<cinder key>>

6.4 Adding Volumes to a Virtual Machine in OpenStack
--

# launch instance from Dashboard
# Create a volume
# Attach volume to instance in dashboard

# connect to instance
# login to ssh --> lsblk(show partition) --

7.1 Nova Service
	- Nova Compute Service
	- Hypervisors
	- Verify Nova Services
	- Verify Nova Endpoints

# Working with Nova
# nova-manage --version
# source adminrc
# openstack compute service list
# openstack endpoint list

7.2 Verify Nova and KVM Support
---
# cat /proc/cpuinfo

# cat /proc/cpuinfo

# grep -E '(vme|svm)' /proc/cpuinfo

# lsmod | grep kvm

# nova-manage --version

# source adminrc

# openstack compute service list

# openstack endpoint list

# openstack endpoint show compute

7.3 Working with Flavors or Hardware Templates
---
## Instance are servers

# source adminrc
# openstack server list
# openstack server show vm1

## Nova flavors
# source adminrc
# openstack flavor list

## Create own flavor
# openstack flavor create --id auto --ram 512 --disk 10 --vcpus 1 --public small-server

## Create Flavor and Instance
# openstack flavor list

# openstack flavor create --id auto --ram 512 --disk 10 --vcpus 1 --public small-server

## change the credentials
# source demorc

# openstack server list
# openstack server create --flavor small-server --image cirros --nic net-id=private vm1

## view the vm status
# openstack server list

8.1 Identity and Verify Neutron Network Service

	-	Neutron Networking Components
	-	Revisit the PackStack Answer Files
	-	Quick Network Reconfigure
- Neutron is the OpenStack Networking Service and is another major part of OpenStack. Neutron evolved out of Nova and Provides the Networking elements to the Cloud internals.

	-	Networks and Subnet Ranges
	-	DHCP Agent
	-	Routers
	-	Firewalling
	-	Network Address Translation

# packstack Answer File:
--
	During the install we did set-up some of the networking:
	
# CONFIG_NEUTRON_OVS_BRIDGE_MAPPINGS=physnet1:br-ex
/etc/neutron/plugins/ml2/openvswitch_agent.ini

#CONFIG_NEUTRON_OVS_BRIDGE_IFACES=br-ex:eth0
/etc/neutron/l3_agent.ini

8.2 Verify the Neutron Configuration
---
# grep NEUTRON answers.txt

# grep -C4 NEUTRON_OVS answers.txt

## check the IPv4 network interfaces
# ip -4 a

# ip -4 a s eth0
# ip a

8.3 Understanding Neutron Networking
---
## What we have

# Working with Neutron
# source adminrc

# openstack network list
# neutron net-list
# neutron subnet-list
# neutron agent-list

8.4 Virtual Machines Without Connectivity
----
# openstack network list

# neutron net-list

## on dashboard as demo user

8.5 Provisioning the Network for Interconnectivity
-----
On horizon dashboard --> Created public network as admin

# Created private network, router as demo user

8.6 Connecting to Virtual Machines
---

# Add ssh rule in default security rule

## Launch instance --> network --> demo_private network

## neutron agent-list










