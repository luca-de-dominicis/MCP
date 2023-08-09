# MCP

## Multiple couriers problem
```sh
minizinc -m MCP_Sym.mzn -d Instances/instXX.dzn -a -r 781948 --solver-statistics --time-limit 300000 -D mzn_ignore_symmetry_breaking_constraints=false
```

## Constraint Programming (Minizinc)
Run CP model on instance XX WITH symmetry breaking constraints

```sh
minizinc -m MCP_Sym.mzn -d Instances/instXX.dzn -r 781948 --solver-statistics --time-limit 300000 -D mzn_ignore_symmetry_breaking_constraints=false
```

Run CP model on instance XX WITHOUT symmetry breaking constraints

```sh
minizinc -m MCP_Sym.mzn -d Instances/instXX.dzn -a -r 781948 --solver-statistics --time-limit 300000 -D mzn_ignore_symmetry_breaking_constraints=true
```

Command for script
```sh
minizinc -m MCP_Sym.mzn -d Instances/inst03.dzn --time-limit 300000 -D mzn_ignore_symmetry_breaking_constraints=true --output-time --output-objective --output-mode json --search-complete-msg "complete" | head -n -1
```

Generate solutions for MIP and SMT, input_folder must contain the .dat files
```sh
./create_sol input_folder
```

Convert python notebook into python script
jupyter nbconvert --to script SMT.ipynb && grep -vE '# In\[[0-9]+\]:' SMT.py > temp.py && mv temp.py SMT.py

## TODO
- Docker
- Script per minizinc
- Report