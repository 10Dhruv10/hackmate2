from queue import Queue
from typing import List, Dict
import heapq

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.resources = []

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str, resource_id: int):
        node = self.root
        word = word.lower()
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            if resource_id not in node.resources:
                node.resources.append(resource_id)
        node.is_end = True
    
    def search_prefix(self, prefix: str) -> List[int]:
        node = self.root
        prefix = prefix.lower()
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return node.resources

class ResourceHeap:
    def __init__(self):
        self.heap = []
    
    def push(self, resource):
        heapq.heappush(self.heap, (-resource.upvotes, resource.id, resource))
    
    def get_top_k(self, k: int) -> List:
        temp_heap = self.heap.copy()
        result = []
        for _ in range(min(k, len(temp_heap))):
            if temp_heap:
                result.append(heapq.heappop(temp_heap)[2])
        return result