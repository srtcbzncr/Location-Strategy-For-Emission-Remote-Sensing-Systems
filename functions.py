import networkx as nx
import matplotlib.pyplot as plt
import sys
import random

def createGraph1():
    print("Graph is creating...")
    #Directed Graph for junctions and roads.
    g = nx.DiGraph()
    g.add_node(1, pos=(1,2))
    g.add_node(2, pos=(2,2))
    g.add_node(3, pos=(3,2))
    g.add_node(4, pos=(1,1))
    g.add_node(5, pos=(2,1))
    g.add_node(6, pos=(3,1))
    g.add_edges_from([(2,1),(1,2),(2,3),(4,1),(2,5),(5,2),(3,6),(5,4),(6,5)])
    print("Graph is created.")
    return g

def createGraph2():
    print("Graph is creating...")
    #Directed Graph for junctions and roads.
    g = nx.DiGraph()
    g.add_node(1, pos=(2,4))
    g.add_node(2, pos=(3,4))
    g.add_node(3, pos=(1,3))
    g.add_node(4, pos=(2,3))
    g.add_node(5, pos=(3,3))
    g.add_node(6, pos=(4,3))
    g.add_node(7, pos=(2,2))
    g.add_node(8, pos=(3,2))
    g.add_node(9, pos=(4,2))
    g.add_node(10, pos=(1,1))
    g.add_node(11, pos=(2,1))
    g.add_node(12, pos=(3,1))
    g.add_node(13, pos=(4,1))
    g.add_edges_from([(2,1),(1,4),(5,2),(4,3),(3,4),(6,5),(5,6),(3,10),(10,3),(4,7),(8,5),(6,9),(9,6),(7,8),(9,8),(7,11),(8,12),(12,8),(9,13),(13,9),(11,10),(10,11),(12,11),(11,12),(13,12),(12,13)])
    print("Graph is created.")
    return g

def createGraph3():
    print("Graph is creating...")
    #Directed Graph for junctions and roads.
    g = nx.DiGraph()
    for i in range(27):
        g.add_node(i)
    g.add_edges_from([(1,2),(1,7),(2,3),(3,4),(3,9),(4,5),(4,10),(5,6),(6,12),(7,13),(8,2),(8,7),(9,8),(9,15),(10,4),(10,9),(11,5),(11,10),(12,11),(12,17),(13,14),
                      (13,18),(14,8),(14,15),(15,16),(15,20),(16,11),(16,17),(17,22),(18,23),(19,14),(19,18),(20,19),(20,25),(21,16),(21,20),(22,21),(22,27),(23,24),
                      (24,19),(24,25),(25,26),(26,21),(26,27),(27,22)])
    print("Graph is created.")
    return g

def drawGraph(g, pos, colors):
    if pos:
        if len(colors) == 0:
            pos = nx.get_node_attributes(g, 'pos')
            nx.draw(g, pos, node_size=1500, width=2.0, with_labels=True)
        else:
            pos = nx.get_node_attributes(g, 'pos')
            nx.draw(g, pos, node_size=1500, edge_color=colors, width=2.0, with_labels=True)
    else:
        nx.draw(g, with_labels=True)
    
    plt.show()

#This function takes a digraph and converts it to line graph.
def convertToLineGraph(g):
    #Line Graph of g
    print("Graph is converting to line graph...")
    lg = nx.line_graph(g)
    print("Graph is converted to line graph.")
    return lg;

#This function generate a directed grap for turn constraints.
def generateTurnConstraints1(lg):
    print("Turn constraints are generating...")
    L = nx.DiGraph()
    for node in lg.nodes:
        L.add_node(node)
    L.add_edge((5,2),(2,1))
    print("Turn constraints are generated.")
    return L

#This function generate a directed grap for turn constraints.
def generateTurnConstraints2(lg):
    print("Turn constraints are generating...")
    L = nx.DiGraph()
    for node in lg.nodes:
        L.add_node(node)
    L.add_edge((8,5),(5,6))
    L.add_edge((11,12),(12,8))
    print("Turn constraints are generated.")
    return L

def deleteTurnConstraints(lg, L):
    for edge in L.edges:
        if lg.has_edge(edge[0], edge[1]):
            lg.remove_edge(edge[0], edge[1])
    return lg
    
#This function finds all cycles in a line graph. It takes an parameter which is line graph and it returns a hypergraph which includes all cycle in the line graph. 
def findCycles(lg):
    print("Cycles are finding...")
    #List for nodes
    N = []
    #List for cycles
    F = []
    #Size of F
    l = 0
    
    for node in lg.nodes:
        N.append(node)
        
    for node in N:
        #Stack for visited nodes
        P = []
        #List for edges
        Q = []
        #Top of stack
        t = 0
        P.append(node)
        t = t+1
        while True:
            #List for all possible neighbour of a node
            S = []
            #print("Node:")
            #print(node)
            #print("P[t]")
            #print(P[t-1])
            #print("P:")
            #print(P)
            #print("Q:")
            #print(Q)
            for adjacent in lg[P[t-1]]:
                if (positionOfNode(N, adjacent) < positionOfNode(N, node)) or (isVisited(P, adjacent)) or (isThereEdge(Q, P[t-1], adjacent)):
                    continue
                S.append(adjacent)
            if len(S) == 0:
                if P[t-1] == node:
                    #print("Bitti")
                    break
                if isThereEdge(lg.edges, P[t-1], node):
                    #print("Cycle Bulundu")
                    #print(len(P))
                    F.append(P[:])
                    #print("Cycle:")
                    #print(P)
                    #print("F:")
                    #print(F)
                    l = l+1
                P.pop()
                t = t-1
            else:
                #print("Komşulara Geçiliyor...")
                P.append(S.pop(0))
                t = t+1
                Q.append((P[t-2], P[t-1]))
                Q = deleteEdgeFromPath(Q, P[t-1])
    X = []
    for node in lg.nodes:
        X.append(node)
    C = (X, F)
    #print("F Sonuç:")
    #print(F)
    print("Cycles are found.")
    return C

#This function takes a hypergraph and converts it to simple hypergraph. 
def simplification(C):
    print("Simplification is started...")
    F = []
    Fnew = []
    deleted = []
    for item in C[1]:
        Fnew.append(item)
        F.append(item)
    for i in range(len(F)-1):
        j = i+1
        while j < len(F):
            if isSubset(F[i], F[j]):
                if isThere(deleted, j) == False:
                    deleted.append(j)
            elif isSubset(F[j], F[i]):
                if isThere(deleted, i) == False:
                    deleted.append(i)
            j = j+1
    deleted = selectionSort(deleted)
    for i in deleted:
        Fnew.pop(i)
    H = (C[0][:], Fnew)
    print("Simplification is completed.")
    return H

def selectionSort(array):
    for i in range(len(array)):
        max = i
        for j in range(i, len(array)):
            if array[j] > array[max]:
                max = j
        tmp = array[i]
        array[i] = array[max]
        array[max] = tmp
    return array


def isThere(a, b):
    result = False
    for item in a:
        if item == b:
            result = True
    return result
                
#Is there any edge from src to dest?
def isThereEdge(Q, src, dest):
    searchingEdge = (src, dest)
    for edge in Q:
        if edge == searchingEdge:
            return True
    return False

#Is there the argument node in P?
def isVisited(P, node):
    for n in P:
        if node == n:
            return True
    return False

#This function delete an edge from path.
def deleteEdgeFromPath(Q, node):
    i = 0;
    while i < len(Q):
        if Q[i][0] == node:
            Q.pop(i)
            i = i-1
        i = i+1
    return Q

#This function returns position of a node in list N.
def positionOfNode(N, node):
    i = 0
    for item in N:
        if item == node:
            return i
        i = i+1
    return -1

#This function eliminates cycles which less than 3.
def eliminateSmallCycles(C, length):
    print("Small cycles are eliminating...")
    F = []
    for item in C[1]:
        F.append(item)
    i = 0
    while i < len(F):
        if len(F[i]) <= length:
            F.pop(i)
            i = i-1
        i = i+1
    E = (C[0], F)
    print("Small cycles are eliminated.")
    return E

#This function returns true if A is a subset of B. If not it's returns false.
def isSubset(A, B):
    #print("isSubset() is started")
    result = True
    i = 0
    for item in A:
        if isThere(B, item) == False:
            result = False
            break
    #print("isSubset() is completed and result is:")
    #print(result)
    return result

def findTransversal(H):
    print("Transversals are finding...")
    n = []
    e = []
    for node in H[0]:
        n.append(node)
    for edge in H[1]:
        e.append(edge)
    S = []
    S.append((n,e))
    T = []
    i = 0
    while len(S[i][1]) > 0:
        t = None
        for node in S[i][0]:
            if nodeDegree(t, S[i]) < nodeDegree(node, S[i]):
                t = node
        T.append(t)
        S.append(cleanS(S[i], t))
        i = i+1
    print("Transversals are found.")
    return T
    
def nodeDegree(node, H):
    if node == None:
        return 0
    result = 0
    for edge in H[1]:
       for n in edge:
           if n == node:
               result = result+1
               break
    return result

def cleanS(S, t):
    n = []
    e = []
    i = 0
    for node in S[0]:
        if node == t:
            continue
        n.append(node)
    while i < len(S[1]):
        isThere = False
        for edge in S[1][i]:
            if edge == t:
                isThere = True
                break
        if isThere == False:
            e.append(S[1][i])
        i = i+1
    result = ((n,e))
    return result
        
def randomly(g, monitorCount):
    R = []
    edges = list(g.edges)
    if monitorCount >= len(edges):
        for edge in edges:
            R.append(edge)
        return R
    i = 0
    while i < monitorCount:
        rand = random.randint(0, len(edges)-1)
        if isThere(R, edges[rand]) == False:
            R.append(edges[rand])
            i = i+1
    return R

def experienceBased(g, monitorCount):
    E = []
    edges = list(g.edges)
    #print("Length of edges:")
    #print(len(edges))
    if monitorCount >= len(edges):
        for edge in edges:
            E.append(edge)
        return E
    ce = int(len(edges)/monitorCount)
    for i in range(monitorCount):
        if i == monitorCount-1:
            rand = random.randint(i*ce, len(edges)-1)
            E.append(edges[rand])
        else:
            rand = random.randint(i*ce, ((i+1)*ce)-1)
            E.append(edges[rand])
    return E


