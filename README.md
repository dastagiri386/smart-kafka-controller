# smart-kafka-controller
Smart controller for multi-tenant Kafka setup

The out-of-box ability for Kafka to change its broker cluster topology is somewhat limited. Furthermore, none of the replication tools take into consideration tenant or user requirements to decide on optimal placement of partitions and corresponding replicas. We, hereby, look at designing a tenant requirement centric smart controller for Kafka which also ensures minimum performance guarantees for each tenant.
