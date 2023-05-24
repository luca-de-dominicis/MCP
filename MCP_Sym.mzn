include "globals.mzn";

int: m;
int: n;

array[1..m] of int: load;
array[1..n] of int: size;

array[1..n+1, 1..n+1] of int: D;

int: o = n+1;

array[1..n, 1..m] of var 0..1: dest_assignment;
array[1..m, 0..n+1] of var 1..n+1: tour;

% constraint forall(i in 1..n)(
%    sum(j in 1..m)(dest_assignment[i,j]) = 1); % So each destination can be assigned to exactly one courier
   
constraint forall(i in 1..n)(
  count(j in 1..m)(dest_assignment[i,j] == 1) = 1);
   
   
constraint forall(i in 1..m)(
   sum(j in 1..n)(size[j] * dest_assignment[j,i]) <= load[i]); % Each courier cannot load more than his capacity
   
constraint forall(i in 1..m)(
   tour[i,0] = o /\ tour[i,n+1] = o
);
   
constraint forall(c in 1..m, i in 1..n)(
  dest_assignment[i,c] == 1 -> exists(j in 1..n)(tour[c,j] = i)
); % assigned items must be in courier's tour


constraint forall(i in 1..m, j in 1..n)(
   dest_assignment[j,i] == 1 -> (count(j1 in 0..n+1)(tour[i,j1] == j) == 1)
);


constraint redundant_constraint( forall(i in 1..m, j in 1..n)(
    dest_assignment[j,i] == 0 -> (count(j1 in 0..n+1)(tour[i,j1] == j) == 0)
));

% constraint forall(i in 1..m)(
%     let {var int: k = count(j in 1..n)(dest_assignment[j,i] == 1)} in
%     forall(j1 in k+1..n+1)(tour[i,j1] = o));
    
constraint forall(i in 1..m)(
    forall(j in 1..n)(
    if tour[i,j] == o
    then tour[i,j+1] = o
    endif));
    
        
var int: maxDist = max(i in 1..m)(sum(j in 0..n)(D[tour[i,j], tour[i,j+1]]));
var int: totalDist = sum(i in 1..m, j in 0..n)(D[tour[i,j], tour[i,j+1]]);


   
 % maxdist boundness constraints
constraint (
  maxDist >= min(i in 1..n)(D[o,i] + D[i,o])
);     
solve minimize maxDist;


output [
"MaxDist: ", show(maxDist), "\n",
"Total: ", show(totalDist), "\n"] ++
["Tour:", "\n"] ++
[
if j == n+1 
then show(tour[i,j]) ++ "\n"
else show(tour[i,j]) ++ " "
endif | i in 1..m, j in 0..n+1]

    
   