./software/confluent-3.3.1/bin/kafka-topics --zookeeper localhost:2181 --delete --topic testA
./software/confluent-3.3.1/bin/kafka-topics --zookeeper localhost:2181 --delete --topic testB

./software/confluent-3.3.1/bin/kafka-topics --zookeeper localhost:2181 --create --topic testA --partitions 1 --replication-factor 2
./software/confluent-3.3.1/bin/kafka-topics --zookeeper localhost:2181 --create --topic testB --partitions 1 --replication-factor 2

./software/confluent-3.3.1/bin/kafka-topics --zookeeper localhost:2181 --describe --topic testA
./software/confluent-3.3.1/bin/kafka-topics --zookeeper localhost:2181 --describe --topic testB
