# @CoderzParadise

## Data Structure library made easy

Welcome to coding in paradise. @CoderzParadise is a package made from scratch in Python by CoderzParadise that makes using Data Structures as easy as possible for humans and AI. Download and get started in under 4 minutes. Supported by ACM (Association of Computing Machinery). 

## Installation (How To Get Started)

1. Install **pip** package in your terminal (command prompt)
```
pip install coderzparadise
```
2. Use the examples below in your code :)

3. Done!

## Data Structure's
Organized way to store and manage data.

Index | Data Structure | Class Name
--- | --- | ---
**0** | Binary Search Tree | BST()
**1** | Disjoint Forrest Set | DSF(int::size)
**2** | Graph - Adjacency List | AdjacencyList(list::nodes)
**3** | Graph - Adjacency Matrix | AdjacencyList(list::nodes)
**4** | Graph - Edge List | EdgeList(list::nodes)
**5** | HashMap | HashMap(int::size)
**6** | Heap | Heap()
**7** | LinkedList | LinkedList()
**8** | Queue | Queue()
**9** | Set | Set()
**10** | Stack | Stack()
**11** | Trie() | Trie()
---


### Binary Search Tree
```
from coderzparadise import DataStructure

b = DataStructure.BST()

b.insert(50)
b.insert(75)
b.insert(25)
b.insert(100)
b.insert(95)

b.display()
```

### DisjointForrestSet
```
from coderzparadise import DataStructure

d = DataStructure.DSF(10) #parameter: (integer) 10 is setting size of disjointforrestset.

d.insert(0, 1)
d.insert(0, 3)
d.insert(0, 5)
d.insert(0, 7)
d.insert(0, 9)
d.insert(2, 4)
d.insert(2, 6)

number_of_sets_found = d.num_of_sets()
print('dsf num of sets: ', number_of_sets_found,\n)

d.display()
```

### Graph - Adjacency List
```
from coderzparadise import DataStructure

a = DataStructure.AdjacencyList([0,1,2,3,4,5,6,7,8,9]) #parameter: list is nodes that make up the graph.

a.insert(9, 1)
a.insert(9, 2)
a.insert(9, 3)
a.insert(9, 4)
a.insert(0, 5)
a.insert(0, 3)

a.display()
```

### Graph - Adjacency Matrix
```
from coderzparadise import DataStructure

a = DataStructure.AdjacencyMatrix([0,1,2,3,4,5,6,7,8,9]) #parameter: list is nodes that make up the graph.

a.insert(9, 1)
a.insert(9, 2)
a.insert(9, 3)
a.insert(9, 4)
a.insert(0, 5)
a.insert(0, 3)

a.display()
```

### Graph - EdgeList
```
from coderzparadise import DataStructure

e = DataStructure.AdjacencyMatrix([0,1,2,3,4,5,6,7,8,9]) #paramter: list is nodes that make up the graph.

e.insert(9, 1)
e.insert(9, 2)
e.insert(9, 3)
e.insert(9, 4)
e.insert(0, 5)
e.insert(0, 3)

e.display()
```

### Hash Map
```
from coderzparadise import DataStructure

h = HashMap(2) #parameter: (integer) 2 is setting up the inital size of hashmap.

h.insert('soccer')
h.insert('soccer')
h.insert('basketball')
h.insert('pizza')
h.insert('hamburger')

h.display()
```

### Heap
```
from coderzparadise import DataStructure

h = Heap()

h.insert(16)
h.insert(16)
h.insert(37)
h.insert(28)
h.insert(49)
h.insert(21)
h.insert(5)

h.display()
```


### Linked List
```
from coderzparadise import DataStructure

ll = DataStructure.LinkedList()

ll.insert(75)
ll.insert(75)
ll.insert(80)
ll.insert(81)
ll.insert(99)
ll.insert(2)
ll.insert(77)

ll.display()
```

### Queue
```
from coderzparadise import DataStructure

q = DataStructure.Queue()

q.insert(10)
q.insert(10)
q.insert(20)
q.insert(30)
q.insert(40)
q.insert(50)

q.display()
```

### Set
```
from coderzparadise import DataStructure

ll = DataStructure.Set()

s.insert(10)
s.insert(10)
s.insert(20)
s.insert(50)
s.insert(50)
s.insert(50)
s.insert(50)
s.insert(30)

s.display()
```

### Stack
```
from coderzparadise import DataStructure

s = DataStructure.Stack()

s.insert(10)
s.insert(10)
s.insert(20)
s.insert(30)
s.insert(40)
s.insert(50)

s.display()
```


### Trie
```
from coderzparadise import DataStructure

t = DataStructure.Trie()
t.insert("socks")
t.insert("soccer")
t.insert("colors")
t.search_word("sock")
t.search_word("socks")
t.is_prefix("b")
t.is_prefix("s")
```
---
---
---
## GitHub Repo:
[Coderz Paradise](https://github.com/coderzparadise/coderzparadise/tree/main/src/coderzparadise)

## Youtube Channel:
[Coderz Paradise](https://www.youtube.com/@CoderzParadise)

## Soundcloud:
(Coderz Paradise Music coming soon!)