# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 17:33:46 2021

@author: coderzparadise
"""
import numpy as np

class AdjacencyList(object):
    def __init__(self, nodes):
        self.node = nodes
        self.item = []
        for i in range(len(self.node) ):
            self.item.append( [] )

    # overloading insert() and add() function for easy-use
    def insert(self, item1, item2):
        if item1 in self.node and item2 in self.node:
            index1 = self.node.index(item1)
            index2 = self.node.index(item2)
            self.item[index1].append(index2)
        else:
            index1 = item1
            index2 = item2
            self.item[index1].append(item2)
            
    # overloading add() and insert() function for easy-use  
    def add(self, item1, item2):
        if item1 in self.node and item2 in self.node:
            index1 = self.node.index(item1)
            index2 = self.node.index(item2)
            self.item[index1].append(index2)
        else:
            index1 = item1
            index2 = item2
            self.item[index1].append(item2)
            
    def display(self):
        print(self.item)
        
    def display_nodes(self):
        print(self.node)
            
    def in_degree(self):
        if self == None:
            return
        result = np.zeros(len(self.item), dtype=int)
        for bucket in range(len(self.item) ):
            for out_degree in range(len(self.item[bucket]) ):
                result[self.item[bucket][out_degree] ] += 1
        return result
    
    
    def adj_list_to_edge_list(self):
        e = []
        for bucket in range(len(self.item) ):
            for edge in range( len(self.item[bucket]) ):
                e.insert( bucket, self.item[bucket][edge] )
        return e
    
    
    def adj_list_to_adj_matrix(self):
        result = np.zeros((len(self.node), len(self.node)), dtype = bool)
        for bucket in range(len(self.item) ):
            for edge in range( len(self.item[bucket]) ):
                result[bucket][self.item[bucket][edge]] = True
        return result
    
    
    # #take in an adjceny list, starting point and visit complete
    def bfs(self, source, visit_complete):
        queue = [] # iniztilze queue
        visit_complete.append(source)
        queue.append(source)
        
        while(len(queue) != 0 ):
            current = queue.pop(0)
            print(current)
            
            for neighbour in self.item[current]:
                if neighbour not in visit_complete:
                    visit_complete.append(neighbour)
                    queue.append(neighbour)
                    #Here you can: prev[neighbour] = current : to state where you came from


    #  # take in an adjceny list, starting point and visit complete
    def dfs(self, source, visit_complete):
        stack = [] #initilize stack
        visit_complete.append(source)
        stack.append(source)
        
        while(len(stack) != 0 ):
            current = stack.pop()
            print(current)
            
            for neighbour in self.item[current]:
                if neighbour not in visit_complete:
                    visit_complete.append(neighbour)
                    stack.append(neighbour)
                    #Here you can: prev[neighbour] = current : to state where you came from 

    def topological(self):
        result = []
        queue = []
        indegree = self.in_degree()
        for i in range(len(indegree)):
            if indegree[i] == 0:
                queue.append(i)
        
        while len(queue) > 0:
            vertex = queue.pop(0)
            result.append(vertex)
            for u in self.item[vertex]:
                indegree[u] = indegree[u] - 1
                if indegree[u] == 0:
                    queue.append(u)
        
        if len(result) == len(self.item):
            return result
        else:
            return []



class AdjacencyMatrix(object):
    def __init__(self, nodes):
        self.node = nodes
        self.item = np.zeros((len(self.node), len(self.node)), dtype = bool)
        
    # overloading insert() and add() function for easy-use
    def insert(self, item1, item2):
        if item1 in self.node and item2 in self.node:
            index1 = self.node.index(item1)
            index2 = self.node.index(item2)
            self.item[index1][index2] = True
        else:
            index1 = item1
            index2 = item2
            self.item[index1][index2] = True

    # overloading add() and insert() function for easy-use  
    def add(self, item1, item2):
        if item1 in self.node and item2 in self.node:
            index1 = self.node.index(item1)
            index2 = self.node.index(item2)
            self.item[index1][index2] = True
        else:
            index1 = item1
            index2 = item2
            self.item[index1][index2] = True
            
    def display(self):
        print(self.item)
            
    def adj_matrix_to_adj_list(self):
        a = []
        for i in range(len(self.item)):
            a.append([])
            for j in range(len(self.item)):
                if self.item[i][j] == True:
                    a[i].append(j)
        return a
                
    def adj_matrix_to_edge_list(self):
        e = []
        for i in range(len(self.item)):
            for j in range(len(self.item)):
                if self.item[i][j] == True:
                    e.append([i, j, 0])
        return e


        
class EdgeList(object):
    def __init__(self, nodes):
        self.node = nodes
        self.item = []

    # overloading insert() and add() function for easy-use
    def insert(self, item1, item2):
        if item1 in self.node and item2 in self.node:
            index1 = self.node.index(item1)
            index2 = self.node.index(item2)
            #Append edge1, edge2, weight of edge
            self.item.append([index1, index2, 0])
        else:
            index1 = item1
            index2 = item2
            self.item.append([index1, index2, 0])

    # overloading add() and insert() function for easy-use  
    def add(self, item1, item2):
        if item1 in self.node and item2 in self.node:
            index1 = self.node.index(item1)
            index2 = self.node.index(item2)
            #Append edge1, edge2, weight of edge
            self.item.append([index1, index2, 0])
        else:
            index1 = item1
            index2 = item2
            self.item.append([index1, index2, 0])
        
    def display(self):
        print(self.item)
        
    def edge_list_to_adj_list(self):
        a = []
        for i in range(len(self.node) ):
            a.append([])
        for j in self.item:
            a[j[0]].append( j[1] )
        return a
    
    def edge_list_to_adj_matrix(self):
        result = np.zeros( (len(self.node), len(self.node)), dtype = bool)
        for i in self.item:
            result[i[0]][i[1]] = True
        return result