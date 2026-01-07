import unittest
import heapq

class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_i] = root_j
                self.rank[root_j] += 1
            return True
        return False

def kruskal(n, edges):
    ds = DisjointSet(n)
    mst = []
    mst_weight = 0
    # Sort edges by weight
    edges.sort(key=lambda x: x[2])
    
    for u, v, w in edges:
        if ds.union(u, v):
            mst.append((u, v, w))
            mst_weight += w
    return mst, mst_weight

def prim(n, adj):
    mst = []
    mst_weight = 0
    visited = [False] * n
    pq = [(0, 0, -1)]  # (weight, current_node, parent_node)
    
    while pq and len(mst) < n:
        weight, u, p = heapq.heappop(pq)
        if visited[u]:
            continue
        
        visited[u] = True
        mst_weight += weight
        if p != -1:
            mst.append((p, u, weight))
        
        if u in adj:
            for v, w in adj[u]:
                if not visited[v]:
                    heapq.heappush(pq, (w, v, u))
            
    return mst, mst_weight

class TestMST(unittest.TestCase):
    def setUp(self):
        # Sample graph from Appendix C
        self.n = 5
        self.edges = [
            (0, 1, 1), (1, 2, 2), (2, 3, 3), 
            (0, 3, 4), (3, 4, 5), (1, 4, 6), (0, 2, 7)
        ]
        self.adj = {
            0: [(1, 1), (3, 4), (2, 7)],
            1: [(0, 1), (2, 2), (4, 6)],
            2: [(1, 2), (3, 3), (0, 7)],
            3: [(2, 3), (0, 4), (4, 5)],
            4: [(3, 5), (1, 6)]
        }

    def test_kruskal(self):
        mst, weight = kruskal(self.n, self.edges)
        self.assertEqual(weight, 11)
        self.assertEqual(len(mst), 4)

    def test_prim(self):
        mst, weight = prim(self.n, self.adj)
        self.assertEqual(weight, 11)
        self.assertEqual(len(mst), 4)

    def test_empty_graph(self):
        mst, weight = kruskal(0, [])
        self.assertEqual(weight, 0)
        self.assertEqual(len(mst), 0)
        
        mst, weight = prim(0, {})
        self.assertEqual(weight, 0)
        self.assertEqual(len(mst), 0)

if __name__ == '__main__':
    unittest.main()
