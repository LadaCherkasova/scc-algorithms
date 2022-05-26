import random
from collections import defaultdict
import matplotlib.pyplot as plt
import time

def generator(vertex):
     graph = defaultdict(list)
     edge = random.randint(1, vertex * (vertex - 1) / 2)
     counter = edge

     while counter > 0:
          x = random.randint(1, vertex * vertex)
          q = x // vertex + 1
          r = x % vertex + 1

          if q != r:
               if graph[q]:
                    if r not in graph[q]:
                         graph[q].append(r)
                         counter = counter - 1
               else:
                    graph[q].append(r)
                    counter = counter - 1

     for i in range(vertex):
          if not graph[i]:
               graph[i] = []

     return graph, edge

def kosaraju(graph):
     def first_dfs(graph):
          visited = set()
          order = []

          def dfs(v):
               visited.add(v)
               for u in graph[v]:
                    if u not in visited:
                         dfs(u)
               order.append(v)

          for u in list(graph.keys()):
               if u not in visited:
                    dfs(u)

          return order

     def second_dfs(graph, order):
          visited = set()
          components = defaultdict(list)
          stack = []

          for u in reversed(order):
               if u not in visited:
                    visited.add(u)
                    stack.append(u)

                    while stack:
                         item = stack.pop()

                         for v in graph[item]:
                              if v not in visited:
                                   visited.add(v)
                                   stack.append(v)
                         components[u].append(item)
          return components

     reversed_graph = defaultdict(list)
     for u in graph.keys():
          for v in graph[u]:
               reversed_graph[v].append(u)

     order = first_dfs(graph)
     return second_dfs(reversed_graph, order)

def tarjan(graph):
     stack = []
     onstack = set()
     indexes = dict()
     links = dict()
     components = defaultdict(list)
     visited = set()

     def strong_connect(v):
          global counter
          indexes[v] = counter
          links[v] = counter
          counter = counter + 1
          stack.append(v)
          onstack.add(v)
          visited.add(v)

          for u in graph[v]:
               if u not in visited:
                    strong_connect(u)
                    if links[v] > links[u]:
                         links[v] = links[u]
               else:
                    if u in onstack and links[v] > indexes[u]:
                         links[v] = indexes[u]

          if links[v] == indexes[v]:
               while True:
                    w = stack.pop()
                    onstack.remove(w)
                    components[v].append(w)
                    if w == v:
                         break

     for u in list(graph.keys()):
          if u not in visited:
               strong_connect(u)
     return components

def gabow(graph):
     stack = []
     path = []
     indexes = dict()
     components = defaultdict(list)
     done = set()
     visited = set()

     def strong_connect(v):
          global counter
          indexes[v] = counter
          counter = counter + 1
          stack.append(v)
          path.append(v)
          visited.add(v)

          for w in graph[v]:
               if w not in visited:
                    strong_connect(w)
               else:
                    if w not in done:
                         while indexes[path[-1]] > indexes[w]:
                              path.pop()

          if path[-1] == v:
               while True:
                    last = stack.pop()
                    components[path[-1]].append(last)
                    done.add(last)
                    if last == v:
                         break
               path.pop()

     for u in list(graph.keys()):
          if u not in visited:
               strong_connect(u)
     return components

counter = 1

# 1. Random graphs analysis

plt.xlabel("Сумма количества вершин и количества ребер")
plt.ylabel("Время работы, с")

for i in range(100, 301):
     graph, edges = generator(i)

     time_start1 = time.time()
     kosaraju(graph)
     time_end1 = time.time()

     if time_end1 - time_start1 <= 0.05:
          plt.scatter(i + edges, time_end1 - time_start1, color="blue")

     time_start2 = time.time()
     tarjan(graph)
     time_end2 = time.time()
     if time_end2 - time_start2 <= 0.05:
          plt.scatter(i + edges, time_end2 - time_start2, color="green")

     time_start3 = time.time()
     gabow(graph)
     time_end3 = time.time()
     if time_end3 - time_start3 <= 0.05:
          plt.scatter(i + edges, time_end3 - time_start3, color="red")

# 2. Analysis graph from http://snap.stanford.edu/data/email-Eu-core.html

file = open("email-Eu-core.txt", "r")
web_graph = defaultdict(list)
web_graph_edges = 0
web_graph_vertex = set()

while True:
     line = file.readline()
     if not line: break

     node_1, node_2 = line.strip().split(' ')

     web_graph[int(node_1)].append(int(node_2))
     web_graph_edges += 1
     if node_1 not in web_graph_vertex:
          web_graph_vertex.add(node_1)
     if node_2 not in web_graph_vertex:
          web_graph_vertex.add(node_2)

for i in range(200):
     time_start1 = time.time()
     kosaraju(web_graph)
     time_end1 = time.time()

     if time_end1 - time_start1 < 0.01:
          plt.scatter(i, time_end1 - time_start1, color="blue")

     time_start2 = time.time()
     tarjan(web_graph)
     time_end2 = time.time()

     if time_end2 - time_start2 < 0.01:
          plt.scatter(i, time_end2 - time_start2, color="green")

     time_start3 = time.time()
     gabow(web_graph)
     time_end3 = time.time()

     if time_end3 - time_start3 < 0.01:
          plt.scatter(i, time_end3 - time_start3, color="red")

file.close()

plt.show()

