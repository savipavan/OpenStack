4.Nova and Neutron
----------------
- Internal Networks
- Nova Instances
- Agile Environment

2.1 Objectives Covered from the COA Exam
----
- Introduce course contents
- Nova - Compute Service
- Neutron - networking service
- Orchestration with Heat
- Troubleshooting
- Fresh Install

# From the requirements
- Compute - Nova (15%)
	- Manage flavors
	- Manage instances
	- Add floating IP
	- Configure security group rules
	- Host consoles
	- Snapshot instances
	- Manage quotas
- Networking - Neutron(16%)
	- Manage network resources, including networks, subnets, routers
	- Manage quotas
	- Security group rules
	- Troubleshoot networking
- Orchestration - Heat (8%)
	- Launch a stack from a template
	- Create templates

- Troubleshooting(13%)
	- Analyze logs
	- Backup Databases
	- Analyze Components

2.2 Creating the Lab Environment
------
Lab Environment in single node using packstack

Centos7 192.168.56.5

- This is Final Course can be a stand-alone module and looks at the main openstack components of Noa and Neutron

3.1 Lab Environment Single Node
--
- Install OpenStack with packstack


## check memory
# free -g

### check the free disk space
# df -h

4.1 Networking with Neutron
---------
- Networking Objects
- Neutron Services
- Flat Networks
- VXLAN networks
- Service Groups
- Floating IPs

## Networking Components
# Instances = Virtual Machines
# Virtual Interfaces(VIFs- Virtual Interfaces) or vNICs(Virtual Network Interface Cards) appear in the instance and connect it to the project network. The connection is made through a port and VIFs are seen in the instance only.

# Port:
# neutron port-list

## Project Network
# neutron net-list

# Subnet
# neutron subnet-list

# Routers:
# neutron router-list

4.2 Investigating Network Objects
------------
# source keystonerc_admin

# neutron port-list
# neutron net-list
# neutron subnet-list

# neutron router-list

# neutron router-list -c name -c external_gateway_info

4.3 Neutron Services and OpenvSwitch
--------
## Neutron Services
# systemctl status neutron-*

## Open vSwitch
# ovs-vsctl -V
# ovs-vsctl add-br b1
# ovs-vsctl del-br b1
# ovs-vsctl show

## br-int : Integration Bridge: Each Openstack host has a single integration bridge. This bridge allows for all VIFs to be connected to the bridge. The OVS Neutron Agent creates br-int

## br-ex : External Bridge: The Bridge allows connection with the external network. A Physical NIC from the host will be connected to this bridge.

## br-tun : Tunnel Bridge: This bridge allows for the termination of tunnel endpoints where GRE or VXLAN tunnels are created.

## View Configuration
# grep -o '^[^#]*' /etc/neutron/plugins/ml2/openvswitch_agent.ini

# neutron router-list

## Check all the openstack service status
# openstack-status

# systemctl status
# systemctl status neutron-*

## Open vSwitch
# ovs-vsctl -V
# ovs-vsctl show
# ovs-vsctl add-br b1
# ovs-vsctl del-br b1

# ovs-vsctl show

# grep -o '^[^#]*' /etc/neutron/plugins/ml2/openvswitch_agent.ini

4.5Understanding Networking Types
------------------
# Flat Networks

## Enable Flat Networks:

# /etc/neutron/plugins/ml2/ml2_conf.ini
	type_drivers = vxlan, flat

## VXLAN Networks:
---

4.6 Configuring Networking in Horizon Dashboard
----
-> Login as Demo user --> network topology --> networks --> Routers --> Delete all networks 

--> login as admin
--> System --> Networks --> Delete network

--> Create Network --> Name=external --> Project:services --> network Type= VXLAN --> segmentation id = 42 --> check the box for "External network" --> Create Network

## Create a subnet:
# click on external network --> Create subnet --> subnet ame:external_subnt --> NetworkAddress: 192.168.0.0/24 --> Next --> uncheck the dhcp --> Allocation Pool= 172.16.0.199,172.16.0.254 --> DNS Name Servers=8.8.8.8 --> Create

4.7 Creating the Demo Project Network
--------
## check the virtual interface
# neutron port-list

# neutron net-list

# neutron subnet-list

## creating demo network and demo router

--> login to horizon --> network --> networks --> Creating the network --> Network Name=demo_network --> subnet --> Subnet Name=demo_subnet --> network address = 192.168.1.0/24 --> next --> Subnet Details --> Enable DHCP --> Allocation Pools --> 192.168.1.2,192.168.1.254 --> DNS Server: 8.8.8.8 --> complete

## Create Routers:
Create router --> name : demo_router --> external Network= external --> create

## click on router --> interfaces --> Add interface --> subnet: demo_network --> IP Address 192.168.1.1 --> Add Interface

## neutron port-list

4.8 Understanding Security Groups Floating IP Addresses
---
## Security Groups
# openstack security group list
# openstack security group show default
# openstack security group rule list default

# # openstack security group create --proto icmp default

# openstack security group rule create --proto tcp --dst-port 22 default

## Floating IP Address
---
# neutron floatingip-list
# neutron floatingip-create external
# neutron floatingip-list

# neutron port-list

4.9 Working at the CLI with Security Groups and Floating IP Addresses
---
# openstack security group list
# openstack security group show
# openstack security group rule list default
# openstack security group rule create --proto icmp default
# openstack security group rule list default
# openstack security group rule create --proto tcp --dst-port 22 default
# openstack security group rule list default

## network address translation rules (or) Floating IPAddress
# neutron floatingip-list
# neutron floatingip-create external
# neutron floatingip-list
# neutron port-list


5.1 Nova Compute Service
---
- Virtual machine instances
- Associate Floating IP Address
- Customize scripts
- Managing Virtual Machines

# Virtual Machines

5.3 Launching Instances from the CLI
----

# neutron port-list

# openstack server list

# opentack server list --project demo

## source keystonerc_demo

# openstack server list

# openstack server create --image cirros --flavor m1.tiny --nic net-id=demo_network vm2

# openstack server list

# nuetron port-list

5.4 Local Interaction Between Instances
---------
# Login as demo user in dashboard

--> Launch the console --> try ping and ssh to the other server

5.5 Using Floating IP Addresses
----
## Floating IPAddress

## Security Groups
--> Access & Security --> Floating IPs --> New Allocate IP --> --> Associate to new VM

## ping 172.16.0.204

5.6 Implementing Security Groups
-------
## SSH Keys

# pwd
# cd .ssh
# pwd
# ls
# cat id_rsa.pub
<<Copy the content>>

# dashbaord --> ASccess & Security --> Keypais --> Import key --> Key Pair Name: host --> Public Key --> 

# Instanaces --> Launch Instance --> Add keypair --> Host Key --> Launch


# try connect to the the instance from Command Prompt
# ssh-keygen -R 172.16.0.204

# ssh cirros@172.16.0.204

5.7 Automation with Automation Scripts
------
Dashboard --> Launch Instance --> Default Sercurity key --> Post-Creattion --> upload file or script data

	#!/bin/sh
	echo '192.168.1.1 router' >> /etc/hosts
	
5.8 Understanding Actions
----
## Pause: VM does not consume CPU, contents in RAM
## Suspend: Similar to pause but at hypervisor level
## Shelve: Similar to shutoff but creates a snapshot and disconnects from hypervisor
## Lock: Prevent changes

--> Dashboard --> vm --> Created snapshots --> Create new instance from snapshot --> 

6.1 Welcome to HEAT
--------
- Understanding HEAT
- Writing HOT Files
- Launch a Stack
- Delete a Stack
- Launch Stack with Parameters
- Restacking with Heat

## HEAT: Orchesration mechanism for OpenStack

## HEAT Services
# openstack-heat-api:	Active
# openstack-heat-api-cfn: inactive (disabled on boot)
# openstack-heat-api-cloudwatch: inactive (disabled on boot)
# openstack-heat-engine: active

6.2 HEAT Services
------
# openstack-status

# heat --version

6.3 Heat Templates
----
# Template Format HOT
	Version
	Optional Parameters
	Resource
	Optional Output
	
## Simple HOT Template:
	heat_template_version: 2015-10-15
	description: Deploy Cirros VM
	Resources:
		resources1:
			properties:
				key_name: host
				image: cirros
				flavor: m1.tiny
				name: vm1

## heat template-version-list

# heat stack-create -f stack.yml my_stack

# heat stack-list
# heat stack show my_stack
# heat stack-delete my_stack

6. 3Launch Stack from CLI
--------
# openstack server list

# vim stack.yml

	heat_template_version: 2015-10-15
	description: Deploy Cirros VM
	Resources:
		my_vm1:
			type: OS::Nova::Server
			properties:
				key_name: host
				image: cirros
				flavor: m1.tiny
				name: vm1
		my_vm2:
			type: OS::Nova::Server
			properties:
				key_name: host
				image: cirros
				flavor: m1.tiny
				name: vm2
:wq!

# heat stack-create -f stack.yml my_stack

# heat stack-list
# heat stack-show my_stack

# openstack server list
# openstack stack-delete my_stack

# openstack server list

# heat template-version-list

6.5  Launch Stack from Dashboard
---------
Dashboard --> Orchestration --> Stacks --> Launch Stack --> Direct input --> past the code --> name: mystack

Verify the instances.

Shutdown stack : suspend the stack

Resume stack : power-it back

6.6 Working User_Data into Stacks
-----------

vim stack_data.yml

resources:
	my_vm1:
		type: OS::Nova::Server
		properties:
			key_name: host
			image: cirros
			flavor: m1.tiny
			name: vm1
			user_data_format: RAW
			user_data: |
				#!/bin/sh
				echo '192.168.1.1 router' >> /etc/hosts

## cat stack_data.yml

# heat stack-create -f stack_data.yml my_stack

6.7 Create SSH Key Pairs with Stack
------
## OS::Nova::KeyPair

vi key.yml
	heat_template_version: 2015-10-15
	description: KEY PAIR
	resources:
		cloud_key
			type: OS::Nova::KeyPair
			properties:
				name: cloud
				public_key: 'ssh-rsa
				<< rsa key hash code>> '

# cat key.yml

# heat stack-create -f key.yml <<Stack Name>>
# heat stack-create -f key.yml my_key
# heat stack-list

6.8 Working with Stack Parameters and Variable Data
-------

vim stack.yml

## Optional Parameters
	heat_template_version: 2015-10-15
	description: Simple Template
	parameters:
		image_id:
			type: string
			label: Image ID
			description: Image to be used for compute instance
	resources:
		my_vm1:
		type: OS::Nova::Server
		properties:
			key_name: host
			image: { get_param: image_id }
			flavor: m1.tiny
			name: vm1

## heat stack-create -f stack.yml -P image_id=cirros s1

## delete stack
# heat stack-delete s1

6.9 Using Stacks to Launch Instances with Volumes Attached
-------
## Cinder Volumes: Heat can create and attach Cinder Volumes. In this way we can create an instance and have a volume connected to it directly.

## cat stack_volume.yml
heat_template_version: 2015-04-30
resources:
my_vm:
	type: OS::Nova::Server
	properties:
		image: cirros
		flavor: m1.tiny
		name: vm1
my_vol:
	type: OS::Cinder::Volume
	properties:
		size: 1
		name: vol1
vol_att:
	type: OS::Cinder::VolumeAttachment
	properties:
		instance_uuid: { get_resource: my_vm }
		volume_id: { get_resource: my_vol }
		mountpoint: /dev/vdb

## heat stack-create -f !$ (or)
heat stack-create -f stack_volume.yml s1

7.1 Troubleshooting OpenStack
------
- Spaces not TABS
- Network Namespaces(ip netns)
- Configuration Files
- Service Status
- Logfiles

## HOT Format: Heat templates written to the HOT format are in YAML format. Indentations should be with spaces and not tabs. Use cat-vet <filename> and look for tabs show with ^1

7.2 Spaces and not Tabs in HOT Files
---

# cat stack.yml
	heat_template_version: 2015-04-30
	description: Simple Template
	resources:
	my_vm:
		type: OS::Nova::Server
		properties:
			key_name: host
			image: cirros
			flavor: m1.tiny
			name: vm1

# cat indent.yml

	heat_template_version: 2015-04-30
	description: Simple Template
	resources:
	my_vm:
		type: OS::Nova::Server
		properties:
			key_name: host
			image: cirros
			flavor: m1.tiny
			name: vm1
## heat stack-create -f indent.yml s1

# cat -vet indent.yml
^1

# vim .vimrc
	set ai expandtab ts=2 nohls
:wq!

# cat -vet indent.yml

7.4 Troubleshooting Networks
---------
## Floating IP Address:
- To be accessible, floating IP address need to be in the same address range as your existing physical network.
- The Allocation range should not be from the DHCP range to ensure address do not clash.
- If you use the default public network it is unlikely to be correct for your physical subnet.

## Network name spaces: Using the ip acommand we can determine a lot about connectivity using the subcommand netns we can run commands from other networks on the system.

# ip addr show
# ip route show
# ip netns show
# ip netns exec <router-namespace> ping 192.168.1.xx

## Working with Network Namespaces

## IPAddress Show
# ip addr show
# ip a
# ip -4 a

## Routes show
# ip -4 r

## Namespaces
# ip netns

## ip netns exec <<router id>> ip a

## If we want to ping the internal server
# ip netns exec <<router id>> ping 192.168.1.2

7.4 Configuration Debugging
--------
## Configuration Files: Most serviecs will have configuration files located in /etc/<servicename>. Most have a setting verbose=True enabled by default. This increases logging but i would encourage that this is only set when required.

## verbose=True
Verbose logging is useful in troubleshooting but adds to the size of the log file.
# grep -o '^[^#]*' /etc/nova/nova.conf | less

## size of the log file
# ls -lh /var/log/nova/nova-api.log

# tail -n 0 -f /var/log/nova/nova-api.log

## Change Logging Level:
With verbose=False and the service restarted only WARNING and higher events are logged, so the simpel openstack server list does not record in your logs when successful.

## Command Level Verbosity: The client can show more details if required when the command is run, just add the --debug option

# openstack server list --debug
# nova --debug list

## Configuration level
# less /etc/nova/nova.conf

# grep -o '^[^#]*' !$
# grep /etc/nova/nova.conf

# grep /etc/nova/nova.conf | less

# ls -lh /var/log/nova/nova-api.log

# tail -n0 -f /var/log/nova/nova-api.log

# openstack server list

## edit configuration
# vim /etc/nova/nova.conf
	verbose=False

## restart the service
# systemctl restart openstack-nova-api.service

## run the below command on 2 terminal sessions and check the log file

# tail -n0 -f /var/log/nova/nova-api.log
# openstack server list


## openstack server list --debug

7.5 Checking Service Status
---------
# openstack-status
# nova service-list
# neutron agent-list
# cinder service-list
# heat service-list

## Service Status: The openstack-status command is great to quickly see the status of both the OpenStack and supporting services. Most OpenStack services have their own mechanism to check their status

## MariaDB Status: A quick overview of the database server status can be gained with mysqladmin. The questions field show the number of SQL queries whilst it has been running. If you used my answer file then the root password is Password!. If you haven't secured the SQL server the Linux root user can login without the -u and -p switches

# mysqladmin -u root -p status

## Check the OpenStack server status
# openstack-status

# nova service-list
# neutron agent-list
# cinder service-list
# heat service-list

# mysqladmin status
# mysqladmin -u root -p status

7.6 Working with Log Files
-------------
## Log Files: Log files can be located in /var/log/<service>. The journalctl command can also be used

## Tail : To read the end of a log we can use tail. The follow the end of a log use -f. To start with a clear screen and follow only new activity use -f -n0

## check the last 10 lines
# tail /var/log/nova/nova-api.log

## check the last 10 lines and follow the logs
# tail -f /var/log/nova/nova-api.log

## check the new lines only
# tail -n0 -f /var/log/nova/nova-api.log

## Journalctl : As part of systemd we also have the command journalctl. This can display logs as a unified entity. We can choose to display entries from a specific service with the -u option.

# journalctl
# journalctl -u openstack-nova-api
# journalctl -u openstack-heat-engine

## Working with Logs
# ls /var/log/nova

# ls /var/log/neutron

# tail /var/log/nova/nova-api.log

# tail -f /var/log/nova/nova-api.log









	













