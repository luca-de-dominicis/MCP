#!/usr/bin/env python
# coding: utf-8

from mip import *
import json, time, math, sys

def courier_tour(courier):
    done = False
    index = n
    out =[]
    while not done:
        for j in range(n+1):
            if tour[courier][index][j].x:
                if j == n:
                    done = True
                    break
                out.append(j+1)
                break
        index = j
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
# print_input_info()


start = time.time()
# Matrix model
model = Model(sense=MINIMIZE, solver_name=CBC)

# tour[c,i,j] == 1 ---> courier c performed movement from i to j
tour = model.add_var_tensor((m, n+1, n+1), "tour", var_type=BINARY)

# variable for subtours elimination
u = [model.add_var("u[%d]" % i, var_type=INTEGER, lb=0, ub=n) for i in range(n)]


maxDist = model.add_var("maxDist", var_type=INTEGER)
model.objective = maxDist

# Constraints for matrix model

# Each item is assigned to exactly one courier
for j in range(n):
    model += xsum([tour[c][i][j] for c in range(m) for i in range(n+1)]) == 1

# Each courier get only one time to the same item
for c in range(m):
    for i in range(n+1):
        model += xsum([tour[c][i][j] for j in range(n+1)]) == xsum([tour[c][j][i] for j in range(n+1)]) 

# Can't stay in the same spot
for c in range(m):
    for i in range(n+1):
        model += tour[c][i][i] == 0

# Each courier cannot load more than his capacity
for c in range(m):
    model += xsum([tour[c][i][j]*size[j] for i in range(n+1) for j in range(n)]) <= load[c]

# Initial and final destination are the same
for c in range(m):
    model += xsum([tour[c][n][j] for j in range(n)]) == 1
    model += xsum([tour[c][j][n] for j in range(n)]) == 1

# Miller-Tucker-Zemlin formulation for subtours elimination
for i in range(n):
    for j in range(n):
        for c in range(m):
            model += u[j] - u[i] >= 1 - n*(1 - tour[c][i][j])

distList = [xsum(instance[i][j]*tour[c][i][j] for i in range(n+1) for j in range(n+1)) for c in range(m)]
for c in range(m):
    model += maxDist >= distList[c]


time_limit = 300
status = model.optimize(max_seconds=time_limit)

elapsed_time = time.time() - start

if status == OptimizationStatus.OPTIMAL:
    for c in range(m):
        print(f"Courier {c}")
        # for i in range(n+1):
        #     print([tour[c][i][j].x for j in range(n+1)])
        print(f"TOUR: {courier_tour(c)}")
    print('optimal solution cost {} found'.format(model.objective_value))
elif status == OptimizationStatus.FEASIBLE:
    elapsed_time = time_limit
else:
    elapsed_time = time_limit
    print('no feasible solution found, lower bound is: {}'.format(m.objective_bound))
        
output_dict = {
    "cbc":
    {
        "time": math.ceil(elapsed_time),
        "optimal": status == OptimizationStatus.OPTIMAL,
        "obj": round(model.objective_value),
        "sol": [courier_tour(c) for c in range(m)]
    }
}

with open("./res/MIP/"+file_number+".json", "w") as write_file:
    json.dump(output_dict, write_file)