PS - Certified OpenStack Administrator (COA)
----
Course developed to learn - Liberty:
=====
Single Machine : Packstack
192.168.56.5

Multi Node: Ubuntu 14.04
----
192.168.56.6

192.168.56.7

===
Packstack installation

Centos7, 20HDD, 4GB RAM

# systemctl disable firewalld NetworkManager

# systemctl stop firewalld NetworkManager

# systemctl start network

# systemctl enable network

@@ Set-up Repos
-----
# yum install -y centos-release-openstack-ocata

# yum install -y bash-completion vim epel-release 

# yum upgrade -y

# reboot

# yum install -y openstack-packstack

@@ Create Answer File and Start Install

# packstack --gen-answer-file=/root/answers.txt

# vim answers.txt or use sed

# packstack --answer-file=/root/answers.txt

#ls ##check the source admin credentials

@@ Check for KVM Support:
---
# grep -Ec '(vmx|svm)" /proc/cpuinfo # 0 =qemu >=1 = kvm

# If KVM is supported edit /etc/nova/nova.conf

	virt_type=qemu
:wq!

# systemctl restart openstack-nova-compute-service

===
2.3 Install OpenStack

2.5 Launching Instance:
-----

- Login to the Dashboard URL --> Access and Security --> Add Rule --> SSh --> Another RUle --> Custom ICMP Rule --> give -1 and save


=======
3.1 Multi-Node Lab Environment:
--
- Install Ubuntu 14.04 Server
- Add OpenStack Repository
- Update Master Image
- Clone Image to Controller and Compute Nodes
- Configure NTP with Chrony

- Ubuntu 14.0.4 - 192.168.56.6
- Ubuntu 14.0.4 - 192.168.56.7

a. Install Ubuntu 14.04 Server
	- Create Master VM Image
	- 14.04 Server
	- Tasksel SSH
	- Configure Static IP
	
- Add the Ocata Release

# apt-get install -y software-properties-common

# apt-get-repository cloud-archive:liberty

#apt-get install -y chrony vim

# apt-get update -y && apt-get dist-upgrade -y

# reboot

3.2 Adding the Repo and Patching the Master
----

#lsb_release -a ## check the server version

# sudo -i

# apt-get install -y software-properties-common chrony vim

# apt-add-repository cloud-archive:liberty

# apt-get update -y && apt-get dist-upgrade -y

# apt-get dist-upgrade -y 

3.3 Setting a Static IP and Hostname Entries
----4

# check the OS release
# lsb_release -d

# Change the IP Address in interfaces files

# sudo vim /etc/network/interfaces

# auto eth0
iface eth0 inet static
	address 192.168.56.8
	netmask 255.255.255.0
	network 192.168.56.0
	broadcast 192.168.56.255
	gateway 192.168.56.1
	dns-nameservers 8.8.8.8
:wq!
:set ai ## auto intend to have a space

## reboot the systemctl

# sudo reboot


3.4 Cloning the machine
----
Clone it from Virtual Box

Change the settings on Controller

# ssh vagrant@192.168.56.8

# sudo -i

# editing the hostname
# vi /etc/hostname
	controller
:wq!

## Configure the static IP

# vi /etc/network/interfaces

iface eth0 inet static
	address 192.168.56.6
	netmask 255.255.255.0
	network 192.168.56.0
	broadcast 192.168.56.255
	gateway 192.168.56.1
	dns-nameservers 8.8.8.8
	
:wq!

## generate new SSH-key Pairs
# cd /etc/ssh
	<remove all the ssh keys>
# rm ssh_host*

# regenrate new ssh keys
# dpkg-reconfigure openssh-server

# sudo reboot

**** Need to do the same on compute node

# ssh vagrant@192.168.56.8

# sudo -i

# editing the hostname
# vi /etc/hostname
	compute
:wq!

## Configure the static IP

# vi /etc/network/interfaces

iface eth0 inet static
	address 192.168.56.7
	netmask 255.255.255.0
	network 192.168.56.0
	broadcast 192.168.56.255
	gateway 192.168.56.1
	dns-nameservers 8.8.8.8
	
:wq!

## generate new SSH-key Pairs
# cd /etc/ssh
	<remove all the ssh keys>
# rm ssh_host*

# regenrate new ssh keys
# dpkg-reconfigure openssh-server

# sudo reboot

3.6 Configuring Time on the Controller and Compute Nodes
-------

# ssh to controller node

# sudo -i

# chrony

# chronyc sources


# ssh to compute node
# sudo -i

# edit chrony configuration
vi /etc/chrony/chrony.conf

<<delete the lines>>
server controller iburst

:wq!

# service chrony restart

#chronyc sources

******
4.1 Installing OpenStack
-----
- Install OpenStack
- Install MySQL Database Server
- Install Rabbit MQ Server

** OpenStack Client : Later OpenStack releases are moving towards a global client that can be used to configure all OpenStack Services. This is the Python Based OpenStack client.

# apt-get install -y python-openstackclient

# openstack --version ## make sure 1.7 or higher

# cat install-openstack-client.sh
	#!/bin/bash 
	apt-get install -y python-openstackclient
:wq!

# openstack --version

## list all the packages
# dpkg -l 

# dpkg -l | grep python-nova 
# dpkg -l | grep python-glance
dpkg -l | grep python-neut

# openstack --help

4.3 Adding the MySQL Database Server
---------
# apt-get install -y mysql-server python-mysqldb

[mysqld]
bind-address = 0.0.0.0
default-storage-engine = innodb
innodb_file_per_table
collation-server = utf8_general_ci
init-connect = 'SET NAMES utf8'
character-set-server = utf8
END

## Restart mysql server
# service mysql restart

## Install MySQL
# cat install-mysql.sh
	# Install MYSQL and Python API
	apt-get install -y mysql-server python-mysqldb
	
	#Configure MYSQL to listen on all interfaces and use UTF-8
	[mysqld]
	bind-address = 0.0.0.0
	default-storage-engine = innodb
	innodb_file_per_table
	collation-server = utf8_general_ci
	init-connect = 'SET NAMES utf8'
	character-set-server = utf8
	END
	
	# Restart MySQL Database Server
	service mysql restart

# apt-get install mysql-server python-mysqldb

# ss -nlt

# ./install-mysql.sh

## show socket command
# ss -nlt

4.4 Adding the Rabbit MQ Server
-----------

# apt-get install -y rabbitmq-server

# rabbitmqctl add_user openstack Password1

# Configure permissions for the account
# rabbitmqctl set_permissions openstack ".*"".*"".*"

## show cockets command again
# ss -ltn
	## *:25672, :::5672, :::4369 are belongs to RabbitMQ Port numbers

## check the users in RabbitMQ
# rabbitmqctl list_users

## Check the permissions for the user in RabbitMQ
# rabbitmqctl list_user_permissions openstack

***
5.1 Installing and configuring Keystone
- Create Database for Keystone
- Install Keystone
- Configure Apache Vhost
- Create identity Elements

## Create the Database

# MYSQL_ROOT_PW=Password1

# cat > create-keystonedb.sql << END
CREATE DATABASE keystone;
GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' IDENTIFIED BY 'Password1';
GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' IDENTIFIED BY 'Password1';
SHOW GRANTS FOR 'keystone'@'%'
END

5.2 Create Database for Keystone:
-----
on controller

# mysql -u root -p 

## show databases;

#quit

# vim create-keystone.sh

	#!/bin/bash
	# MYSQL_ROOT_PW=Password1

	# cat > create-keystonedb.sql << END
	CREATE DATABASE keystone;
	GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' IDENTIFIED BY 'Password1';
	GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' IDENTIFIED BY 'Password1';
	SHOW GRANTS FOR 'keystone'@'%'
	END
	
	#Import SQL File
	mysql -u root -p$MYSQL_ROOT_PW < create-keystonedb.sql
:wq!

# run the above keystone shell script
#./create-keystonedb.sh

## Login to the database

# mysql -u root -pPassword1
# show databases;

# use keystone;

# show tables;

# quit

5.3 Understand the Installation and Configuration of Keystone
----
# echo "manual" > /etc/init/keystone.override

# apt-get install keystone \
	apache2 \
	libapache2-mod-wsgi \
	memcached \
	python-memcache
## We don't want keystone to start so we override it first

## The web-servlet in keystone is depreciated in favor of the apache wsgi module.

## Check the keystone.conf settings
# cat /etc/keystone/keystone.conf

	[DEFAULT]
	verbose = True
	admin_token = Password1
	log_dir = /var/log/keystone
	[database]
	connection = mysql://keystone:Password1@controller/keystone
	[memcache]
	servers = localhost:11211
	[revoke]
	driver = sql
	[token]
	provider = uuid
	driver = memcache
	[extra_headers]
	Distribution = Ubuntu
	
# Populate Keystone Database

# su -s /bin/sh -c "keystone-manage db_sync" keystone

# mysql -u root -p

# use keystone;

# show tables;

## Configure Apache VHOST for keystone
# ./create-keystone-apache-vhost.sh


***
5.4 Installing Keystone and Configuring the Service
---

on controller:

## show sockets
# ss -ntl

D:\Workshops\7-OpenStack\PS-path\1.OpenStack Installing the Lab Environment\openstack-lab-environment\4-openstack-lab-environment-m4-exercise-files\create-keystone-apache-vhost.sh
# vim create-keystone-apache-vhost.sh

## ss -ntl

	
	127.0.0.:11211 ##memcache demon
			:35357 ## keystone service
			: 5000 ## keystone service

## open up the mysql command
#!mysql

	use keystone;
	show tables;
	
	quit;

--
5.4 Managing Keystone Identities

# Authenticate

	# export OS_TOKEN=Password1
	# export OS_URL=http://controller:35357/v3
	# export OS_IDENTITY_API_VERSION=3

# Create Identities:
	# openstack service create --name keystone --description "OpenStack Identity" identity

	# openstack service list

	# openstack service delete keystone

# EndPoints:
	# openstack endpoint create --region RegionOne identity public http://controller:5000/v2.0
	
	# openstack endpoint create --region RegionOne identity internal http://controller:5000/v2.0

	# openstack endpoint create --region RegionOne identity admin http://controller:5000/v2.0

5.6 Creating Keystone Identities from the CLI
----

# export OS_TOKEN=Password1
# export OS_URL=http://controller:35357/v3
# export OS_IDENTITY_API_VERSION=3

# openstack service list

# openstack service create --name keystone --desccription "ID Service" identity

# openstack service list

# openstack service delete keystone

# openstack service list

## vim create-keystone-identities.sh

D:\Workshops\7-OpenStack\PS-path\1.OpenStack Installing the Lab Environment\openstack-lab-environment\4-openstack-lab-environment-m4-exercise-files\create-keystone-identities.sh

# ./create-keystone-identities.sh

6.1 Installing the Glance Image Service : Creating Client Scripts
--------------
	- Create Client Authentication Scripts
	- Glance Image Service
	- Create Glance Database
	- Create Glance Identities
	- Install and Configure Glance
	- Populate Glance Database
	- Create Image

## Client Authentication Script: Admin Account

export OS_PROJECT_DOMAIN_ID=default
export OS_USER_DOMAIN_ID=default
export OS_PROJECT_NAME=admin
export OS_TENANT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=Password1
export OS_AUTH_URL=http://controller:35357/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2

## Client Authentication Script: Admin Account
export OS_PROJECT_DOMAIN_ID=default
export OS_USER_DOMAIN_ID=default
export OS_PROJECT_NAME=demo
export OS_TENANT_NAME=demo
export OS_USERNAME=demo
export OS_PASSWORD=Password1
export OS_AUTH_URL=http://controller:5000/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2

## Using Scripts

# source adminrc.sh

# openstack service list

6.2 Creating the Database
----------

# Create the Database

	vim create-glancedb.sh
	
		#!/bin/bash
		#Make sure you set the variable for the MySQL root password
		MYSQL_ROOT_PW=Password1

		#Create SQL file with SQL code to create DB
		cat > create-glancedb.sql << END
		CREATE DATABASE glance;
		GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'localhost' IDENTIFIED BY 'Password1';
		GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' IDENTIFIED BY 'Password1';
		SHOW GRANTS FOR 'glance'@'%'
		END

		#Import SQL File
		mysql -u root -p$MYSQL_ROOT_PW < create-glancedb.sql
	
	:wq!
	
## Execute the script

./create-glancedb.sh

# mysql -u root -pPassword1

# show databases;
# quit

## Create glance identities:
D:\Workshops\7-OpenStack\PS-path\1.OpenStack Installing the Lab Environment\openstack-lab-environment\5-openstack-lab-environment-m5-exercise-files\create-glance-identies.sh

## Execute ./Create-glancedb.sh

# Openstack service list

# openstack endpoints list

## Install GlanceClient:
----
# apt-get install -y glance python-glanceclient

6.3 Installing and Configuring Glance
---------

## Configuration Files:
---
	/etc/glance/glance-api.conf
	/etc/glance/glance-registry.conf
## Populate the Database 

# su -s /bin/sh -c "glance-manage db_sync" glance

## Regart glance service restart
# service glance-registry restart
# service glance-api restart

## remove the SQLite DB
# rm -f /var/lib/glance/glance.sqlite

## Execute install-glance.sh script
D:\Workshops\7-OpenStack\PS-path\1.OpenStack Installing the Lab Environment\openstack-lab-environment\5-openstack-lab-environment-m5-exercise-files\install-glance.sh

# ./install-glance.sh

## check the shell sockets
# ss -ntl
	:9292 # main service for glance

6.4 Adding Images to Glance
-----------
On controller:

## Download a Test Image
# wget http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img

## Add the image to glance
# source adminrc.sh

# openstack image create --file cirros-0.3.4-x86_64-disk.img --public --disk-format qcow2 --container-format bare cirros

# openstack image list

## execute the below script to run all above commmands

# vim create-glance-image.sh
D:\Workshops\7-OpenStack\PS-path\1.OpenStack Installing the Lab Environment\openstack-lab-environment\5-openstack-lab-environment-m5-exercise-files\create-glance-image.sh

# openstack image list

## if we want to delete the image then we need to delete with the image id not with the name

# ls /var/lib/glance/images

# ls -lh /var/lib/glance/images

********
7.1 Nova Image Service

	- Nova Image Service
	- Create Nova Database
	- Create Nova Identities
	- Install and Configure Nova on Controller
	- Install and Configure Nova on Compute

## Create a Nova Database
D:\Workshops\7-OpenStack\PS-path\1-installation\excersize\6-openstack-lab-environment-m6-exercise-files\nova-01-create-novadb.sh

## Create Identities for Nova
D:\Workshops\7-OpenStack\PS-path\1-installation\excersize\6-openstack-lab-environment-m6-exercise-files\nova-02-create-nova-identities-install.sh

## On a controller node:

# need to execute nova-01-create-novadb.sh
# ./nova-01-create-novadb.sh

# source adminrc.sh ( . adminrc.sh)
# openstack service list

# openstack endpoints list

# openstack endpoint list --service compute

7.3  Configuring the Controller Node
----

# Configuration files
## we should set our controller ip address in nova.conf

# vi /etc/nova/nova.conf
	my_ip = 192.168.56.6(Controller IP)
:wq!

## Populate the Database:
# su -s /bin/sh -c "nova-manage db sync" nova

## Restart the services
# service nova-api restart
# service nova-cert restart
# service nova-consoleauth restart
# service nova-scheduler restart
# service nova-conductor restart
# service nova-novncproxy restart

## Delete the SQLiteDB
# rm -f /var/lib/nova/nova.sqlite

## Configure nova
D:\Workshops\7-OpenStack\PS-path\1-installation\excersize\6-openstack-lab-environment-m6-exercise-files\nova-03-configure-nova-controller.sh

## ss -ntl
	:8774 ## Primary service for Nova Service

7.4 Installing Nova on the Compute Node
-----------
Install Nova on the Compute Node

# apt-get install -y python-openstackclient
# openstack --version
# apt-get install -y nova-compute sysfsutils

## Con compute node

# cat install-nova-compute.sh

# ./install-nova-compute.sh

7.5 Configuring the Compute Node
------------
# cat /etc/nova/nova.conf
my_ip = 192.168.56.7

# check for KVM Support
KVM=$( grep -Ec '(vmx|svm)' /proc/cpuinfo )
if (( $KVM < 1)); then
	echo "Setting QEMU Support"
	sed -i "s/^virt_type\s*=\s*kvm/virt_type=qemu/" \
	/etc/nova/nova-compute.conf
else
	echo "You have KVM Support"
fi

# Restart the service
# service nova-compute restart

# Delete the SQLite DB
# rm -f /var/lib/nova/nova.sqlite

# verify services
# source adminrc.sh
# openstack compute service list

## vim nova-configure-compute.sh
D:\Workshops\7-OpenStack\PS-path\1-installation\excersize\6-openstack-lab-environment-m6-exercise-files\nova-05-nova-configure-compute.sh

# ./nova-configure-compute.sh

# verify services
# source adminrc.sh
# openstack compute service list

----
8.1 Installing Neutron on the Controller Node
---
	- Neutron Network Service
	- Create Neutron Database
	- Create Neutron Identities
	- Install and Configure Neutron on COntroller Node
	- Install and Configure Neutron on Compute Node
	- Launch an Instance
# Creating Database

# Create Identities for Neutron

# Install Neutron on the controller node

# vim 01-neutron-create-neutrondb.sh
D:\Workshops\7-OpenStack\PS-path\1-installation\excersize\7-openstack-lab-environment-m7-exercise-files\01-neutron-create-neutrondb.sh

# ./01-neutron-create-neutrondb.sh

# vim 02-neutron-identities-install-controller.sh
D:\Workshops\7-OpenStack\PS-path\1-installation\excersize\7-openstack-lab-environment-m7-exercise-files\02-neutron-identities-install-controller.sh

## Controller Configuration Files

	/etc/neutron/neutron.conf
	/etc/neutron/plugins/m12/m12_conf.ini
	/etc/neutron/plugins/m12/linuxbridge_agent.ini
	/etc/neutron/dhcp_agent.ini
	/etc/neutron/metadata_agent.ini
	/etc/nova/nova.conf
	
## relationship in Files

m12-conf.ini
[m12_type_flat]

linuxbridge_agent.ini
[linuxbridge]4
physical_interface_mappings = provider:eth0

# populate the database
# su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/m12/m12_conf.ini upgrade head" neutron 

## Restart the services
# service nova-api restart
# service neutron-server restart
# service neutron-plugin-linuxbridge-agent restart
# service neutron-dhcp-agent restart
# service neutron-metadata-agent restart

## Delete the SQLite DB
# rm -f /var/lib/neutron/neutron.sqlite

## 03-neutron-populatedb-restart-services.sh
D:\Workshops\7-OpenStack\PS-path\1-installation\excersize\7-openstack-lab-environment-m7-exercise-files\03-neutron-populatedb-restart-services.sh

# ./!$
# ./03-neutron-populatedb-restart-services.sh

8.3 Installing and Configuring Bridge Agents on the Compute Node
----
# apt-get install -y neutron-plugin-linuxbridge-agent conntrack

# editing the nova.conf
	/etc/neutron/neutron.conf
	/etc/neutron/plugins/m12/linuxbridge_agent.ini
	/etc/nova/nova.conf
# service nova-compute restart
# service neutron-plugin-linuxbridge-agent restart

## install neutron on compute node

# vim 04-neutron-install-configure-compute.sh
D:\Workshops\7-OpenStack\PS-path\1-installation\excersize\7-openstack-lab-environment-m7-exercise-files\04-neutron-install-configure-compute.sh

./04-neutron-install-configure-compute.sh

## On controller node check the sockets
# ss -ntl

## Check the agents
# neutron agent-lit

## neutron extentions support
# neutron ext-list

## 8.4 Creating a Virtual Machine Instance
----

# Create Provider Network
# source /root/adminrc.sh
# neutron net-create provider --shared --provider:physical_network provider --provider:network_type flat

## Create Subnet
# neutron subnet-create provider 10.10.10.0/24 --name provider-subnet 10.10.10.1

## Create Virtual Machine
# source /root/demorc.sh

# openstack server create --flavor m1.tiny --image cirros provider-instance

## On controller
# vim 05-neutron-network-create.sh
./05-neutron-network-create.sh

## ip a s

## Check the namespace
# ip netns

## ip netns exec qdhcp <<ID of the namespace>>

## Creating a virtual machine
# source demorc.sh
# openstack server create --flavor m1.tiny --image cirros --provider-vm

# openstack server list

****
9.1  Installing Horizon on the Controller Node

	Horizon Dashboard Service
	Install Horizon on Controller
	Configure Horizon
	Visit the Dashboard

## Install Horizon on the Controller Node
# apt-get install -y openstack-dashboard

## Horizon configuration file
# /etc/openstack-dashboard/local_settings.py

# service apache2 reload

## execute install script
# ./01-install-dashboard-contoller.sh
D:\Workshops\7-OpenStack\PS-path\1-installation\excersize\8-openstack-lab-environment-m8-exercise-files\01-install-dashboard-contoller.sh

# vim 02-configure-dasboard.sh
D:\Workshops\7-OpenStack\PS-path\1-installation\excersize\8-openstack-lab-environment-m8-exercise-files\02-configure-dasboard.sh

# Execute the scripts
./02-configure-dasboard.sh

9.2 Accessing the Dashboard
----
# Access the Dashboard
# http://controller/horizon

******
10.1Deploying the Storage Node
	- Cinder Block Storage Service
	- Deploy Storage Node
	- Install Cinder on Controller Node
	- Install Cinder on Storage Node
	- Manage Cinder Volumes
	
## Clone Storage Node from Controller node

## lsblk ## check the attached disks

10.2 Installing Cinder on the Controller Nod
---
	- Controller:
	- Create Database
	- Create Identities
	- Install cinder-api cinder-schduler
	- Configure /etc/cinder/cinder.conf
	- Populate Database
	- Add to /etc/nova/nova.conf
	- Restart nova-api cinder-scheduler cinder-api

## Controller:
# vim 01-cinder-create-cinderdb.sh

!#/bin/bash
#Make sure you set the variable for the MySQL root password
MYSQL_ROOT_PW=Password1

# Create SQL file with SQL code to create DB
# cat > create-neutrondb.sql << END
CREATE DATABASE neutron;
GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'localhost' IDENTIFIED BY 'Password1';
GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'%' IDENTIFIED BY 'Password1';
SHOW GRANTS FOR 'neutron'@'%'
END

#Import SQL File
mysql -u root -p$MYSQL_ROOT_PW < create-neutrondb.sql

*****
Replace neutron with cinder on all lines 
:%s/neutron/cinder/g
*****

## Output Would be

# vim 01-cinder-create-cinderdb.sh

!#/bin/bash
#Make sure you set the variable for the MySQL root password
MYSQL_ROOT_PW=Password1

# cat > create-cinderdb.sql << END
CREATE DATABASE cinderdb;
GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'localhost' IDENTIFIED BY 'Password1';
GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'%' IDENTIFIED BY 'Password1';
SHOW GRANTS FOR 'cinder'@'%'
END

#Import SQL File
mysql -u root -p$MYSQL_ROOT_PW < create-cinderdb.sql

## Execute the above script
# ./01-cinder-create-cinderdb.sh

## Start creating our Identities:
----
vim 02-cinder-createinstances-install-controller.sh

#!/bin/bash
source /root/adminrc.sh
openstack user create --domain default --password-prompt cinder
openstack role add --project service --user cinder admin
openstack service create --name cinder --description "OpenStack Block Storage" volume
openstack service create --name cinderv2 --description "Openstack Block Storage" volumev2
openstack endpoint create --region RegionOne volume public http://controller:8776/v1/%\(tenant_id\)s 
openstack endpoint create --region RegionOne volume internal http://controller:8776/v1/%\(tenant_id\)s
openstack endpoint create --region RegionOne volume admin http://controller:8776/v1/%\(tenant_id\)s
openstack endpoint create --region RegionOne volume public http://controller:8776/v2/%\(tenant_id\)s 
openstack endpoint create --region RegionOne volume internal http://controller:8776/v2/%\(tenant_id\)s
openstack endpoint create --region RegionOne volume admin http://controller:8776/v2/%\(tenant_id\)s

apt-get update
apt-get install -y cinder-api cinder-scheduler

## Execute the script
./02-cinder-createinstances-install-controller.sh

## Configuring Cinder

# vi 03-cinder-configure-controller.sh
#!/bin/bash

cat > /etc/cinder/cinder.conf << END
[DEFAULT]
my_ip = 192.168.56.6
rootwrap_config = /etc/cinder/rootwrap.conf
api_paste_config = /etc/cinder/api-paste.ini
iscsi_helper = tgtadm
volume_name_template = volue-%s 
volume_group = cinder-volumes
verbose = True
auth_strategy = keystone
state_path = /var/lib/cinder
local_path = /var/lock/cinder
volumes_dir = /var/lib/cinder/volumes
rpc_backend = rabbit
auth_strategy = keystone
[database]
connection = mysql://cinder:Password1@controller/cinder
[oslo_messaging_rabbit]
rabbit_host = controller
rabbit_userid = openstack
rabbit_password = Password1
[keystone_authtoken]
auth_rui = http://controller:5000
auth_rul = http://controller:35357
memcached_servers = controller:11211
auth_plugin = password
project_domain_name = default
user_domain_name = default
project_name =service
username = cinder
password = Password1
[oslo_concurrency]
local_path = /var/lib/cinder/tmp
END

su -s /bin/sh -c "cinder-manage db sync" cinder

echo -e "[cinder]\nos_region_name = RegionOne" >> /etc/nova/nova.conf

## Execute the above script
./03-cinder-configure-controller.sh

---
10.3  Installing Cinder on the Storage Node
---
	Storage Node:
	Install package lvm2 if required
	Add extra disk /dev/sdb
	Create cinder-volumes volume group
	Edit /etc/lvm/lvm.conf filters
	install package cinder-volumes
	Edit /etc/cinder/cinder.conf
	Restart tgt and cinder-volumes services

vim 04-cinder-storage.sh
# Check the lvm.conf
**update the following lines
filter [ "a/sda/", "a/sdb/", "r/.*/" ] ## Storage Node

filter [ "a/sda/", "r/.*/" ] ##Compute Node

## Configure Storage Node
# lsblk
vim 04-cinder-storage.sh

# vim /etc/lvm/lvm.conf

## 10.4 Verify Cinder Operations
------------
# source .adminrc
# cinder service-list

# Create volume
# source .adminrc
# openstack volume create --size 1 volume1
# openstack volume list
# lsblk

10.4 Verify Cinder Operations
--
# source .adminrc
# cinder service-list

#@ Create volume
# source .adminrc
# openstack volume list
# openstack volume create --size 1 volume1
# openstack volume list
# lsblk

***
11.1 Creating RC Files
---
	Create OpenStack RC File
	Enable TAB Completion
	Verify Services and Authentication
	Using --debug
	Help
# Create OpenStack RC Files
Project > Compute > Access And Security --> Download OpenStack RC File.

11.2 Enabling TAB Completion

# openstack tab completion
# env | grep OS_

# . adminrc.sh

# openstack complete >> adminrc.sh

## Logout
# exit

# relogin
# . adminrc.sh

# openstack service

_------
11.3 Verify Services and Authentication
-----

# openstack endpoint list --service compute
# nova service-list

# openstack endpoint list --service image
# openstack image list

# openstack endpoint list --service network
# neutron agent-list

# openstack endpoint list --service cinderv2
# cinder agent-list

## Testing Authentication
# openstack token issue

# openstack user show <user_id>

## Debug
# openstack token issue --debug

*****
11.4 Gaining Help
---

# openstack help compute service list
# openstack compute service list -c Binary -c Host -c Status -c State

# openstack compute service list -f yaml










