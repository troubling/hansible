Managing Hummingbird Rings with Hansible
========================================

Adding Nodes to the Ring
------------------------

Adding nodes to the ring is as simple as adding the new node in the inventory and running the `rings.yml` playbook.  If you are using a separate replication network, make sure you set the `replication_ip` variable for each node.  For example a node with a service ip of `10.1.1.10` and a repliaction ip of `10.2.2.10` would look like:

```
[hummingbird]
10.1.1.10 service_ip=10.1.1.10 replication_ip=10.2.2.10
```

Removing Nodes from the Ring
----------------------------

To remove a node from the ring, the node should stay in the inventory, and set the `state` variable for that node in the inventory to `remove`.  For example, if you wanted to remove node `10.1.1.10` from the ring, its entry in the inventory might look something like:

```
[hummingbird]
10.1.1.10 service_ip=10.1.1.10 state=remove
```

Ring Configuration
------------------

The following ring properties can be set in `group_vars/hummingbird/hummingbird`:

| Var                           | Definition                               | Default |
| ----------------------------- | ---------------------------------------- | ------- |
| object_ring_replicas          | Number of replicas in the object ring    | 6       |
| container_ring_replicas       | Number of replicas in the container ring | 3       |
| account_ring_replicas         | Number of replicas in the account ring   | 3       |
| object_ring_part_power        | Partition power of the object ring       | 20      |
| container_ring_part_power     | Partition power of the container ring    | 20      |
| account_ring_part_power       | Partition power of the account ring      | 20      |
| object_ring_min_part_hours    | min_part_hours for the object ring       | 168     |
| container_ring_min_part_hours | min_part_hours for the container ring    | 168     |
| account_ring_min_part_hours   | min_part_hours for the account ring      | 168     |

*NOTE*:  These variables can only be set before the rings are initially created.
