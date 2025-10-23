class MinHeapNode:
    def __init__(self, key, payload, idx):
        self.key = key
        self.payload = payload
        self.idx = idx
    def __lt__(self, other):
        return self.key < other.key
    def __le__(self, other):
        return self.key <= other.key
    def __eq__(self, other):
        return self.key == other.key
    def __gt__(self, other):
        return self.key > other.key
    def __ge__(self, other):
        return self.key >= other.key
    def __ne__(self, other):
        return self.key != other.key

class MinHeap:
    def __init__(self):
        self.nodes = []

    def get_min(self):
        if len(self.nodes) == 0:
            return MinHeapNode((1e32,1e32), None, -1)
        return self.nodes[0]

    def pop_min(self):
        if len(self.nodes) == 0:
            return MinHeapNode((1e32,1e32), None, -1)
        elif len(self.nodes) == 1:
            m = self.nodes[0]
            self.nodes = []
            return m
        else:
            m = self.nodes[0]
            e = self.nodes[-1]
            self.nodes = self.nodes[:-1]
            e.idx = 0
            self.nodes[0] = e
            # perculate down
            self._bubble_down(0)
            return m

    def insert(self, key, payload):
        new_node = MinHeapNode(key, payload, len(self.nodes))
        self.nodes.append(new_node)
        self._bubble_up(len(self.nodes) - 1)
        return new_node
    
    def arbitrary_delete(self, index):
        if index >= len(self.nodes) or index < 0:
            return -1
        elif index == len(self.nodes) - 1:
            self.nodes = self.nodes[:-1]
            return
        elif index == 0:
            self.pop_min()
            return
        else:
            e = self.nodes[-1]
            e.idx = index
            self.nodes = self.nodes[:-1]
            self.nodes[index] = e
            if self.nodes[(index-1)//2] > self.nodes[index]:
                self._bubble_up(index)
                return
            else:
                self._bubble_down(index)
                return

    def pop_range(self, lteq):
         # lteq must be the same data structure as a key.
        results = []
        while len(self.nodes) != 0 and lteq >= self.nodes[0].key:
            results.append(self.pop_min())
        return results

    def change_key(self, index, new_key):
        if index >= len(self.nodes) or index < 0:
            return -1
        old_key = self.nodes[index].key
        self.nodes[index].key = new_key
        if new_key < old_key:
            self._bubble_up(index)
        else:
            self._bubble_down(index)

    def _bubble_down(self, index):
            p = index # parent
            l = 2*p + 1 # left
            r = 2*p + 2 # right
            while r < len(self.nodes) and self.nodes[p] > min(self.nodes[l], self.nodes[r]):
                t = self.nodes[p]
                if self.nodes[l] > self.nodes[r]:
                    self.nodes[p] = self.nodes[r]
                    self.nodes[r] = t
                    self.nodes[r].idx = r
                    p = r
                else:
                    self.nodes[p] = self.nodes[l]
                    self.nodes[l] = t
                    self.nodes[l].idx = l
                    p = l
                self.nodes[p].idx = p
                l = 2*p + 1
                r = 2*p + 2
            # accounting for odd case where there is not a left and right
            if len(self.nodes) % 2 == 0 and self.nodes[-1] < self.nodes[(len(self.nodes) - 2) // 2]:
                # swap values
                t = self.nodes[-1]
                self.nodes[-1] = self.nodes[(len(self.nodes) - 2) // 2]
                self.nodes[-1].idx = len(self.nodes) - 1
                self.nodes[(len(self.nodes) - 2) // 2] = t
                self.nodes[(len(self.nodes) - 2) // 2].idx = (len(self.nodes) - 2) // 2

    def _bubble_up(self, index):
        i = index
        p = (i - 1) // 2
        while i > 0 and self.nodes[p] > self.nodes[i]:
            t = self.nodes[p]
            self.nodes[p] = self.nodes[i]
            self.nodes[p].idx = p
            self.nodes[i] = t
            self.nodes[i].idx = i
            i = p
            p = (i - 1) // 2