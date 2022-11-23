import requests
import json
import paramiko
from py2neo import Node, Relationship, Graph, NodeMatcher
import neo4jupyter
from ast import literal_eval

neo4jupyter.init_notebook_mode()

graph = Graph("bolt://localhost:7687", auth=("neo4j", "neo4j_test"))
graph.run("Match (n) detach delete n")  ## clean the exist graph in the project
node_matcher = NodeMatcher(graph)


private_key = paramiko.RSAKey.from_private_key_file('C://Users//Ruibin//.ssh//id_rsa')

# 创建SSH对象
ssh = paramiko.SSHClient()

# 允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 连接服务器
ssh.connect(hostname='10.121.10.239', port=22, username='rwang', pkey=private_key)


# 执行命令
commands = "source ~/anaconda3/bin/activate text2KG && cd '/tmp/pycharm_project_939' && python main.py"
# commands = "source ~/anaconda3/bin/activate text2KG && cd '/tmp/pycharm_project_939' && ~/anaconda3/envs/text2KG/bin/python3.8 main.py"
stdin, stdout, stderr = ssh.exec_command(commands)

# 获取命令结果
result = stdout.read()


# print(stderr.read())
# print(result.decode('utf-8'))

# 关闭连接
# ssh.close()

## result的输出是str类型的list，采用第三方模块将其转化成list
entity_pair = literal_eval(result.decode('utf-8'))

# entity_pair = [[0.9397001286877047, 'south-eastern Ukraine', 'consists', 'of Luhansk and Donetsk oblasts'], [0.9151265598185118, 'Russia', 'began a large military build-up along its border with Ukraine amassing', "up to 190,000 troops and their equipment. Despite the build-up, denials of plans to invade or attack Ukraine were issued by various Russian government officials up to the day before the invasion. On 21 February 2022, Russia recognised the Donetsk People's Republic and the Luhansk People's Republic, two self-proclaimed breakaway quasi-states in the Donbas"], [0.9499287288593953, 'Russia', 'annexed', 'Crimea'], [0.9023946766454398, 'Russia', 'began', 'a large military build-up along its border with Ukraine'], [0.866473419484604, 'denials of plans', 'were issued up', 'by various Russian government officials'], [0.9681777807375632, 'Russia', 'recognised', "the Donetsk People's Republic and the Luhansk People's Republic"], [0.8850659690664333, 'Russian-backed paramilitaries', 'seized part of the Donbas region of south-eastern Ukraine sparking', 'a regional war'], [0.9579134693618594, 'Russian-backed paramilitaries', 'seized', 'part of the Donbas region of south-eastern Ukraine']]


head_entities = []
relations = []
tail_entities = []


## extract the head, tail and relation from the entity_pair
for index in entity_pair:
    if index[0] > 0.7: # when the confidence max then 0.7, keep them
        head_entities.append(index[1])
        relations.append(index[2])
        tail_entities.append(index[3])



## delete the duplicated entities
sorted_head_entities = list(set(head_entities))
sorted_tail_entities = list(set(tail_entities))


## create the node
for index in range(len(sorted_head_entities)):
    graph.create(Node("head_entity", name = sorted_head_entities[index]))

for index in range(len(sorted_tail_entities)):
    graph.create(Node("tail_entity", name = sorted_tail_entities[index]))


## connect the node with the relation
for index in range(len(relations)):
    exist_head_node = node_matcher.match("head_entity").where(name=head_entities[index]).first()
    exist_tail_node = node_matcher.match("tail_entity").where(name=tail_entities[index]).first()
    relation_arrow = Relationship(exist_head_node, relations[index], exist_tail_node)
    graph.create(relation_arrow)



