#!/bin/bash

hummingbird ring object.builder create 10 1 1
hummingbird ring object.builder add r1z1-127.0.0.1:6000R127.0.0.1:6500/aio 1
hummingbird ring object.builder rebalance

hummingbird ring container.builder create 10 1 1
hummingbird ring container.builder add r1z1-127.0.0.1:6001/aio 1
hummingbird ring container.builder rebalance

hummingbird ring account.builder create 10 1 1
hummingbird ring account.builder add r1z1-127.0.0.1:6002/aio 1
hummingbird ring account.builder rebalance
