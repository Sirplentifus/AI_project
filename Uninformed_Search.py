import sys;

from Domain_Dependent import *;
from General_Search import *;

fh = open(sys.argv[1],'r');

#No heuristic is used
initialState = state(fh, sys.argv[2]);
solution = General_Search(initialState);

print(solution.allOpsToThis());
print('problem solved?: %s'%solution.goalAchieved());

