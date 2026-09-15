import array

class Vector:
    def __init__(self):
        self._capacity = 2
        self._count = 0
        self._array = array.array('i', [0] * self._capacity)

    def __len__(self):
        return self._count

    def __getitem__(self, index):
        if not (0 <= index < self._count):
            raise IndexError("Vector index out of range")
        return self._array[index]

    def __setitem__(self, index, value):
        if not (0 <= index < self._count):
            raise IndexError("Vector index out of range")
        self._array[index] = value

    def __contains__(self, value):
        for i in range(self._count):
            if self[i] == value:
                return True
        return False

    # --- Internal helper: grows the array when full ---
    # Doubling capacity keeps append O(1) amortized: copying n items
    # happens rarely (only on powers-of-two boundaries), so the average
    # cost per append stays constant even though any single doubling is O(n).
    def _resize(self, new_capacity):
        new_array = array.array('i', [0] * new_capacity)
        for i in range(self._count):
            new_array[i] = self._array[i]
        self._array = new_array
        self._capacity = new_capacity

    # --- append: add item to the end ---
    # Grow first if full, then write to the next free slot.
    def append(self, item):
        if self._count == self._capacity:
            self._resize(2 * self._capacity)
        self._array[self._count] = item
        self._count += 1

    # --- insert: add item at position ndx, shifting later items right ---
    # Bounds: 0 <= ndx <= count (count itself means "insert at the end").
    # Must grow BEFORE shifting, so there's a free slot to shift into.
    # Shift right-to-left (from the last item backward) so you don't
    # overwrite a value before you've copied it.
    def insert(self, ndx, item):
        if not (0 <= ndx <= self._count):
            raise IndexError("Vector index out of range")
        if self._count == self._capacity:
            self._resize(2 * self._capacity)
        for i in range(self._count, ndx, -1):
            self._array[i] = self._array[i - 1]
        self._array[ndx] = item
        self._count += 1

    # --- remove: delete item at position ndx, shifting later items left ---
    # Bounds: 0 <= ndx < count (this time count itself is NOT valid --
    # there's no item there to remove).
    # Shift left-to-right this time, since you're pulling values toward
    # a lower index and each source slot is read before being overwritten.
    def remove(self, ndx):
        if not (0 <= ndx < self._count):
            raise IndexError("Vector index out of range")
        item = self._array[ndx]
        for i in range(ndx, self._count - 1):
            self._array[i] = self._array[i + 1]
        self._count -= 1
        self._array[self._count] = 0  # clear the now-unused last slot
        return item

    # --- index: linear search, like list.index() ---
    # Returns the first matching position, or -1 if not found
    # (check your spec: some versions want a raised exception instead).
    def index(self, item):
        for i in range(self._count):
            if self._array[i] == item:
                return i
        return -1

    # --- extend: append every item from another iterable/Vector ---
    # Deliberately reuses append() instead of duplicating growth logic.
    def extend(self, other):
        for item in other:
            self.append(item)

    # --- subVector: build a brand-new Vector from a range of this one ---
    def subVector(self, start, stop):
        result = Vector()
        for i in range(start, stop):
            result.append(self._array[i])
        return result

    # --- iteration support, so `for x in vector` and extend() work ---
    def __iter__(self):
        for i in range(self._count):
            yield self._array[i]

    def __str__(self):
        return "[" + ", ".join(str(self._array[i]) for i in range(self._count)) + "]"


def demo():
    """Simple demonstration / sanity check of each operation, printed to console."""
    v = Vector()
    print("Initial vector:", v, "| capacity:", v._capacity)

    for i in range(1, 6):
        v.append(i)
    print("After append 1..5:", v, "| capacity:", v._capacity)

    v.insert(2, 99)
    print("After insert(2, 99):", v)

    removed = v.remove(0)
    print(f"After remove(0) [removed {removed}]:", v)

    print("index(99):", v.index(99))
    print("index(1000):", v.index(1000))
    print("42 in v:", 42 in v)

    v2 = Vector()
    v2.extend([100, 200, 300])
    print("v2 after extend([100,200,300]):", v2)

    v3 = v.subVector(1, 3)
    print("subVector(1,3) of v:", v3)

if __name__ == "__main__":
    demo()
