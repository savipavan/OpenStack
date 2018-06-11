3. OpenStack: Managing Identities and Objects
========
1.1 Course Overview:
---
	-	Configuring Keystone V3 API
	-	Customized Master Image
	-	Storing Configuration with Swift

2.1 Welcome to OpenStack Object and Identities
---
Objectives:
	- Keystone - Identity Service
	- Cinder - Volume Service
	- Glance - Image Service
	- Swift - Object Storage

2.2 OpenStack Exam Requirements We Match
---
-	Identity Management - Keystone(12%)
	- Manage Keystone Catalog services and endpoints
	- Manage/Create Domains, Groups, Projects, Users and roles
	- Manage the Identity Service
	- Verify the Identity Service
-	Block Storage - Cinder (10%)
	- Manage Volumes
	- Create Volume Groups for storage
	- Create Volume and Mount to instance
	- Manage quotas
	- Manage backups
	- Manage snapshots
	- Manage encryption
	- Setup Storage Pools
	- Monitor Capacity
	- Analyze Volume size reports
- Image Management - Glance (10%)
	- Deploy a new image to instance
	- Manage image types and back-ends
	- Manage Images
	- Verify image services
- Object Store - Swift (10%)
	- Manage access to Object Store
	- Manage expiring Objects
	- Manage Policies
	- Verify object store
	- Manage permissions on containers
	
2.3 Lab Requirements
-------------
Openstack : Installing the Lab Environment
Openstack : Getting to know OpenStack and the COA

Lab Environment ( Single Node )
	- Packstack - Centos 7 - 192.168.56.5

Highlights:
	- Convert CLI and Horizon to use Keyston V3 API
	- Create your own images
	- Snapshot volumes
	- Use Swift to store central configuration files

2.4 Keystone Identity API
------
- Check API version for keystone
- Create service and endpoint records
- Manage Domins, users, groups, roles
- Understand the keystone configuration
- Issue tokens

## Check Functionality of the v2 API
# source keystonerc_admin
# openstack domain list
# openstack endpoint list

# Standard V2 Credentials:
-------
Unset OS_SERVICE_TOKEN
export OS_USERNAME=admin
export OS_PASSWORD=Password1
export OS_AUTH_URL=http://192.168.56.5:5000/v2.0
export PS1='[\u@\h \W(keystone_admin)]\$ '
export OS_TENANT_NAME=admin
export OS_REGION_NAME=RegionOne


# Standard V3 Credentials:
-------
Unset OS_SERVICE_TOKEN
export OS_USERNAME=admin
export OS_PASSWORD=Password1
export OS_AUTH_URL=http://192.168.56.5:5000/
export OS_IDENTITY_API_VERSION=3
export OS_PROJECT_DOMAIN_NAME=Default
export OS_USER_DOMAIN_NAME=Default
export PS1='[\u@\h \W(keystone_admin)]\$ '
export OS_TENANT_NAME=admin
export OS_REGION_NAME=RegionOne

## Check Functionality of the V3 API

# source keystonerc_adminv3
# openstack domain list
# openstack endpoint list

3.2 Updating to Version 3 Credentials
---

# source keystonerc_admin

# openstack domain list
## Since it is v2 api it wont give the domain list

# openstack endpoint list

# cp keystonerc_admin keystonerc_adminv3

# vim keystonerc_adminv3

## Modify the source file
	Unset OS_SERVICE_TOKEN
	export OS_USERNAME=admin
	export OS_PASSWORD=Password1
	export OS_AUTH_URL=http://192.168.56.5:5000/
	export OS_IDENTITY_API_VERSION=3
	export PS1='[\u@\h \W(keystone_admin)]\$ '
	export OS_TENANT_NAME=admin
	export OS_REGION_NAME=RegionOne

# . keystonerc_adminv3

# openstack domain list

# openstack endpoint list

# openstack endpoint list --service identity

3.3 Managing Services and Endpoints
-----
## Manage Service Entries:
---

# openstack service create | delete | show | list

# openstack service create --name "heat" orchestration
# openstack service list
# openstack service show heat
# openstack service delete heat

## Manage Endpoints:
----
- Public: facing users, the main cloud users
- internal: communication between cloud nodes
- admin: Reserved for cloud administration. Not Internet facing

## When creating service entries for keystone, port 5000 is the user port and port 35357 is reserved for admin. The Version 3 API is denoted with v3 not v3.0

# openstack endpont create --region RegionOne identity public http://192.168.56.5:5000/v3

# openstack endpoint create --region RegionOne identity admin http://192.168.56.5:35357/v3

## when we delete endpont we need to use ID rather than name

3.4 Working with Services and Endpoints from the CLI
-----
## Managing service entries
# openstack service list

## create service entries
# openstack service create --name "heat" orchestration

# openstack service list

## Look the detail
# openstack service show heat

# openstack service delete heat
# openstack service list

# openstack endpoint list --service identity
## these are v2 entries

### Create v3 entries
# openstack endpoint create --region RegionOne identity public http://192.168.56.5:5000/v3

# openstack endpoint create --region RegionOne identity admin http://192.168.56.5:35357/v3

## openstack endpoint list --service identity


3.5 V3 Domains
----
## Create new domain
# source keystonerc_adminv3
# openstack domain create pluralsight

## Add User to New Domain
# openstack user create --password Password1 --domain pluralsight ps_admin

# openstack user list

# openstack user list --domain pluralsight

## adding user in to admin roles
# openstack role add --user ps_admin --domain pluralsight admin

# openstack role list --user ps_admin --domain pluralsight

# Credentials File for ps_admin

	unset OS_SERVICE_TOKEN
	export OS_USERNAME=ps_admin
	export OS_PASSWORD=Password1
	export OS_AUTH_URL=http://192.168.56.5:5000/
	export OS_IDENTITY_API_VERSION=3
	export PS1='[\u@\h \W(ps_admin)]\$ '
	export OS_USER_DOMAIN_NAME=pluralsight
	export OS_DOMAIN_NAME=pluralsight
	export OS_REGION_NAME=RegionOne

3.6 Working with Domains
----

# source keystonrc_adminv3
# source complete

# openstack complete > complete
# source complete

# openstack domain create pavan
# openstack user create --password Password1 --domain pavan ps_admin

# openstack user list

# openstack user list --domain pavan

# openstack role add --user ps_admin --domain pavan admin

## openstack role list --user ps_admin --domain pavan

## Log out and login back again

## Create source file
# cp keystonerc_adminv3 keystone_ps

# vim keystone_ps
	unset OS_SERVICE_TOKEN
	export OS_USERNAME=ps_admin
	export OS_PASSWORD=Password1
	export OS_AUTH_URL=http://192.168.56.5:5000/
	export OS_IDENTITY_API_VERSION=3
	export PS1='[\u@\h \W(ps_admin)]\$ '
	export OS_USER_DOMAIN_NAME=pavan
	export OS_DOMAIN_NAME=pavan
	export OS_REGION_NAME=RegionOne

# . keystone_ps

# openstack user create --password Password1 --domain pavan bob

3.7 Working with Projects
-------
## Projects is a container that groups or isolates resources or identity objects. Projects were previously called tenants and were the main openstack container before Domains. Now we have Domains these are very much more like Organizational Units in LDAP directories creating sub-groupings for administration

## Projects in OpenStack
---
# openstack project create slc
# openstack project list
# openstack project show slc
# openstack user create --password Password1 leah
# openstack role add --project slc --user leadh _member_

## openstack project list
# openstack domain list

# openstack user create --password Password1 leah

## openstack role add --project slc --user leah _member_

3. 8 Working with Groups
--------
Groups: Another V3 API Identity object that allows users to be gathered together and the group to be added to a role. Like users, groups are created within the domain

## Openstack groups
# openstack group list

# openstack group create --domain pavan ops
# openstack group add user ops bob

# openstack group list
# openstack group list --user bob

***
4.1Introduction to Glance
---
	- Glance Services
	- Disk Formats
	- Container Formats
	- Creating Image Files
	- Managing Images with Glance

## Glance Services
The API service accepts incoming requests to the server.
The Registry service stores and retrieves metadata about Glance Images
Both Configuration files can be found in /etc/glance on the server.

# systemctl | grep glance

## Verify the Glance Services:
---
# systemctl 
# systemctl | grep glance

# cd /etc/glance
# ls
# grep sql glance-api.conf 

## quotas:
# grep quota !$(##last argument) (or)
# grep quota glance-api.conf

4.3 Understanding Virt-builder
------
# Disk Formats

## type		-> Description
# raw		-> Unstructured disk image format
# qcow2		-> QEMU file that can dynamically grow and supports copy on write
# vhd		-> Common format use by Xen, VMWare, VirtualBox and Microsoft
# iso		-> Archive format used by CDROMs
# aki		-> Amazon Kernel Images
# ari		-> Amazon Ram Disk Images
# ami		-> Amazon Machine Images

## Container Formats:
--
# Type	-> Description
# bare	-> There is no metadata in the image
# ovf 	-> OVF container format
# ova 	-> OVA tar archive
# docker -> Docker archive

## Download and Customize Images:
---
# yum whatrprovides *virt-builder
# yum install -y libguestfs-tools
# virt-builder -l
# cd /tmp
# virt-builder centos-7.3 --format qcow2 --install "cloud-init,epel-release,vim" --selinux-relabell

## Create Image from the CLI
# openstack image create --disk-format qcow2 --container-format bare --public --file centos7.3 centos7

4.4 Using Virt-builder
----
# check the virt-builder tool
# yum whatprovides *virt-builder

# yum install -y libguestfs-tools

# cd /tmp
# virt-builder -l

# virt-builder centos-7.3 --format qcow2 --install "cloud-init,epel-release,vim,tree" --selinux-relabel --root-password password:Password1 

4.5 Creating Glance Images
---------

## ls /tmp
## we can find the centos-7.3.qcow2 file

# mv centos-7.3.qcow2 /root/
# cd
# ls

# . keystonerc_admin

# openstack image create --disk-format qcow2 --container-format bare --public --file centos-7.3.qcow2 centos7

4.6 Deploying Instances
--
Dashboard --> check the image

5.1 Welcome to Cinder
-------
-	Identify Cinder Services
- Understand Cinder Services
- Identify Cinder Back Ends
- Create Cinder Volume Group
- Managing Cinder Quotas
- Volume Snapshots

## Cinder Services:
---
Cinder has been in OpenStack since the Folsom release and replaces the nova-volume service

There are a few services for Cinder as you will see but they share the one configuration file /etc/cinder/cinder.conf

# systemctl | grep cinder
# cinder service-list

# API: interface to Cinder from clients and generally will run on the controller node

# Schedular: Takes requests from API and has them run by the cinder volume service. Usually runs on the Controller

# Volume: Interacts with the back end storage

# Backup: Interface allowing backup of volumes to services like swift

## Cinder back Ends:
# cinder-manage service list
# ls /usr/lib/python2.7/site-packages/cinder/volume/drivers
# grep lvm /etc/cinder/cinder.conf

5.2 Cinder Services
-------
# systemctl | grep cinder

# cinder service-list
# ls
# ls /usr/lib/python2.7/site-packages/cinder/volume/drivers/

# grep lvm /etc/cinder/cinder.conf

5.3 Volumes and Volume Types
--------
Volumes : We have seen these already and they are block storage devices that have an independent lifecycle to virtual machine instances.

# Volume Types: 

# In horizon dashboard --> Login as Admin --> Volumes --> Volume Types --> Actions --> Extra Specs --> 

# login as demo user --> images --> volumes --> Create Volume --> 

5.4 Understanding Multiple Back-ends
---------
## Multiple Cinder Back Ends

# grep lvm /etc/cinder/cinder.conf
# Cinder.conf
[DEFAULT]
enabled_backends = lvm

## Define New Volume Group:
--
# dd if=/dev/zero of=/root/disk.img bs=100 count=1M

# losetup /dev/loop2 /root/disk.img

# pvcreate /dev/loop2

# vgcreate cinder-volume2 /dev/loop2

5.5 Configuring Volume Groups
--------
# dd if=/dev/zero of=/root/file1 bs=100 count=1M

# lsblk
# losetup /dev/loop2 /root/file1
# lsblk

## creat lvm structure
# pvcreate /dev/loop2
# vgcreate cinder-vol2 /dev/loop2

## volume group scan
# vgs

5.6 Configuring Additional Storage Back-ends
----
# vgs
# pwd
# ls

# less cinder.conf
# sed -i.bak '/^s*#/d;/^d' cinder.conf
	enabled_backends = lvm,lvm-b
	[lvm-b]
	iscsi_helper=lioadm
	volume_group=cinder-vol2
	iscsi_ip_address=192.168.56.5
	volume_driver=cinder.volume.drivers.lvm.LVMVolumeDriver
	volumes_dir=/var/lib/cinder/volumes
	iscsi_protocol=iscsi
	volume_backend_name=lvm-b
:wq!

# systemctl restart openstack-cinder-api.service openstack-cinder-volume.service openstack-cinder-backup.service

# cinder-manage service list

5.7 Creating Volume Types
----
# login horizion as admin --> volumes --> volume Types --> Create new volume type --> Name:gold --> view entra sepc --> key:volume_backend_name --> value: lvm-b -> ok

# login as demo user

# volumes --> create a new volume --> type : see both types --> gold --> 

5.8 Enabling Quotas
----
## Manage Volume Quotas
# openstack quota show demo
# openstack quota set --volumes 15 demo

## Manage Storage Quotas
# . adminrc
# openstack quota show demo

# openstack quota set --volumes 15 demo
# openstack quota show demo

## restricint the gold volumes
# openstack quota set --volumes 2 --volume-type gold demo

# openstack quota show demo

5.9 Enabling Snapshots
======
## Manage Volume Snapshots
--
# source keystonerc_demo
# cinder list
# cinder snapshot-list
# cinder snapshot-create <volume-name> --name snap1
# cinder snapshot-create vol1 --name before-update
# cinder snapshot-list
# cinder snapshot-delete snap1

6.1 Introducing Swift
-------
- Identify Swift Services
- Swift Hierarchy
- Using Swift
- Expiring Objects

# Swift Services:
--
Swift is the openstack object store.

# systemctl | grep swift

# Listing Swift Objects
# swift stat

## . keystone_admin
# systemctl | grep swift
# swift stat

6.2 Uploading Content to Swift
------
# Swift can act as a configuration store. We may need a shared configuration file to be stored in Swift and downloaded to instances as required.

## Uploading content
# swift stat

# swift upload hosts /etc/hosts
# swift list hosts
# swift stat hosts etc/hosts

## Upload Swift Content
---
# swift stat

# swift upload hosts /etc/hosts
# swift stat

# swift list hosts

# swift stat hosts etc/hosts

6.3 Downloading Content and ACLS
------
## swift client

## Download Content
# swift download hosts

## manage ACLs : Swift post can be used to set the Access Control List to a container.

# SWIFT post hosts -r "demo:demo"
# swift stat hosts

## Clear Read ACL, just send empty string
# swift post hosts -r ""
# swift stat hosts

# SWIFT post hosts -w "demo:demo"

## Manage ACL and Downloads

6.4 Managing Expiring Objects and Deletions
-------
## Expire Objects : Objects can be automatically deleted at a specific date and time or after a specified number of seconds

## Unix Time : To delete at a specifc data and time we use the Unix Time Epoch

# date

## Unix Date
# date +%s

# date --date '30 days'

## Unix Date
# date --date '30 days' +%s

# swift post hosts etc/hosts -H "X-Delete-At:1495466045"

## check the policy status on the object
# swift stat hosts etc/hosts

## Delete after certain number of seconds
# swift post hosts etc/hosts -H "X-Delete-After:86400"

## Delete container
# swift delete hosts












	