for file in $1/*; do
  if [[ $file == *.dat ]]
  then
    base=${file%.*}
    num=${base: -2}
    echo "---Solving SMT for instance $num---"
    python3 SMT.py $num
    echo ""
    echo ""

    echo "---Solving MIP for instance $num---"
    python3 MIP.py $num
    echo ""
    echo ""
  fi
done