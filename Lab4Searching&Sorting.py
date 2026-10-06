"""
CMPSC 412 - Lab 4: Searching and Sorting

Part 1: Binary-search number guessing game (1..5000) with memory tracking
Part 2: Read 30 students from a text file, sort with selection / insertion /
        bubble / merge sort by (a) student id and (b) first name, save the
        results, and print time (Table 1) and memory (Table 2).

Usage:
    python lab4.py                # interactive game, then sorting
    python lab4.py --auto 3721    # game guesses 3721 automatically (for screenshots)
    python lab4.py --skip-game    # only run Part 2
"""

import sys
import time
import argparse

# ----------------------------------------------------------------------------
# Data
# ----------------------------------------------------------------------------
STUDENT_FILE = "students.txt"

STUDENT_DATA = """Student_ID  first_name   last_name    email_id                major          GPA
102348765   Jack         Green        jack.green@psu.edu      CMPAB_BS       3.7
102348750   Olivia       Brown        olivia.brown@psu.edu    CMPAB_BS       3.5
102348748   Sarah        Lee          sarah.lee@psu.edu       CMPAB_BS       3.9
102348755   Benjamin     Anderson     benjamin.anderson@psu.edu CMPAB_BS     3.1
102348767   Henry        Nelson       henry.nelson@psu.edu    CMPAB_BS       3.9
102348749   Michael      Johnson      michael.johnson@psu.edu CMPAB_BS       3.7
102348756   Ava          Thomas       ava.thomas@psu.edu      CMPAB_BS       3.7
102348769   Noah         Mitchell     noah.mitchell@psu.edu   CMPAB_BS       3.7
102348754   Mia          Taylor       mia.taylor@psu.edu      CMPAB_BS       3.8
102348761   Daniel       Walker       daniel.walker@psu.edu   CMPAB_BS       3.5
102348770   Grace        Perez        grace.perez@psu.edu     CMPAB_BS       3.9
102348772   Sophia       Morris       sophia.morris@psu.edu   CMPAB_BS       3.6
102348759   Ethan        Clark        ethan.clark@psu.edu     CMPAB_BS       3.8
102348746   Emma         Williams     emma.w@psu.edu          CMPAB_BS       3.8
102348758   Charlotte    Harris       charlotte.harris@psu.edu CMPAB_BS     3.6
102348751   William      Davis        william.davis@psu.edu   CMPAB_BS       3.6
102348763   Lucas        King         lucas.king@psu.edu      CMPAB_BS       3.6
102348760   Abigail      Lewis        abigail.lewis@psu.edu   CMPAB_BS       3.9
102348762   Ella         Young        ella.young@psu.edu      CMPAB_BS       3.3
102348747   John         Smith        john.smith@psu.edu      CMPAB_BS       3.4
102348753   James        Wilson       james.wilson@psu.edu    CMPAB_BS       3.2
102348785   Jack         Campbell     jack.campbell@psu.edu   CMPAB_BS       3.8
102348757   Alexander    Martinez     alexander.m@psu.edu     CMPAB_BS       3.4
102348773   Mason        Rogers       mason.rogers@psu.edu    CMPAB_BS       3.5
102348766   Harper       Adams        harper.adams@psu.edu    CMPAB_BS       3.5
102348775   Jack         Green        jack.green@psu.edu      CMPAB_BS       3.8
102348768   Scarlett     Carter       scarlett.carter@psu.edu CMPAB_BS       3.4
102348771   Liam         Evans        liam.evans@psu.edu      CMPAB_BS       3.8
102348774   Lily         Reed         lily.reed@psu.edu       CMPAB_BS       3.6
102348752   Isabella     Miller       isabella.miller@psu.edu CMPAB_BS       3.9
"""


def create_student_file(filename=STUDENT_FILE):
    """Store the 30 student records as a text file."""
    with open(filename, "w") as f:
        f.write(STUDENT_DATA)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def size_of_all(*objs):
    """Sum of sys.getsizeof() for each variable passed in (shallow, per object)."""
    return sum(sys.getsizeof(o) for o in objs)


def deep_size(obj, seen=None):
    """Size of a container plus everything inside it (each object counted once)."""
    if seen is None:
        seen = set()
    if id(obj) in seen:
        return 0
    seen.add(id(obj))
    total = sys.getsizeof(obj)
    if isinstance(obj, dict):
        for k, v in obj.items():
            total += deep_size(k, seen) + deep_size(v, seen)
    elif isinstance(obj, (list, tuple, set)):
        for item in obj:
            total += deep_size(item, seen)
    return total


# ----------------------------------------------------------------------------
# PART 1: Binary search number-guessing game
# ----------------------------------------------------------------------------
def guessing_game(auto_secret=None):
    """
    The user thinks of a number from 1 to 5000. The program guesses using
    binary search. After each guess the user answers:
        h = my guess was too high,  l = my guess was too low,  c = correct
    Memory of every variable / data structure is measured at each step.
    """
    print("=" * 70)
    print("PART 1: NUMBER GUESSING GAME (BINARY SEARCH)")
    print("=" * 70)
    if auto_secret is None:
        print("Think of a number between 1 and 5000. I will try to guess it.")
        print("Answer with:  h = too high,  l = too low,  c = correct\n")
    else:
        print(f"[Auto mode] The secret number is {auto_secret}\n")

    low = 1
    high = 5000
    guess_count = 0
    history = []          # data structure that stores every guess
    mem_steps = []        # data structure that stores memory per step
    found = False
    guess = None

    while low <= high:
        guess = (low + high) // 2          # intermediate step of binary search
        guess_count += 1
        history.append(guess)

        print(f"Guess #{guess_count}: is it {guess}?  (range {low}-{high})")

        if auto_secret is None:
            answer = ""
            while answer not in ("h", "l", "c"):
                answer = input("  h (too high) / l (too low) / c (correct): ").strip().lower()
        else:
            answer = "c" if guess == auto_secret else ("h" if guess > auto_secret else "l")
            print(f"  -> {answer}")

        # memory of every variable and data structure at this step
        step_mem = {
            "low": sys.getsizeof(low),
            "high": sys.getsizeof(high),
            "guess": sys.getsizeof(guess),
            "guess_count": sys.getsizeof(guess_count),
            "history (list)": sys.getsizeof(history),
            "answer": sys.getsizeof(answer),
            "found": sys.getsizeof(found),
        }
        mem_steps.append(step_mem)

        if answer == "c":
            found = True
            break
        elif answer == "h":
            high = guess - 1
        else:
            low = guess + 1

    if found:
        print(f"\nI found your number: {guess} in {guess_count} guesses.")
    else:
        print("\nThe answers were inconsistent - I could not find the number.")

    # ---- memory report ----
    print("\nMemory usage (bytes) per variable at the final guess:")
    print(f"  {'Variable':<18}{'Bytes':>8}")
    print("  " + "-" * 26)
    for name, b in mem_steps[-1].items():
        print(f"  {name:<18}{b:>8}")
    final_total = sum(mem_steps[-1].values())
    mem_steps_total = sys.getsizeof(mem_steps)
    print("  " + "-" * 26)
    print(f"  {'TOTAL (variables)':<18}{final_total:>8}")
    print(f"  {'mem_steps (list)':<18}{mem_steps_total:>8}  (the list that stores these records)")

    print("\nMemory per intermediate step (sum of all variables, bytes):")
    print(f"  {'Step':<6}{'Guess':>8}{'Total bytes':>14}")
    print("  " + "-" * 28)
    for i, s in enumerate(mem_steps):
        print(f"  {i + 1:<6}{history[i]:>8}{sum(s.values()):>14}")
    peak = max(sum(s.values()) for s in mem_steps)
    print(f"\nPeak memory across all steps: {peak} bytes")


# ----------------------------------------------------------------------------
# PART 2: Read file
# ----------------------------------------------------------------------------
def read_students(filename=STUDENT_FILE):
    """
    Read the text file into a list of dictionaries (one dict per student).
    List  -> keeps the order of the records and can be sorted
    Dict  -> gives each field a name (student['first_name'])
    Student_ID is stored as int and GPA as float so they sort numerically.
    """
    students = []
    with open(filename) as f:
        header = f.readline().split()
        for line in f:
            parts = line.split()
            if not parts:
                continue
            students.append({
                "Student_ID": int(parts[0]),
                "first_name": parts[1],
                "last_name": parts[2],
                "email_id": parts[3],
                "major": parts[4],
                "GPA": float(parts[5]),
            })
    return header, students


def save_students(students, header, filename):
    """Save the (sorted) records to a different text file."""
    with open(filename, "w") as f:
        f.write(f"{header[0]:<12}{header[1]:<12}{header[2]:<12}{header[3]:<28}{header[4]:<10}{header[5]}\n")
        for s in students:
            f.write(f"{s['Student_ID']:<12}{s['first_name']:<12}{s['last_name']:<12}"
                    f"{s['email_id']:<28}{s['major']:<10}{s['GPA']}\n")


def display_students(students, header):
    print(f"  {header[0]:<12}{header[1]:<12}{header[2]:<12}{header[3]:<28}{header[4]:<10}{header[5]}")
    for s in students:
        print(f"  {s['Student_ID']:<12}{s['first_name']:<12}{s['last_name']:<12}"
              f"{s['email_id']:<28}{s['major']:<10}{s['GPA']}")


# ----------------------------------------------------------------------------
# Sorting algorithms
# Each takes (arr, key, track). arr is sorted in place (except merge sort which
# returns a new list). Each returns (sorted_list, memory_bytes).
# memory_bytes = sys.getsizeof of every local variable / data structure,
# measured individually (never sys.getsizeof on the function itself).
# ----------------------------------------------------------------------------
def selection_sort(arr, key, track=False):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j][key] < arr[min_idx][key]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    mem = size_of_all(arr, key, n, i, j, min_idx) if track else 0
    return arr, mem


def insertion_sort(arr, key, track=False):
    n = len(arr)
    for i in range(1, n):
        current = arr[i]
        j = i - 1
        while j >= 0 and arr[j][key] > current[key]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    mem = size_of_all(arr, key, n, i, j, current) if track else 0
    return arr, mem


def bubble_sort(arr, key, track=False):
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j][key] > arr[j + 1][key]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    mem = size_of_all(arr, key, n, i, j, swapped) if track else 0
    return arr, mem


def merge_sort(arr, key, track=False, stats=None):
    """
    Recursive merge sort. When track=True, `stats` keeps:
      live  - bytes of auxiliary lists/variables currently alive
      peak  - the maximum value live ever reached
    """
    if stats is None:
        stats = {"live": 0, "peak": 0}
    n = len(arr)
    if n <= 1:
        return arr, (stats["peak"] if track else 0)

    mid = n // 2
    left, _ = merge_sort(arr[:mid], key, track, stats)
    right, _ = merge_sort(arr[mid:], key, track, stats)

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][key] <= right[j][key]:      # <= keeps the sort stable
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])

    if track:
        local = size_of_all(left, right, merged, n, mid, i, j)
        stats["live"] += local
        stats["peak"] = max(stats["peak"], stats["live"])
        stats["live"] -= local
    return merged, (stats["peak"] if track else 0)


ALGORITHMS = [
    ("Selection Sort", selection_sort),
    ("Insertion Sort", insertion_sort),
    ("Bubble Sort", bubble_sort),
    ("Merge Sort", merge_sort),
]


# ----------------------------------------------------------------------------
# Sort driver
# ----------------------------------------------------------------------------
def sort_students(students, sort_by, algo_name, algo_func, header, repeats=2000):
    """
    Sort the whole list by `sort_by` ('Student_ID' or 'first_name') using the
    given algorithm. Returns (sorted_list, cpu_time_seconds, memory_bytes).

    CPU time (time.process_time) of a single sort of 30 rows is far below the
    clock resolution, so each sort is repeated `repeats` times on a fresh copy
    and the average per sort is reported.
    """
    # --- memory (one tracked run) ---
    working = list(students)                       # shallow copy; records are shared
    sorted_list, algo_mem = algo_func(working, sort_by, track=True)
    working_list_size = sys.getsizeof(working)
    mem_total = algo_mem + working_list_size       # algorithm's locals + the working list
    # (selection/insertion/bubble already counted `arr`, merge sort did not
    #  count the original `arr`, so add it for a fair comparison)
    if algo_func is not merge_sort:
        mem_total = algo_mem                       # arr already inside algo_mem

    # --- CPU time ---
    start = time.process_time()
    for _ in range(repeats):
        tmp = list(students)
        algo_func(tmp, sort_by)
    cpu_avg = (time.process_time() - start) / repeats

    return sorted_list, cpu_avg, mem_total


def print_table(title, row_labels, col_labels, values, fmt):
    width = 18
    print("\n" + title)
    line = "+" + "-" * width + ("+" + "-" * 22) * len(col_labels) + "+"
    print(line)
    print("|" + "Algorithm".ljust(width) + "".join("|" + c.center(22) for c in col_labels) + "|")
    print(line)
    for label, row in zip(row_labels, values):
        print("|" + label.ljust(width) + "".join("|" + fmt(v).center(22) for v in row) + "|")
    print(line)


def run_sorting_part():
    print("=" * 70)
    print("PART 2: SORTING STUDENT RECORDS")
    print("=" * 70)

    create_student_file()
    header, students = read_students()
    print(f"Read {len(students)} student records from '{STUDENT_FILE}'.")
    print(f"Records are stored as a list of dictionaries "
          f"(list size {sys.getsizeof(students)} bytes, "
          f"deep size of all data {deep_size(students)} bytes).\n")

    sort_keys = [("Student_ID", "Student ID", "id"), ("first_name", "First Name", "first_name")]
    times = {name: [] for name, _ in ALGORITHMS}
    mems = {name: [] for name, _ in ALGORITHMS}

    for field, nice, tag in sort_keys:
        for algo_name, algo_func in ALGORITHMS:
            sorted_list, cpu, mem = sort_students(students, field, algo_name, algo_func, header)
            times[algo_name].append(cpu)
            mems[algo_name].append(mem)

            outfile = f"sorted_by_{tag}_{algo_name.split()[0].lower()}.txt"
            save_students(sorted_list, header, outfile)

        # Display the sorted result once per key (identical for every algorithm,
        # apart from the order of ties in first_name for non-stable sorts).
        print(f"--- All students sorted by {nice} (merge sort result) ---")
        display_students(sort_students(students, field, "Merge Sort", merge_sort, header, repeats=1)[0], header)
        print()

    names = [n for n, _ in ALGORITHMS]
    cols = ["Sort by Student ID", "Sort by First Name"]

    print_table("TABLE 1: CPU time per sort (microseconds, average of 2000 runs)",
                names, cols, [times[n] for n in names], lambda v: f"{v * 1e6:,.2f} us")
    print_table("TABLE 2: Memory used by each sorting algorithm (bytes)",
                names, cols, [mems[n] for n in names], lambda v: f"{v:,} bytes")

    print("\nSorted output files written:")
    for tag in ("id", "first_name"):
        for algo_name, _ in ALGORITHMS:
            print(f"  sorted_by_{tag}_{algo_name.split()[0].lower()}.txt")


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CMPSC 412 Lab 4")
    parser.add_argument("--auto", type=int, help="let the program play the game with this secret number")
    parser.add_argument("--skip-game", action="store_true", help="skip Part 1")
    args = parser.parse_args()

    if not args.skip_game:
        guessing_game(args.auto)
    run_sorting_part()