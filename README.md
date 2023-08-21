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

Generate solutions for MIP and SMT, input_folder must contain the .dat files
```sh
./create_sol input_folder
```

Generate solutions for CP, input_folder must contain the .dzn files
```sh
./create_sol input_folder
```

Build and run docker
```sh
docker build -t cdmo . && docker run -it cdmo
```

Convert python notebook into python script
jupyter nbconvert --to script SMT.ipynb && grep -vE '# In\[[0-9]+\]:' SMT.py > temp.py && mv temp.py SMT.py

## TODO
- Report
- Aggiungere lower-bound alla max dist
- Aggiungere immagini per capire meglio (se necessario e se possibile)
- Aggiungere dettagli a sezione implied constraints
- Controllare che effettivamente gli implied constraint diano lo stesso risultato ( per definizione non modificano il solution set)
- I symbreak che abbiamo scritto non funzionano
- Il constraint "Having an item in the tour implies that the item is assigned" può essere messo anche in CP
- Controllare teorie e sort