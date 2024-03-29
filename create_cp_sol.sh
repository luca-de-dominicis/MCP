for file in $1/*; do
  if [[ $file == *.dzn ]]
  then
    base=${file%.*}
    num=${base: -2}
    time_th=300000

    echo "---Solving CP for instance $num using GECODE---"
    echo "gecode" > .temp/temp_$num.out
    minizinc -m MCP_CP.mzn -d $file --time-limit $time_th --solver gecode -D mzn_ignore_symmetry_breaking_constraints=true --output-time --output-objective --output-mode json --json-stream --search-complete-msg "optimal" | head -n 1 >> .temp/temp_$num.out

    echo "---Solving CP for instance $num using GECODE with symbreak---"
    echo "&" >> .temp/temp_$num.out
    echo "gecode_symbreak" >> .temp/temp_$num.out
    minizinc -m MCP_CP.mzn -d $file --time-limit $time_th --solver gecode -D mzn_ignore_symmetry_breaking_constraints=false --output-time --output-objective --output-mode json --json-stream --search-complete-msg "optimal" | head -n 1 >> .temp/temp_$num.out
    
    echo "---Solving CP for instance $num using CHUFFED---"
    echo "&" >> .temp/temp_$num.out
    echo "chuffed" >> .temp/temp_$num.out
    minizinc -m MCP_CP_norandom.mzn -d $file --time-limit $time_th --solver chuffed -D mzn_ignore_symmetry_breaking_constraints=true --output-time --output-objective --output-mode json --json-stream --search-complete-msg "optimal" 2> /dev/null | head -n 1 >> .temp/temp_$num.out
    
    echo "---Solving CP for instance $num using CHUFFED with symbreak---"
    echo "&" >> .temp/temp_$num.out
    echo "chuffed_symbreak" >> .temp/temp_$num.out
    minizinc -m MCP_CP_norandom.mzn -d $file --time-limit $time_th --solver chuffed -D mzn_ignore_symmetry_breaking_constraints=false --output-time --output-objective --output-mode json --json-stream --search-complete-msg "optimal" 2> /dev/null | head -n 1 >> .temp/temp_$num.out
    python3 generate_cp.py $num

    echo ""
    echo ""
  fi
done

rm -f .temp/*