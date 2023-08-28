# MCP

## Multiple couriers problem
```sh
minizinc -m MCP_CP.mzn -d Instances/instXX.dzn -a -r 781948 --solver-statistics --time-limit 300000 -D mzn_ignore_symmetry_breaking_constraints=false
```

## Constraint Programming (Minizinc)
Run CP model on instance XX WITH symmetry breaking constraints

```sh
minizinc -m MCP_CP.mzn -d Instances/instXX.dzn -r 781948 --solver-statistics --time-limit 300000 -D mzn_ignore_symmetry_breaking_constraints=false
```

Run CP model on instance XX WITHOUT symmetry breaking constraints

```sh
minizinc -m MCP_CP.mzn -d Instances/instXX.dzn -a -r 781948 --solver-statistics --time-limit 300000 -D mzn_ignore_symmetry_breaking_constraints=true
```

## MIP

Run the mixed integer programming model on instance XX, the .dat file will be taken from the *Instances* folder, this will also generate the solution json in *res/MIP*

```sh
python MIP.py XX
```

## SMT

Run the satisfiabilirt modulo theory model on instance XX, the .dat file will be taken from the *Instances* folder, this will also generate the solution json in *res/SMT*.

```sh
python SMT.py XX
```
Be aware that Z3 is unable to report a partial solution, if it can't find an optimal solution in the 5 minutes time limit it returns an upper bound if it found one.

## Generate solutions
Generate solutions for MIP and SMT, input_folder must contain the .dat files
```sh
./create_sol input_folder
```
For both MIP and SMT it is possible to generate the json also for just one instance with the commands reported before.

Generate solutions for CP, input_folder must contain the .dzn files.
```sh
./create_cp_sol input_folder
```

Build and run docker
```sh
docker build -t cdmo . && docker run -it cdmo
```

## TODO
- Report
- Aggiungere lower-bound alla max dist
- Aggiungere immagini per capire meglio (se necessario e se possibile)
- Trovare una quadra per i constraint di cp e verificare che gli implied non cambino il solution set