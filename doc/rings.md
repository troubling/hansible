Managing Hummingbird Rings with Hansible
========================================

Adding Nodes to the Ring
------------------------

Adding nodes to the ring is as simple as adding the new node in the inventory and running the `rings.yml` playbook.

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
| object_ring_replicas          | Number of replicas in the object ring    | 3       |
| container_ring_replicas       | Number of replicas in the container ring | 3       |
| account_ring_replicas         | Number of replicas in the account ring   | 3       |
| object_ring_part_power        | Partition power of the object ring       | 22      |
| container_ring_part_power     | Partition power of the container ring    | 22      |
| account_ring_part_power       | Partition power of the account ring      | 22      |
| object_ring_min_part_hours    | min_part_hours for the object ring       | 168     |
| container_ring_min_part_hours | min_part_hours for the container ring    | 168     |
| account_ring_min_part_hours   | min_part_hours for the account ring      | 168     |

*NOTE*:  These variables can only be set before the rings are initially created.
