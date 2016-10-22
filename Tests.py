import sys;
import pprint;
from Domain_Dependent import *
    
fh = open(sys.argv[1],'r');#sys.stdin;
initialState = state(fh, sys.argv[2]);

newState = initialState.copy();
newState.applyOp(operation('MOVE', 0));
MoveTo(newState, 'B');
MoveTo(newState, 'A');
MoveTo(newState, 'S1');
newState.applyOp(operation('LOAD'));
MoveTo(newState, 'A');
MoveTo(newState, 'B');
MoveTo(newState, 'C');
MoveTo(newState, 'EXIT');

print('CasksProps:');
pprint.pprint(newState.CasksProps);

print('\ninitialState:');
pprint.pprint(initialState);

print('\nnewState:');
pprint.pprint(newState);

print('\nnewState\'s parent:');
pprint.pprint(newState.parent);

print('\nPossible child states:');
pprint.pprint(newState.expandState());

print('\nPossible Ops:');
pprint.pprint(newState.possibleOps());

print('\nWorld:');
pprint.pprint(initialState.World);

print('\nGoal Cask:');
print(newState.GoalCask);

print('\nGoal achieved?');
print(newState.goalAchieved());

print('\nnewState same as initialState?:');
print(newState == initialState);
