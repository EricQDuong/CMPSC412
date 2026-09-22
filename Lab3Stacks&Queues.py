"""CMPSC 462 - Lab 3: Stack and Queue"""
from collections import deque

# ---------------------------------------------------------------
# Basic Stack and Queue classes (stand-ins for the ones from class)
# ---------------------------------------------------------------
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __str__(self):
        return "Stack(bottom->top): " + str(self._items)


class Queue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def front(self):
        if self.is_empty():
            raise IndexError("front of empty queue")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __str__(self):
        return "Queue(front->back): " + str(list(self._items))


# ---------------------------------------------------------------
# Exercise 1: Queue using two stacks
# ---------------------------------------------------------------
class QueueTwoStacks:
    """enqueue -> push on in_stack.
       dequeue -> if out_stack is empty, pour everything from in_stack
                  into out_stack (reverses order), then pop from out_stack."""

    def __init__(self):
        self.in_stack = Stack()
        self.out_stack = Stack()

    def enqueue(self, item):
        self.in_stack.push(item)

    def _shift(self):
        if self.out_stack.is_empty():
            while not self.in_stack.is_empty():
                self.out_stack.push(self.in_stack.pop())

    def dequeue(self):
        self._shift()
        if self.out_stack.is_empty():
            raise IndexError("dequeue from empty queue")
        return self.out_stack.pop()

    def is_empty(self):
        return self.in_stack.is_empty() and self.out_stack.is_empty()

    def size(self):
        return self.in_stack.size() + self.out_stack.size()


def show_state(q):
    print(f"  Stack1 (in):  {q.in_stack._items}")
    print(f"  Stack2 (out): {q.out_stack._items}")
    print()


def test_exercise_1():
    q = QueueTwoStacks()

    for x in [10, 20, 30]:
        q.enqueue(x)
        print(f"enqueue({x})")
        show_state(q)

    val = q.dequeue()
    print(f"dequeue() -> {val}")
    show_state(q)

    val = q.dequeue()
    print(f"dequeue() -> {val}")
    show_state(q)

    q.enqueue(40)
    print("enqueue(40)")
    show_state(q)

    val = q.dequeue()
    print(f"dequeue() -> {val}")
    show_state(q)

    val = q.dequeue()
    print(f"dequeue() -> {val}")
    show_state(q)


# ---------------------------------------------------------------
# Exercise 2: Merge two sorted queues into a third sorted queue
# ---------------------------------------------------------------
def merge_queues(q1, q2):
    q3 = Queue()
    while not q1.is_empty() and not q2.is_empty():
        if q1.front() <= q2.front():
            q3.enqueue(q1.dequeue())
        else:
            q3.enqueue(q2.dequeue())
    # one queue is empty; drain whatever is left in the other
    while not q1.is_empty():
        q3.enqueue(q1.dequeue())
    while not q2.is_empty():
        q3.enqueue(q2.dequeue())
    return q3


def make_queue(items):
    q = Queue()
    for s in items:
        q.enqueue(s)
    return q


def test_exercise_2():
    print("=== Exercise 2: Merge two sorted queues ===")
    tests = [
        (["apple", "cherry", "grape"], ["banana", "date", "kiwi", "mango"]),
        (["ant", "bee"], []),
        (["cat", "dog"], ["elk", "fox"]),
    ]
    for a, b in tests:
        q1, q2 = make_queue(a), make_queue(b)
        print("Queue 1:", q1)
        print("Queue 2:", q2)
        q3 = merge_queues(q1, q2)
        print("Queue 3:", q3)
        print()


# ---------------------------------------------------------------
# Exercise 3: Balanced brackets
# ---------------------------------------------------------------
def check_balanced(text):
    """Returns (is_balanced, message). Characters other than brackets
    (such as the commas in the test cases) are ignored."""
    pairs = {")": "(", "]": "[", "}": "{"}
    openers = set(pairs.values())
    stack = Stack()                       # holds (char, index)

    for i, ch in enumerate(text):
        if ch in openers:
            stack.push((ch, i))
        elif ch in pairs:
            if stack.is_empty():
                return False, f"extra closing '{ch}' at index {i} (nothing to match)"
            top, j = stack.pop()
            if top != pairs[ch]:
                return False, (f"'{ch}' at index {i} does not match "
                               f"'{top}' opened at index {j}")

    if not stack.is_empty():
        top, j = stack.pop()
        return False, f"'{top}' opened at index {j} is never closed"
    return True, "all brackets matched"


def test_exercise_3():
    print("=== Exercise 3: Balanced brackets ===")
    cases = ["{,[,],}", "{,(,},)", "(,{,),},)"]
    for c in cases:
        ok, msg = check_balanced(c)
        print(f'Input: "{c}"')
        print("  Balanced:", ok, "-", msg)
    print()


if __name__ == "__main__":
    test_exercise_1()
    test_exercise_2()
    test_exercise_3()