class MinHeap:
    def __init__(self):
        self.nodes = []

    def get_min(self):
        if len(self.nodes) == 0:
            return -1
        return self.nodes[0]

    def pop_min(self):
        if len(self.nodes) == 0:
            return -1
        elif len(self.nodes) == 1:
            m = self.nodes[0]
            self.nodes = []
            return m
        else:
            m = self.nodes[0]
            l = self.nodes[-1]
            self.nodes = self.nodes[:-1]
            self.nodes[0] = l
            # perculate down
            p = 0
            l = 2*p + 1
            r = 2*p + 2
            while r < len(self.nodes) and self.nodes[p] > min(self.nodes[l], self.nodes[r]):
                if self.nodes[l] > self.nodes[r]:
                    t = self.nodes[p]
                    self.nodes[p] = self.nodes[r]
                    self.nodes[r] = t
                    p = r
                else:
                    t = self.nodes[p]
                    self.nodes[p] = self.nodes[l]
                    self.nodes[l] = t
                    p = l
                l = 2*p + 1
                r = 2*p + 2
            # accounting for odd case where there is not a left and right
            if len(self.nodes) % 2 == 0 and self.nodes[-1] < self.nodes[(len(self.nodes) - 2) // 2]:
                # swap values
                t = self.nodes[-1]
                self.nodes[-1] = self.nodes[(len(self.nodes) - 2) // 2]
                self.nodes[(len(self.nodes) - 2) // 2] = t
            return m

    def insert(self, x):
        self.nodes.append(x)
        i = len(self.nodes)-1
        p = (i - 1) // 2
        while i > 0 and self.nodes[p] > self.nodes[i]:
            t = self.nodes[p]
            self.nodes[p] = self.nodes[i]
            self.nodes[i] = t
            i = p
            p = (i - 1) // 2
