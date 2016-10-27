import sys;

from Domain_Dependent import *;
from General_Search import *;
from Heuristics import InfiniteStacksHeuristic;


fh = open(sys.argv[1],'r');

initialState = state(fh, sys.argv[2], InfiniteStacksHeuristic());
solution = General_Search(initialState);

print(solution.allOpsToThis());
