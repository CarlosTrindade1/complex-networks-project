import networkx as nx

graph = nx.DiGraph()

graph.add_edge('a', 'b')
graph.add_edge('b', 'c')
graph.add_edge('c', 'a')
graph.add_edge('a', 'd')
graph.add_edge('b', 'e')

for position, node in enumerate(graph):
    print(position)
    print(node)
    print('---')

dag = nx.condensation(graph)

print("-"*100)

print(dag)
print(dag.nodes())
print(dag.edges())
print(dag.graph["mapping"])

print("-"*100)

print(list(nx.topological_sort(dag)))

for scc in reversed(list(nx.topological_sort(dag))):
    print(dag.nodes[scc]["members"])
    for node in dag.nodes[scc]["members"]
        print(sum)