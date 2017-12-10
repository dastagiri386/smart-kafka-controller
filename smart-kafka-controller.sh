
python customController.py
/users/ajayt6/software/confluent-3.3.1/bin/kafka-reassign-partitions --zookeeper localhost:2181 --reassignment-json-file cluster-reassign.json --execute > allout.txt 2>&1
python printResults.py

