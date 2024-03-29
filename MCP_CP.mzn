include "globals.mzn";

% couriers
int: m;

% total number of items (n >=m)
int: n;

% capacity per courier
array[1..m] of int: load;

% weight/size of each item
array[1..n] of int: size;

% Distance matrix (not symmetrical)
% D[i,j] distance between distribution point i and j
% D[i, n+1] distance between dist. point i and origin o
array[1..n+1, 1..n+1] of int: D;

% depot
int: o = n+1;

% assignment of items to distr. point
% dest[i,j] = 1 ---> item i assigned to courier j
array[1..n, 1..m] of var 0..1: dest_assignment;

% couriers tour
% tour[i,j] = 4 ---> courier i dispatched item 4 in his j-th route
array[1..m, 0..n+1] of var 1..n+1: tour;

%---------CONSTRAINTS----------%

% Each destination can be assigned to exactly one courier
constraint forall(i in 1..n)(
  count(c in 1..m)(dest_assignment[i,c] == 1) = 1);

% Each courier cannot load more than his capacity
constraint forall(c in 1..m)(
   sum(i in 1..n)(size[i] * dest_assignment[i,c]) <= load[c]); 

% initial and final destination are the same
constraint forall(c in 1..m)(
   tour[c,0] = o /\ tour[c,n+1] = o
);

% Each assigned item is dispatched just once
constraint forall(c in 1..m, i in 1..n)(
   dest_assignment[i,c] == 1 -> (count(j in 0..n+1)(tour[c,j] == i) == 1)
);

% Cannoy depart again once at the depot
constraint forall(c in 1..m, j in 1..n)(
    % if tour[c,j] == o
    %   then tour[c,j+1] = o
    % endif
    tour[c,j] == o -> tour[c,j+1] == o
);

% Assigned items must be in courier's tour
constraint redundant_constraint(
  forall(c in 1..m, i in 1..n)(
    dest_assignment[i,c] == 1 -> exists(j in 1..n)(tour[c,j] = i)
  )
);

% If courer i does not dispatch item j, then j is not in his tour
constraint redundant_constraint(
  forall(c in 1..m, i in 1..n)(
    dest_assignment[i,c] == 0 -> (count(j in 0..n+1)(tour[c,j] == i) == 0)
  )
);

% Having an item in the tour implies that that item is assigned
constraint redundant_constraint(
  forall(c in 1..m, i in 1..n, j in 1..n+1)(
    tour[c,j] == i -> dest_assignment[i,c] == 1
  )
);
        
% courier tour symmetry breaking for couriers with same load capacity
constraint symmetry_breaking_constraint(
  forall(c in 1..m)(
    forall(c_eq in 1..m)(
      if c != c_eq /\ load[c] == load[c_eq]
        then 
          lex_greatereq(array1d(dest_assignment), [ if i = c then dest_assignment[j, c_eq]
                                           elseif i = c_eq then dest_assignment[j, c]
                                           else dest_assignment[j, i]
                                           endif
                                           | j in 1..n, i in 1..m ])
      endif
    )
  )
);

% symmetry breaking for each courier, shifted routes are deleted (41344 == 44134)
constraint symmetry_breaking_constraint(
  forall(c in 1..m)(
    let {var int: maxShift = count(h in 0..n+1)(tour[c, h]==o)-2} in
    forall (shift in 1..maxShift)(
      lex_lesseq([tour[c, i] | i in 1..n], [tour[c, (j + maxShift + 1) mod o] | j in 1..n])
    )
  )
);

var int: maxDist = max(c in 1..m)(sum(j in 0..n)(D[tour[c,j], tour[c,j+1]]));
% var int: totalDist = sum(c in 1..m, j in 0..n)(D[tour[c,j], tour[c,j+1]]);


% maxdist boundness constraints
constraint (
  maxDist >= min(i in 1..n)(D[o,i] + D[i,o])
);

solve
 :: int_search(tour, dom_w_deg, indomain_random)
 :: restart_luby(2000)
 minimize maxDist;

% User friendly output
% output [
%  "MaxDist: ", show(maxDist), "\n",
%  "Total Dist:", show(totalDist), "\n",
% ]++
% ["Tours:", "\n"]++
% [
% %  if j == n+1 then show(tour[i,j]) ++ "\n" 
% %    elseif fix(tour[i,j]) == n+1 then "o " 
% %    else show(tour[i,j]) ++ " " 
% %  endif |
%  i in 1..m, j in 0..n+1
%   if j == n+1 then show(tour[i,j]) ++ "\n"
%    else show(tour[i,j]) ++ " " 
%  endif |
%  i in 1..m, j in 0..n+1
% ]

    
   