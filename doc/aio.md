# Creating a hummingbird AIO with hansible
This can be useful when needing to do some initial testing or dev work

###  Create a vm
Create a vm with an extra storage device (This document uses `/dev/vdb` as an example).  A Debian based distro is recommended as that is what we currently dev, test and deploy with.  These instructions can be easily adapted for other distros though.

### Install ansible
You can use **bootstrap.sh** to install ansible
```
./bootstrap.sh
```

### Edit any group_var variables
For a basic AIO the only thing you need to change is the storage_devs refernce in **group_vars/hummingbird** to `"vdb"`


### Edit the inventory file 
Uncomment the line containing **127.0.0.1** in the **hummingbird** section only 


### Install hummingbird
Run the **aio.yml** playbook to install hummingbird and wait for the vault password prompt
```
ansible-playbook -i hosts aio.yml --vault-id @prompt
```

### Verify the install was successful 
Run hummingbird bench to make sure install worked
```
hummingbird bench tests/temp_bench.conf
```

### Simple clean 
Perfrom these steps to stop the service, remove config, ring and exe files.  Also delete the data
 * Stop the service
 * Remove the rings and configuration files
 * Remove the hummingbird executable
 * Remove the data directories for account, containers and objects
 
if you want to reset the disk completely then add `reset: "yes"` to the **group_vars/hummingbird** file

Cleanup commands
```
service hummingbird-* stop
rm /etc/hummingbird/{*.gz,*.conf}
rm /usr/local/bin/hummingbird
rm -rf /srv/node/aio/{accounts,containers,objects}
```


