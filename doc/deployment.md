Deployment of Hummingbird with Ansible
======================================

Prerequisites
-------------

The documentation below assumes:

  1.  Ansible is installed on an admin machine or vm that has access to all nodes in the cluster.
  2.  The user that you will be runing the ansible script as has SUDO access to all nodes in the cluster.

Example Configuration
---------------------

The following configuration is used for the examples in this documentation:

| Server | IP | SATA Devices | SSD Devices |
| ------ | -- | ------------ | ----------- |
| storage1 | 10.1.1.10 | /dev/sdd, /dev/sde, /dev/sdf, /dev/sdg | /dev/sdb, /dev/sdc | 
| storage2 | 10.1.1.11 | /dev/sdd, /dev/sde, /dev/sdf, /dev/sdg | /dev/sdb, /dev/sdc | 
| storage3 | 10.1.1.12 | /dev/sdd, /dev/sde, /dev/sdf, /dev/sdg | /dev/sdb, /dev/sdc |

Configuring the Ring
--------------------

If you do not yet have a Hummingbird binary, it can be downloaded directly from https://troubling.github.io/hummingbird/bin/hummingbird

The ring is managed outside of Ansible with the `hummingbird` command line.  Ansible will distribute the ring files to the nodes of the cluster.  The ring files will need to be stored in `/etc/hummingbird` on the admin node:

  1.  Create the etc dir for the ring: `sudo mkdir -p /etc/hummingbird`
  2.  Set the permissions: `sudo chown -R $USER.$USER /etc/hummingbird`

It can be useful to create a script to create the initial account, container and object rings.  When configuring the ring, a good starting point is to use `3` replicas, a part power of `22`, and a min part hours of `162` for most clusters.  The following example also uses the SATA devices for the object servers and the SSD devices for the account and container servers.  For more advanced info on using the ring, see the Hummingbird documentation.

`make_rings.sh`:
```
#!/bin/bash

cd /etc/hummingbird

hummingbird ring object.builder create 22 3 168
hummingbird ring object.builder add r1z1-10.1.1.10:6000/sdd 100
hummingbird ring object.builder add r1z1-10.1.1.10:6000/sde 100
hummingbird ring object.builder add r1z1-10.1.1.10:6000/sdf 100
hummingbird ring object.builder add r1z1-10.1.1.10:6000/sdg 100
hummingbird ring object.builder add r1z2-10.1.1.11:6000/sdd 100
hummingbird ring object.builder add r1z2-10.1.1.11:6000/sde 100
hummingbird ring object.builder add r1z2-10.1.1.11:6000/sdf 100
hummingbird ring object.builder add r1z2-10.1.1.11:6000/sdg 100
hummingbird ring object.builder add r1z3-10.1.1.12:6000/sdd 100
hummingbird ring object.builder add r1z3-10.1.1.12:6000/sde 100
hummingbird ring object.builder add r1z3-10.1.1.12:6000/sdf 100
hummingbird ring object.builder add r1z3-10.1.1.12:6000/sdg 100
hummingbird ring object.builder rebalance

hummingbird ring container.builder create 22 3 168
hummingbird ring container.builder add r1z1-10.1.1.10:6001/sdb 100
hummingbird ring container.builder add r1z1-10.1.1.10:6001/sdc 100
hummingbird ring container.builder add r1z2-10.1.1.11:6001/sdb 100
hummingbird ring container.builder add r1z2-10.1.1.11:6001/sdc 100
hummingbird ring container.builder add r1z3-10.1.1.12:6001/sdb 100
hummingbird ring container.builder add r1z3-10.1.1.12:6001/sdc 100
hummingbird ring container.builder rebalance

hummingbird ring account.builder create 22 3 168
hummingbird ring account.builder add r1z1-10.1.1.10:6001/sdb 100
hummingbird ring account.builder add r1z1-10.1.1.10:6001/sdc 100
hummingbird ring account.builder add r1z2-10.1.1.11:6001/sdb 100
hummingbird ring account.builder add r1z2-10.1.1.11:6001/sdc 100
hummingbird ring account.builder add r1z3-10.1.1.12:6001/sdb 100
hummingbird ring account.builder add r1z3-10.1.1.12:6001/sdc 100
hummingbird ring account.builder rebalance
```

Note: It is important to keep the `*.builder` files for when modifications of the rings are made

Setup Ansible for Hummingbird
-----------------------------

Check out the Hansible repository which is responsible for Ansible playbooks and roles for Humminbird.

  1.  `git clone https://github.com/troubling/hansible.git`
  2.  `cd hansible`

Edit the inventory (`./hosts') to reflect your hardware configures.  For more information on configuring the inventory, see the Hansible documentaiton.  An example inventory for the example configuration would look like:

```
[hummingbird]
10.1.1.10 service_ip=10.1.1.10
10.1.1.11 service_ip=10.1.1.11
10.1.1.12 service_ip=10.1.1.12
```

Edit the group variables ('./group_vars/hummingbird') to set cluster specific information.  For more information on group variables, see the Hansible documentation.  The group vars for the example configuration would look like:

```
---
# Devices that will be used for storage
storage_devs: ["sdb", "sdc", "sdd", "sde", "sdf", "sdg"]


proxy_port: 8080
# Only change the following if you are not going to use default ports
#object_port: 6000
#container_port: 6001
#account_port: 6002
#object_replicator_port: 6500
#container_replicator_port: 6501
#account_replicator_port: 6502

# Set the following to true if you would like to use tempauth
use_temp_auth: true
hash_prefix: changeme
hash_suffix: changeme
filebeat_logstash_hosts:
  - "localhost"
filebeat_logging_paths:
  - paths:
    - '/var/log/hummingbird/*.log'
```

Install Hummingbird with Ansible
--------------------------------

Hummingbird should now be able to be installed with ansible:

`ansible-playbook -i hosts hummingbird.yml`

