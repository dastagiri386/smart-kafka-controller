import os
from subprocess import call 
import time

topicNameSuffix = str( time.time() )

print "[MESSAGE] Checking requirements for both tenants ...."
copyString = "scp -i key/id_rsa_group2.pem node-%d:/users/ajayt6/tenant_configuration.json ./tenant_configuration%d.json >> customControllerLog.log"
os.system(copyString%(3,3))
os.system(copyString%(4,4))

f = open("tenant_configuration3.json", 'r')
l = f.readlines()
f.close()

bandwidthA = l[0].split(':')[1]
topicA = l[1].split(':')[1][:-1] + topicNameSuffix

f = open("tenant_configuration4.json", 'r')
l = f.readlines()
f.close()

bandwidthB = l[0].split(':')[1]
topicB = l[1].split(':')[1][:-1] + topicNameSuffix

createString = "./software/confluent-3.3.1/bin/kafka-topics --zookeeper localhost:2181 --create  --partitions 1 --replication-factor 2 --topic %s"
deleteString = "./software/confluent-3.3.1/bin/kafka-topics --zookeeper localhost:2181 --delete --topic %s"


createA = os.popen(createString%topicA).read()
createB = os.popen(createString%topicB).read()

print "[MESSAGE] Fetched requirements from all tenants. Requirements are as follows:"
print ""
print "Bandwidth required for topic testA: " + str(bandwidthA) + \
 "Bandwidth required for topic testB: " + str(bandwidthB)
#print bandwidthA, bandwidthB, topicA, topicB

if int(bandwidthA.replace("Gbps", "")) + int(bandwidthB.replace("Gbps", "")) <= 10:
	print "[MESSAGE] Throughput guarantees for both tenants can be met. Exiting now"
	exit()
else:
	print "[MESSAGE] Current partition replica placement is as follows:"
	topicString = "/users/ajayt6/software/confluent-3.3.1/bin/kafka-topics --zookeeper localhost:2181 --describe --topic %s"
	outA = os.popen(topicString%topicA).read()
	leaderA = int(outA.split('\n')[1].split('\t')[3].split(' ')[1])
	followerA = map(int, outA.split('\n')[1].split('\t')[4].split(' ')[1].split(','))
	followerA = [ item for item in followerA if item != leaderA][0]
	print "For topic testA: leader replica at node: "+str(leaderA) + ", follower replica at node: " + str(followerA)
	

	outB = os.popen(topicString%topicB).read()
        leaderB = int(outB.split('\n')[1].split('\t')[3].split(' ')[1])
        followerB = map(int, outB.split('\n')[1].split('\t')[4].split(' ')[1].split(','))
        followerB = [ item for item in followerB if item != leaderB][0]
	print "For topic testB: leader replica at node: "+str(leaderB) + ", follower replica at node: " + str(followerB)

	#-------------------------------------------------------------------
	print ""
	print ""
	if leaderA == leaderB: # scenario 1: when both leaders are collocated
		print "[STATE] Partition replicas placement is not optimal. Leader replicas are collocated"
		leaderB = followerA
		followerA = followerB
		print "[MESSAGE] Optimal placement for replicas computed "

	else:
		leaders = [leaderA, leaderB]
		followers = [followerA, followerB]

		collocated_follower = set(leaders).intersection(set(followers))
		if len(collocated_follower) == 0: # scenario 2: This is an optimized placement already
			print "[STATE] Leader replicas reside on different brokers. Follower replicas not collocated with any leader"
			print "[MESSAGE] Partition replicas placement is optimal. No changes needed."
			exit()
		else:
			print "[STATE] Partition replicas placement is not optimal. A leader is collocated with a slave."
			final_follower = list( set(followers) - collocated_follower)[0]
			followerA = final_follower
			followerB = final_follower
			print "[MESSAGE] Optimal placement for replicas computed "




	#-------------------------------------------------------------------a
	print ""
	print ""
	print "[MESSAGE] Saving optimal replica placement configuration"
	import json
	with open("cluster-reassign.json") as cf:
		jsonDict = json.load(cf)
	
	os.remove("cluster-reassign.json")
	
	jsonDict["version"] = 2
	jsonDict["partitions"][0]["topic"] = topicA
	print topicA
	jsonDict["partitions"][0]["replicas"][0] = leaderA
	jsonDict["partitions"][0]["replicas"][1] = followerA
	
	jsonDict["partitions"][1]["topic"] = topicB
	jsonDict["partitions"][1]["replicas"][0] = leaderB
	jsonDict["partitions"][1]["replicas"][1] = followerB
	
	print jsonDict
	#Dump the json to cluster-reassign.json
	with open('cluster-reassign.json','w') as cf:
		json.dump(jsonDict,cf)

	with open('cluster-reassign.json','r') as cf:
		reloadD = json.load(cf)
		print "immediately aftyer dumping the dict is: " + str(reloadD)
	#-------------------------------------------------------------------a
	print ""
	print ""
	print "[MESSAGE] Triggering partiion reassignment tool with optimal replica placement configuration"
	reassignString = "/users/ajayt6/software/confluent-3.3.1/bin/kafka-reassign-partitions --zookeeper localhost:2181 --reassignment-json-file cluster-reassign.json --execute"
	os.system(reassignString)
	
	#-------------------------------------------------------------------a
	print "[MESSAGE] Current partition replica placement is as follows:"
	topicString = "/users/ajayt6/software/confluent-3.3.1/bin/kafka-topics --zookeeper localhost:2181 --describe --topic %s >> customControllerLog.log"
	outA = os.popen(topicString%topicA).read()
	leaderA = int(outA.split('\n')[1].split('\t')[3].split(' ')[1])
	followerA = map(int, outA.split('\n')[1].split('\t')[4].split(' ')[1].split(','))
	followerA = [ item for item in followerA if item != leaderA][0]
	print "For topic testA: leader replica at node: "+str(leaderA) + ", follower replica at node: " + str(followerA)
	

	outB = os.popen(topicString%topicB).read()
        leaderB = int(outB.split('\n')[1].split('\t')[3].split(' ')[1])
        followerB = map(int, outB.split('\n')[1].split('\t')[4].split(' ')[1].split(','))
        followerB = [ item for item in followerB if item != leaderB][0]
	print "For topic testB: leader replica at node: "+str(leaderB) + ", follower replica at node: " + str(followerB)


	#-------------------------------------------------------------------a

outA = os.popen(deleteString%topicA).read()
outB = os.popen(deleteString%topicB).read()

'''
./software/confluent-3.3.1/bin/kafka-topics --zookeeper localhost:2181 --delete --topic testA
./software/confluent-3.3.1/bin/kafka-topics --zookeeper localhost:2181 --delete --topic testB

./software/confluent-3.3.1/bin/kafka-topics --zookeeper localhost:2181 --create --topic testA --partitions 1 --replication-factor 2
./software/confluent-3.3.1/bin/kafka-topics --zookeeper localhost:2181 --create --topic testB --partitions 1 --replication-factor 2

./software/confluent-3.3.1/bin/kafka-topics --zookeeper localhost:2181 --describe --topic testA
./software/confluent-3.3.1/bin/kafka-topics --zookeeper localhost:2181 --describe --topic testB
'''
