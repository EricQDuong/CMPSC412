import time
import random

#timer function so no repeated time calculation has to be done for all problems
#*args means that anything passed into func is accepted
def timer(func, *args, repeats=10000):
    start = time.perf_counter()
    for _ in range(repeats):
        func(*args)
    end = time.perf_counter()
    return (end - start) / repeats

def masterData():
    master = []
    for i in range(2000):
        master.append(random.randint(1, 5000))
    return master

def data():
    listy = masterData()
    diction = {}
    for num in listy:
        if num in diction:
            diction[num] += 1
        else:
            diction[num] = 1
    return diction, listy

def printList(listy):
    print(listy)

def printDiction(diction):
    print(diction)

def problemOne():
    for i in range(3):
        print(f"\nTrial {i+1}:")
        diction, listy = data()

        time_list = timer(printList, listy, repeats=1)
        time_dict = timer(printDiction, diction, repeats=1)

        print(f"List print time: {time_list} seconds")
        print(f"Dictionary print time: {time_dict} seconds")


def findList(listy, target):
    return target in listy

def findDictionary(dictionary, target):
    return target in dictionary

def problemTwo():
    for i in range(3):
        print(f"\nTrial {i+1}:")
        diction, listy = data()

        target = random.randint(1, 5000)

        time_list = timer(findList, listy, target)
        time_dict = timer(findDictionary, diction, target)

        print(f"List find time: {time_list} seconds")
        print(f"Dictionary find time: {time_dict} seconds")


def insertList(listy, target):
    listy.append(target)
    print(listy)

def insertDictionary(dictionary, target):
    if target in dictionary:
        dictionary[target] += 1
    else:
        dictionary[target] = 1
    print(dictionary)

def problemThree():
    for i in range(3):
        print(f"\nTrial {i+1}:")
        diction, listy = data()

        target = random.randint(1, 5000)

        time_list = timer(insertList, listy, target, repeats=1)
        time_dict = timer(insertDictionary, diction, target, repeats=1)

        print(f"List insert time: {time_list} seconds")
        print(f"Dictionary insert time: {time_dict} seconds")

def deleteList(listy, target):
    listy.remove(target)

def deleteDictionary(dictionary, target):
    del dictionary[target]

def problemFour():
    for i in range(3):
        print(f"\nTrial {i+1}:")
        diction, listy = data()

        target = random.choice(listy)

        time_list = timer(deleteList, listy, target, repeats=1)
        time_dict = timer(deleteDictionary, diction, target, repeats=1)

        print(f"List delete time: {time_list} seconds")
        print(f"Dictionary delete time: {time_dict} seconds")

problemOne()
problemTwo()
problemThree()
problemFour()