import os

def main():
	topicA = "testA"
	topicB = "testB"
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

main()
