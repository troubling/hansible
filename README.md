Hansible
========

TL;DR
-----

1.  Install the latest version of [Ansible](http://docs.ansible.com/ansible/latest/intro_installation.html) or run `bootstrap.sh` if you are on a Debian based distro.
2.  Edit the hosts file to have the hosts you want and modify variables as needed.
3.  Create rings for the cluster.
4.  Run the hummingbird playbook `ansible-playbook -i hosts hummingbird.yml` to install and configure the latest hummingbird.

Inventory
---------

Each storage node should be listed in the `hummingbird` group.  The `service_ip` variable is the ip that the non-public services will listen on.  

### hummingbird group variables

Variable | Description
-------- | -----------
`storage_devs` | A list of devices used as storage for servers.  This can also be overriden at the server level.
`proxy_port` | Port the proxy server will listen on.
`container_port` | Port the container server will listen on.
`account_port` | Port the account server will listen on.
`auth_uri` | Auth URI for keystone
`auth_url` | Auth URL for keystone
`authtoken_username` | Username to use when validating auth with keystone.
`authtoken_password` | Password to use when validating auth with keystone.

Playbooks
---------

### hummingbird.yml

This playbook will install and configure the latest version of hummingbird to all of the nodes in the `hummingbird` group.

### keystone.yml

This playbook will install a dockerized keystone that we use for development and testing.

### monitoring.yml

This playbook will install a dockerized prometheus, grafana & alertmanager.

Secrets
-------
```
ansible-vault encrypt_string <string_to_encrypt> --ask-vault-pass
```

Will prompt you for a password. It results in:

```
!vault |
          $ANSIBLE_VAULT;1.1;AES256
          31633734306439336165653439346662323730393765633466353634333133316566373961663739
          6539633735306336373465306336373366653761656666620a653464373461363234346339333431
          37376337396362346266613061383862323636316432353230633136656161313661643939363866
          3838346232316434360a633964643434633763336565386339643764616566383661373663333062
          34316463363061633363623339383864626162323661396262303562656433343233
```

You can paste this into a yaml inventory file. (Not an INI file.)

```
hummingbird:
  hosts:
    localhost:
  vars:
    hash_prefix: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          31633734306439336165653439346662323730393765633466353634333133316566373961663739
          6539633735306336373465306336373366653761656666620a653464373461363234346339333431
          37376337396362346266613061383862323636316432353230633136656161313661643939363866
          3838346232316434360a633964643434633763336565386339643764616566383661373663333062
          34316463363061633363623339383864626162323661396262303562656433343233
```

Then when you execute it, just pass in:

```
sudo ansible-playbook -i hosts.yml hummingbird.yml --vault-id @prompt
```

Keys and Certs
--------------

Two vars need to be placed in your inventory.

* ca\_key\_content: CA private key pem
* ca\_cert\_content: CA cert pem

It's highly encouraged to encrypt this file:

```
ansible-vault encrypt group_vars/hummingbird/ca.yml --ask-vault-pass
```

An example can be found in ansible/examples/ca.yml, which you can use (password: asdf):
```
mkdir group_vars/hummingbird
cp examples/ca.yml group_vars/hummingbird/
ansible-vault edit group_vars/hummingbird/ca.yml
ansible-vault rekey group_vars/hummingbird/ca.yml --ask-vault-pass
```


Generating the CA key:

```
openssl genrsa -out /path/to/key.pem 4096
```

Generate the self signed CA cert (from the hummingbird dir):

```
openssl req -config ansible/keys/ca.conf -key /path/to/key.pem -new -x509 -days 3560 -extensions ca_ext -out /path/to/ca.cert.pem -subj "/CN=Hummingbird CA"
```


Monitoring
----------
### Monitoring group variables

Variable | Description
-------- | -----------
`grafana_admin_user` | Admin user for Grafana UI
`grafana_admin_password` | Encrypted Grafana admin password
`alertmanager_route` | Routes for Alertmanager
`alertmanager_receivers` | Receivers config for alerts
`prometheus_scrape_configs` | This section specifies set of targets and parameters describing how to scrape them

To install monitoring role:

```
sudo ansible-playbook -i hosts.yml monitoring.yml --vault-id @prompt
```

Filebeat
---------
This role was yanked from https://github.com/rcbops/rpc-role-filebeat.

It can be minimally configured with two variables:

```
filebeat_logging_paths:
  - paths:
    - '/var/log/hummingbird/*.log'
filebeat_logstash_hosts:
  - '<logstash_host>'
```

For an INI inventory, I used a group\_vars/hummingbird yml file. If using a yml inventory, you can just put these directly in there.
