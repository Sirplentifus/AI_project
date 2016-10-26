import sys;

from Domain_Dependent import *;
from General_Search import *;
from Heuristics import GhostRobotHeuristic;


fh = open(sys.argv[1],'r');

initialState = state(fh, sys.argv[2], GhostRobotHeuristic());
solution = General_Search(initialState);

print(solution.allOpsToThis());
print('problem solved?: %s'%solution.goalAchieved());
