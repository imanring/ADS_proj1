class PairingHeap:
    def __init__(self, key, payload):
        self.key = key
        self.payload = payload
        self.child = None
        self.left = None
        self.right = None
    
    def meld(self, other):
        """
        Meld other and self. You should only meld 2 roots.
        Parameters:
            other(PairingHeap): PairingHeap to be melded with self
        Return:
            (PairingHeap): resultant pairing heap
        """
        if self.key >= other.key:
            # set other as left child of self
            if self.child is not None:
                self.child.left = other
            other.right = self.child
            self.child = other
            # left of the left-most sibling is the parent
            other.left = self
            return self
        else:
            # set self as left child of other
            if other.child is not None:
                other.child.left = self
            self.right = other.child
            other.child = self
            self.left = other
            return other

    def insert(self, key, payload):
        # probably will not be used if you want to 
        new_tree = PairingHeap(key, payload)
        return self.meld(new_tree)

    def increase_key(self, n, i):
        n.key += i
        # remove from sibling linked list
        if n.right is not None:
            n.right.left = n.left
        if n.left is not None:
            if n.left.child == n:
                n.left.child = n.right
            else:
                n.left.right = n.right
        # meld self with the node with increased key
        return self.meld(n)

    def pop_max(self):
        
        result = (self.key, self.payload)

        # first pass
        children = [self.child]
        while children[-1] is not None:
            if children[-1].right is not None:
                s = children[-1].right
                t = children[-1].right.right
                s.right = None
                s.left = None
                children[-1].right = None
                children[-1].left = None
                children[-1] = children[-1].meld(s)
                children.append(t)
            else:
                children.append(None)
                break
        # remove None from end of list
        children = children[:-1]

        # second pass
        while len(children) > 1:
            children = children[:-2] + [children[-1].meld(children[-2])]
        # If the node is the last in the PairingHeap, then children will have length 0
        # return None as the new PairingHeap
        children.append(None)
        return result, children[0]

    def arbitrary_delete(self, tree):
        # arbitrary remove
        if tree == self: # removing root
            return self.pop_max()
        
        # remove from double linked list
        if tree.left is not None:
            # if left most child
            if tree.left.child == tree:
                tree.left.child = tree.right
            else:
                tree.left.right = tree.right
        if tree.right is not None:
            tree.right.left = tree.left
        
        if tree.child is not None:
            r, m = tree.pop_max()
            return self.meld(m)
        else:
            return self
            
    def dfs(self):
        # print key in depth first manner
        if self.child is not None:
            self.child.dfs()
        print(self.key)
        if self.right is not None:
            self.right.dfs()

    def __str__(self):
        return f"{self.key}"
