"""
CMPSC 412 - Lab 6: Binary Search Tree of Students
(continuation of Lab 4 - student records, and Lab 5 - BST basics)

The student data from Lab 4 (students.txt) is loaded into a BST.
Each node stores one student:
    key     -> Student_ID (PSU ID), which must be unique
    details -> dictionary with first_name, last_name, email_id, major, GPA

Operations:
  1. Insert a new student with a unique PSU ID
  2. Find a student by PSU ID
  3. Print every student with all details (in-order traversal = sorted by ID)
"""

import os

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.txt")


class Node:
    """One BST node: the PSU ID (key) plus a dictionary of student details."""

    def __init__(self, student_id, details):
        self.student_id = student_id   # key used to order the tree
        self.details = details         # {"first_name": ..., "last_name": ..., ...}
        self.left = None               # subtree with smaller IDs
        self.right = None              # subtree with larger IDs


class StudentBST:
    def __init__(self):
        self.root = None
        self.size = 0

    # ---------- Insert ----------
    def insert(self, student_id, details):
        """Insert a student. Returns True on success, False if the ID already exists."""
        if self.root is None:
            self.root = Node(student_id, details)
            self.size += 1
            return True
        inserted = self._insert(self.root, student_id, details)
        if inserted:
            self.size += 1
        return inserted

    def _insert(self, node, student_id, details):
        if student_id == node.student_id:
            return False                                   # duplicate ID -> reject
        if student_id < node.student_id:
            if node.left is None:
                node.left = Node(student_id, details)
                return True
            return self._insert(node.left, student_id, details)
        else:
            if node.right is None:
                node.right = Node(student_id, details)
                return True
            return self._insert(node.right, student_id, details)

    # ---------- Find ----------
    def find(self, student_id):
        """Return the node with this PSU ID, or None if it is not in the tree."""
        return self._find(self.root, student_id)

    def _find(self, node, student_id):
        if node is None or node.student_id == student_id:
            return node
        if student_id < node.student_id:
            return self._find(node.left, student_id)
        return self._find(node.right, student_id)

    # ---------- Print all ----------
    def print_all(self):
        """Print every student in ascending PSU ID order (in-order traversal)."""
        if self.root is None:
            print("No students in the tree.")
            return
        print_header()
        self._inorder(self.root)
        print(f"\nTotal students: {self.size}")

    def _inorder(self, node):
        if node is not None:
            self._inorder(node.left)       # smaller IDs first
            print_student(node)            # then this student
            self._inorder(node.right)      # then larger IDs


# ---------- Display helpers ----------
def print_header():
    print(f"\n{'Student_ID':<12}{'First':<12}{'Last':<12}{'Email':<28}{'Major':<10}{'GPA'}")
    print("-" * 78)


def print_student(node):
    d = node.details
    print(f"{node.student_id:<12}{d['first_name']:<12}{d['last_name']:<12}"
          f"{d['email_id']:<28}{d['major']:<10}{d['GPA']}")


# ---------- Load / save the Lab 4 text file ----------
def load_students(bst, filename=DATA_FILE):
    """Read students.txt (header line + one student per line) into the BST."""
    with open(filename) as f:
        next(f)                                    # skip the header row
        for line in f:
            parts = line.split()
            if len(parts) != 6:
                continue                           # skip blank or malformed lines
            student_id, first, last, email, major, gpa = parts
            details = {"first_name": first, "last_name": last,
                       "email_id": email, "major": major, "GPA": float(gpa)}
            if not bst.insert(int(student_id), details):
                print(f"  Skipped duplicate Student_ID {student_id} in file.")


def append_student_to_file(student_id, d, filename=DATA_FILE):
    """Keep the text file in sync when a new student is inserted."""
    with open(filename, "a") as f:
        f.write(f"{student_id} {d['first_name']} {d['last_name']} "
                f"{d['email_id']} {d['major']} {d['GPA']}\n")


# ---------- Interactive menu ----------
def read_student_id():
    while True:
        value = input("Enter Student_ID (9 digits): ").strip()
        if value.isdigit() and len(value) == 9:
            return int(value)
        print("  Invalid ID. It must be 9 digits, e.g. 102348765.")


def read_word(prompt):
    """Fields are space-separated in the text file, so they can't contain spaces."""
    while True:
        value = input(prompt).strip()
        if value and " " not in value:
            return value
        print("  Please enter a single word (no spaces).")


def read_gpa():
    while True:
        try:
            gpa = float(input("GPA (0.0 - 4.0): "))
            if 0.0 <= gpa <= 4.0:
                return gpa
        except ValueError:
            pass
        print("  Invalid GPA.")


def add_student(bst):
    student_id = read_student_id()
    if bst.find(student_id):
        print(f"  A student with Student_ID {student_id} already exists. IDs must be unique.")
        return
    details = {
        "first_name": read_word("First name: "),
        "last_name": read_word("Last name: "),
        "email_id": read_word("Email: "),
        "major": read_word("Major (e.g. CMPAB_BS): "),
        "GPA": read_gpa(),
    }
    bst.insert(student_id, details)
    append_student_to_file(student_id, details)
    print(f"  {details['first_name']} {details['last_name']} added.")


def search_student(bst):
    student_id = read_student_id()
    node = bst.find(student_id)
    if node is None:
        print(f"  No student found with Student_ID {student_id}.")
    else:
        print("  Student found:")
        print_header()
        print_student(node)


def main():
    bst = StudentBST()
    load_students(bst)
    print(f"Loaded {bst.size} students from {os.path.basename(DATA_FILE)} into the BST.")

    menu = """
===== Student BST Menu =====
1. Insert a new student
2. Find a student by Student_ID
3. Print all students
4. Exit"""
    while True:
        print(menu)
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_student(bst)
        elif choice == "2":
            search_student(bst)
        elif choice == "3":
            bst.print_all()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("  Please enter 1-4.")


if __name__ == "__main__":
    main()