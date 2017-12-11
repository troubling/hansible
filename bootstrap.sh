
#!/bin/bash

# Install ansible 2.3

apt-get install --yes software-properties-common
apt-add-repository ppa:ansible/ansible
apt-get update
apt-get install --yes ansible


