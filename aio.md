
# Creating a hummingbird AIO with hansible

###  Create a vm
The easiest way to get started is to install the AIO on a virtual machine

Item | Value | Reference
--- | --- | ---
RAM | 16384 
DISK |   100GB
VCPUS |     8
Attached Volume | 100GB | /dev/vdb


### Install ansible
You can use **bootstrap.sh** to install ansible
```
./bootstrap.sh
```

### Edit any group_var variables
For a basic AIO the only thing you need to change is the obj_dev refernce in **group_vars/hummingbird** to `"vdb"`


### Install hummingbird
Run the **aio.yml** playbook to install hummingbird
```
# password asdf
ansible-playbook -i hosts aio.yml  --vault-id=@prompt
```

### Verify the install was successful 
Run hummingbird bench to make sure install worked
```
hummingbird bench tests/temp_bench.conf
```




