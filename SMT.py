#!/usr/bin/env python
# coding: utf-8

# SMT
from itertools import combinations
from z3 import *
import math, sys, json, time

def courier_tour(courier):
    out = [int(str(model[tour[courier][i]]))+1 for i in range(n+2)]
    out = [out[i] for i in range(len(out)) if out[i] != n+1]
    return out

def print_input_info():
    print(f'Couriers: {m}')
    print(f'Items: {n}')
    print(f'Couriers Load: {load}')
    print(f'Item\'s size: {size}')
    print('Distance matrix:')
    for i in range(n+1):
        for j in range(n+1):
            print(instance[i][j], end = " ")
        print()

# Caricamento dati
file_number = sys.argv[1]

file = open("./Instances/inst"+file_number+".dat", "r")
lines = file.readlines()
file.close()
m = int(lines[0].rstrip(''))
n = int(lines[1].rstrip(''))
load = [int(x) for x in lines[2].split(' ')]
size = [int(x) for x in lines[3].split(' ')]
instance = [[int(x) for x in line.rstrip().split(' ') ]for line in lines[4:]]
o = n

# Definizione solver
# s = Solver()
s = Optimize()


# Utils
def at_least_one_np(bool_vars):
    return Or(bool_vars)

def at_most_one_np(bool_vars):
    return And([Not(And(pair[0], pair[1])) for pair in combinations(bool_vars, 2)])

def exactly_one_np(bool_vars):
    return And(at_least_one_np(bool_vars), at_most_one_np(bool_vars))

def all_false(bool_vars):
    return And([And(Not(pair[0]), Not(pair[1])) for pair in combinations(bool_vars, 2)])


start = time.time()

# Decision variables
dest_assignment = [[Bool(f'dest_assignment_{i}_{j}') for j in range(m)] for i in range(n)]

# tour[i][j] = x ---> courier i dispatch item x at j-th route
tour = [[Int(f'tour_{i}_{j}') for j in range(n+2)] for i in range(m)]

# Distance matrix
D_val = ArraySort(IntSort(), IntSort())
D = Array('D', IntSort(), D_val)

# Maxdist objective variable
maxDist = Int("maxDist")

# Constraints

# Matrix D initialization
for i in range(n+1):
    for j in range(n+1):
        s.add(D[i][j] == instance[i][j])

# Each item is assigned to exactly one courier
for i in range(n):
    s.add(exactly_one_np([dest_assignment[i][j] for j in range(m)]))

# Each courier cannot load more than his capacity
for j in range(m):
    s.add(sum([If(dest_assignment[i][j], size[i], 0) for i in range(n)]) <= load[j])

# Initial and final destinations are the same
for c in range(m):
    s.add(And(tour[c][0] == o, tour[c][n+1] == o))

# Each assigned item is dispatched just once
for c in range(m):
    for i in range(n):
        s.add(Implies(dest_assignment[i][c], exactly_one_np([tour[c][j] == i for j in range(1,n+1)])))

# If courier c does not dispatch item i, then i is not in his tour
for c in range(m):
    for i in range(n):
        s.add(Implies(Not(dest_assignment[i][c]), all_false([tour[c][j] == i for j in range(1, n+1)])))

# Cannot go back to deposit
for c in range(m):
    for j in range(1,n):
        s.add(Implies(tour[c][j] == o, tour[c][j+1] == o))

# Having an item in the tour implies that that item is assigned
for c in range(m):
    for j in range(1,n+1):
        s.add([Implies(tour[c][j] == i, dest_assignment[i][c]) for i in range(n)])

# Limit the range of assignable item to only valid one
for c in range(m):
    for j in range(1,n+1):
        s.add(And(tour[c][j]<=n, tour[c][j]>=0))


# Objective function, minize max distance
maxList = [Sum([D[tour[c][i]][tour[c][i+1]] for i in range(n+1)]) for c in range(m)]

for c in range(m):
    s.add(maxDist >= maxList[c])

# Lower bound on maxDist
smaller_path = min(instance[o][i] + instance[i][o] for i in range(o))
s.add(maxDist >= smaller_path)

z = s.minimize(maxDist)


s.set("timeout", 300000)
set_param("parallel.enable", True)
status = s.check()

elapsed_time = time.time() - start

if status == sat:
    model = s.model()
    print("sat")
    for i in range(m):
        print(f"Courier {i}")
        out = [int(str(model[tour[i][j]])) for j in range(n+2)]
        out = [out[i] for i in range(len(out)) if out[i] != n]
        print(f"Tour: {out}")
    
    dist = [sum([ instance[int(str(model[tour[i][j]]))][int(str(model[tour[i][j+1]]))] for j in range(n+1) if i in range(n)]) for i in range(m)]
    # print("Distances:", dist)
    print("MaxDist:", z.value())
    # print("Total Dist:", sum(dist))
else:
    print(status)

output_dict = {
    "Z3":
    {
        "time": math.floor(elapsed_time),
        "optimal": status == sat,
        "obj": int(str(z.value())) if status == sat else int(str(z.upper())) if status == unknown and str(z.upper()) != 'oo' else 0,
        "sol": [courier_tour(c) for c in range(m)] if status == sat else [] 
    }
}

with open("./res/SMT/"+file_number+".json", "w") as write_file:
    json.dump(output_dict, write_file)