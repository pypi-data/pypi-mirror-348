# -*- coding: utf-8 -*-

from .binarysearchtree import BST as _BST
from .disjointforrestset import DSF as _DSF
from .graph import AdjacencyList as _AdjacencyList, AdjacencyMatrix as _AdjacencyMatrix, EdgeList as _EdgeList
from .hashmap import HashMap as _HashMap
from .heap import Heap as _Heap
from .linked_list import LinkedList as _LinkedList
from .queue import Queue as _Queue, Node as _Node
from .stack import Stack as _Stack, Node as _Node
from .trie import Trie as _Trie

class DataStructure:
    AdjacencyList = _AdjacencyList
    AdjacencyMatrix = _AdjacencyMatrix
    BST = _BST
    DSF = _DSF
    EdgeList = _EdgeList
    Hashmap = _HashMap
    LinkedList = _LinkedList
    Queue = _Queue
    Stack = _Stack
    Trie = _Trie