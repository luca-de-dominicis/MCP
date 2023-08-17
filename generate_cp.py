import sys, json, math

"""
Input file structure is:
{"type": "solution", "output": {"json": {  "dest_assignment" : [[1, 0], [0, 1], [1, 0], [1, 0], [0, 1], [0, 1]],  "tour" : [[7, 4, 3, 1, 7, 7, 7, 7], [7, 2, 5, 6, 7, 7, 7, 7]],  "_objective" : 14}}, "sections": ["json"], "time": 108}
solver
&
{"type": "solution", "output": {"json": {  "dest_assignment" : [[1, 0], [0, 1], [1, 0], [1, 0], [0, 1], [0, 1]],  "tour" : [[7, 1, 3, 4, 7, 7, 7, 7], [7, 2, 5, 6, 7, 7, 7, 7]],  "_objective" : 14}}, "sections": ["json"], "time": 114}
solver
&
{"type": "solution", "output": {"json": {  "dest_assignment" : [[1, 0], [0, 1], [1, 0], [1, 0], [0, 1], [0, 1]],  "tour" : [[7, 1, 3, 4, 7, 7, 7, 7], [7, 2, 5, 6, 7, 7, 7, 7]],  "_objective" : 14}}, "sections": ["json"], "time": 114}
solver
"""

# Filter tour array
def courier_tour(tour):
    n = max(tour)
    out = [tour[i] for i in range(len(tour)) if tour[i] != n]
    return out

file_number = sys.argv[1]

file = open("./.temp/temp_"+file_number+".out", "r")
lines = file.readlines()
file.close()

output_json = {}

i = 0
solver = ""
for line in lines:
    match i:
        case 0:
          solver = line.rstrip()
          output_json.update({solver: {}})
          i = i+1
        case 1:
            js = json.loads(line)
            out = {
                  "time": math.floor(float(js["time"])/1000),
                  "optimal": js["time"]<300000,
                  "obj": js["output"]["json"]["_objective"],
                  "sol": [courier_tour(c) for c in js["output"]["json"]["tour"]]
            }

            output_json[solver] = out
            i = i+1
        case 2:
            i = 0

with open("./res/CP/"+file_number+".json", "w") as write_file:
    json.dump(output_json, write_file)
    