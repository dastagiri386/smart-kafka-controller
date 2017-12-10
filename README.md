# smart-kafka-controller

## Introduction

The out-of-box ability for **Kafka** to change its broker cluster topology is somewhat limited. Furthermore, none of the replication tools take into consideration tenant or user requirements to decide on optimal placement of partitions and corresponding replicas. 

We, hereby, look at designing a tenant requirement centric smart controller for Kafka which also ensures minimum performance guarantees for each tenant. You can see detailed progress [here](add link to report here)

## Running the controller

We use [CloudLab](https://cloudlab.us/) for design and demonstration of our controller. Other distributions used are as follows :
* [Confluent 3.3.1](https://www.confluent.io/previous-versions/)
* [Zookeeper 3.4.6](https://archive.apache.org/dist/zookeeper/)

We consider a three-node Kafka cluster and two tenants with different throughput requirements hosted on bare metal CloudLab physical machines. All nodes are connected to 10Gbps ethernet network. 

To motivate the need for a better Kafka controller with multiple tenants, we consider producers running on each tenants with [**acks=1**](https://kafka.apache.org/documentation/#producerconfigs).



