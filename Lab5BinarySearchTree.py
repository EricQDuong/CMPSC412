"""
CMPSC 412 - Lab 5: Binary Search Tree Basics
Covers Exercises 1-4.
"""


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    # ------------------------------------------------------------------
    # Exercise 1
    # ------------------------------------------------------------------
    def insert(self, key):
        """Insert key into the tree. Duplicates are ignored."""
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return Node(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        # key == node.key -> duplicate, do nothing
        return node

    def inorder(self):
        """Left, Root, Right -> gives keys in sorted order."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    def preorder(self):
        """Root, Left, Right."""
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node:
            result.append(node.key)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self):
        """Left, Right, Root."""
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.key)

    def find(self, key):
        """Return True if key is in the tree, else False."""
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def minimum(self):
        """Smallest key = leftmost node."""
        if self.root is None:
            return None
        node = self.root
        while node.left:
            node = node.left
        return node.key

    def maximum(self):
        """Largest key = rightmost node."""
        if self.root is None:
            return None
        node = self.root
        while node.right:
            node = node.right
        return node.key

    # ------------------------------------------------------------------
    # Exercise 2
    # ------------------------------------------------------------------
    def remove(self, key):
        """
        Remove key from the tree (no-op if not present).

        Time complexity: O(h), h = height of the tree.
          - Finding the node walks one root-to-node path: O(h).
          - Case 3 also walks down to the in-order successor and then
            deletes it, which continues along the same downward path: O(h).
          Balanced tree: h = log n  ->  O(log n)
          Worst case (skewed tree, e.g. sorted inserts): h = n -> O(n)
        """
        self.root = self._remove(self.root, key)

    def _remove(self, node, key):
        if node is None:
            return None  # key not found
        if key < node.key:
            node.left = self._remove(node.left, key)
        elif key > node.key:
            node.right = self._remove(node.right, key)
        else:
            # Case 1: leaf node -> just remove it
            if node.left is None and node.right is None:
                return None
            # Case 2: one child -> replace node with its child
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Case 3: two children -> copy in-order successor
            # (smallest key in right subtree), then delete that successor
            succ = node.right
            while succ.left:
                succ = succ.left
            node.key = succ.key
            node.right = self._remove(node.right, succ.key)
        return node

    # ------------------------------------------------------------------
    # Exercise 4 (part 2)
    # ------------------------------------------------------------------
    def is_valid_bst(self):
        return is_valid_bst(self.root)


# ----------------------------------------------------------------------
# Exercise 3: merge two trees
# ----------------------------------------------------------------------
def insert_node(tree, new_node):
    """Attach an existing Node object (not a copy of its value) into tree.
    Returns True if attached, False if its key was already in the tree."""
    new_node.left = new_node.right = None   # detach from its old tree
    if tree.root is None:
        tree.root = new_node
        return True
    cur = tree.root
    while True:
        if new_node.key < cur.key:
            if cur.left is None:
                cur.left = new_node
                return True
            cur = cur.left
        elif new_node.key > cur.key:
            if cur.right is None:
                cur.right = new_node
                return True
            cur = cur.right
        else:
            return False  # duplicate key: node is dropped


def merge_trees(t1, t2):
    """
    Merge t2 into t1 by moving t2's actual Node objects into t1.
    No new nodes are created; each node of t2 is relinked into t1.

    How: walk t2 in POST-order (left, right, root). A node's children are
    always moved before the node itself, so when we reset the node's
    left/right pointers we are not losing any part of t2 that still has
    to be visited.

    Time complexity: O(n * h)
      - n = number of nodes in t2; each one is inserted once.
      - each insert walks one path in t1, costing O(h), where h is the
        height of the growing tree (at most m + n).
      Average (fairly balanced tree): O(n log(m + n))
      Worst case (skewed tree):       O(n * (m + n))
    Extra space: O(height of t2) for the recursion stack.
    """
    def move(node):
        if node is None:
            return
        left, right = node.left, node.right   # save before detaching
        move(left)
        move(right)
        insert_node(t1, node)

    move(t2.root)
    t2.root = None   # t2's nodes now belong to t1
    return t1


# ----------------------------------------------------------------------
# Exercise 4
# ----------------------------------------------------------------------
def build_bst_from_list(values):
    """Build a BST by inserting each element of the list in order.
    O(n * h): O(n log n) on average, O(n^2) if the list is sorted."""
    tree = BinarySearchTree()
    for v in values:
        tree.insert(v)
    return tree


def is_valid_bst(node, low=float("-inf"), high=float("inf")):
    """
    Every node must lie strictly between the bounds inherited from its
    ancestors. Checking only node.left < node < node.right is NOT enough:
    a deep descendant could still be on the wrong side of an ancestor.
    Time O(n) - each node visited once.
    """
    if node is None:
        return True
    if not (low < node.key < high):
        return False
    return (is_valid_bst(node.left, low, node.key) and
            is_valid_bst(node.right, node.key, high))


# ----------------------------------------------------------------------
# Demo
# ----------------------------------------------------------------------
def _all_nodes(node):
    if node is None:
        return []
    return _all_nodes(node.left) + [node] + _all_nodes(node.right)


def show(tree, label):
    print(f"{label}")
    print("  In-order  :", tree.inorder())
    print("  Pre-order :", tree.preorder())
    print("  Post-order:", tree.postorder())


if __name__ == "__main__":
    print("=" * 60)
    print("EXERCISE 1: insert, traversals, find, min, max")
    print("=" * 60)
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 65, 90]
    bst = BinarySearchTree()
    for v in values:
        bst.insert(v)
    print("Inserted:", values)
    show(bst, "Tree:")
    print("  find(35):", bst.find(35))
    print("  find(99):", bst.find(99))
    print("  Minimum :", bst.minimum())
    print("  Maximum :", bst.maximum())

    print()
    print("=" * 60)
    print("EXERCISE 2: remove (all three cases)")
    print("=" * 60)
    bst.remove(10)   # leaf
    print("Case 1 - remove leaf 10           :", bst.inorder())
    bst.remove(60)   # one child (65)
    print("Case 2 - remove 60 (one child)    :", bst.inorder())
    bst.remove(30)   # two children (20, 40)
    print("Case 3 - remove 30 (two children) :", bst.inorder())
    print("  Pre-order after removals:", bst.preorder())
    print("  (35, the in-order successor, replaced 30)")

    print()
    print("=" * 60)
    print("EXERCISE 3: merge two trees")
    print("=" * 60)
    t1 = build_bst_from_list([15, 5, 25, 3, 8, 20, 30, 1, 4, 9])
    t2 = build_bst_from_list([12, 6, 18, 2, 7, 16, 22, 11, 14, 25])
    show(t1, "Tree 1:")
    show(t2, "Tree 2:")
    t2_node_ids = {id(n) for n in _all_nodes(t2.root)}
    merged = merge_trees(t1, t2)
    show(merged, "Merged tree (tree 2's nodes moved into tree 1):")
    print("  Merged is valid BST:", merged.is_valid_bst())
    reused = sum(1 for n in _all_nodes(merged.root) if id(n) in t2_node_ids)
    print(f"  Node objects reused from tree 2: {reused} "
          f"(25 was a duplicate, so it was dropped)")
    print("  Tree 2 is now empty:", t2.inorder())

    print()
    print("=" * 60)
    print("EXERCISE 4: build from list + validate")
    print("=" * 60)
    data = [45, 22, 67, 11, 33, 56, 78, 5, 17, 29, 39, 88]
    built = build_bst_from_list(data)
    print("List:", data)
    show(built, "Built tree:")
    print("  Valid BST?", built.is_valid_bst())

    # Hand-built tree that is NOT a BST: 60 sits in 50's LEFT subtree.
    #        50
    #       /  \
    #     30    70
    #    /  \
    #   20   60   <- 60 > 50, invalid even though 60 > 30 locally
    bad = BinarySearchTree()
    bad.root = Node(50)
    bad.root.left = Node(30)
    bad.root.right = Node(70)
    bad.root.left.left = Node(20)
    bad.root.left.right = Node(60)
    print("Hand-built tree with 60 in 50's left subtree")
    print("  In-order:", bad.inorder(), "(not sorted)")
    print("  Valid BST?", bad.is_valid_bst())