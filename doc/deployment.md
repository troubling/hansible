Deployment of Hummingbird with Ansible
======================================

Prerequisites
-------------

The documentation below assumes:

  1.  A recent version of Ansible is installed on an admin machine or vm that has access to all nodes in the cluster.  This can be easily accomplished by running the `bootstrap.sh` script.
  2.  The user that you will be runing the ansible script as has SUDO access to all nodes in the cluster.

Example Configuration
---------------------

The following configuration is used for the examples in this documentation:

| Server | IP | SATA Devices | SSD Devices |
| ------ | -- | ------------ | ----------- |
| storage1 | 10.1.1.10 | /dev/sdd, /dev/sde, /dev/sdf, /dev/sdg | /dev/sdb, /dev/sdc | 
| storage2 | 10.1.1.11 | /dev/sdd, /dev/sde, /dev/sdf, /dev/sdg | /dev/sdb, /dev/sdc | 
| storage3 | 10.1.1.12 | /dev/sdd, /dev/sde, /dev/sdf, /dev/sdg | /dev/sdb, /dev/sdc |

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

Edit the group variables ('./group_vars/hummingbird/hummingbird') to set cluster specific information.  For more information on group variables, see the Hansible documentation.  The group vars for the example configuration would look like:

```
---
# Devices that will be used for account, container and object storage
storage_devs: ["sdb", "sdc", "sdd", "sde", "sdf", "sdg"]

# If you use separate devices for separate services define them below (for ring creation):
object_devs: ["sdd", "sde", "sdf", "sdg"]
container_devs: ["sdb", "sdc"]
account_devs: ["sdb", "sdc"]

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

Create the Initial Rings
------------------------

Rings will be created in the `/etc/hummingbird` directory on the current machine.  It is *VERY* important to keep backups of the `.builder` files as they will be needed when future ring changes are made.

The `create_rings.yml` playbook will create a ring with each node in a separate zone.  It is also important that all machines in the cluster are available when running this playbook so that it can detect the device sizes to set a proper weight.

The rings should now be able to be created with ansible:

`ansible-playbook -i hosts create_rings.yml`

Install Hummingbird with Ansible
--------------------------------

Hummingbird should now be able to be installed with ansible:

`ansible-playbook -i hosts hummingbird.yml`

If that it completes successfully, then you should have a hummingbird cluster running.  To quickly test if things are running you can try to auth with:

`curl http://10.1.1.10:8080/auth/v1.0 -Hx-auth-user:test:tester -Hx-auth-key:testing -i`

Upgrading Hummingbird
---------------------

By default, hansible will install the latest github release version. In a production environment, you likely want to install a specific version. The release tag can be specified in group_vars. A list of releases can be found here: https://github.com/troubling/hummingbird/releases

Example:

`hummingbird_version: "v0.0.2"`

When it is time to upgrade to "v0.0.3" simply update your group_vars/hummingbird/hummingbird and rerun the playbook. Services will be reloaded after the new binary is downloaded. If any upgrades require any additional steps, those will need to be documented in the hummingbird release version.
