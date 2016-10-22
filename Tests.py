import sys;
import pprint;
from Domain_Dependent import *
    
fh = open('../input.txt','r');#sys.stdin;
initialState = state(fh, sys.argv[1]);

EstadoNovo = initialState.copy();
EstadoNovo.applyOp(operation('MOVE', 0));
MoveTo(EstadoNovo, 'B');
MoveTo(EstadoNovo, 'A');
MoveTo(EstadoNovo, 'S1');
EstadoNovo.applyOp(operation('LOAD'));
MoveTo(EstadoNovo, 'A');
MoveTo(EstadoNovo, 'B');
MoveTo(EstadoNovo, 'C');
MoveTo(EstadoNovo, 'EXIT');

print('CasksProps:');
pprint.pprint(EstadoNovo.CasksProps);

print('\ninitialState:');
pprint.pprint(initialState);

print('\nEstadoNovo:');
pprint.pprint(EstadoNovo);

print('\nEstadoNovo\'s parent:');
pprint.pprint(EstadoNovo.parent);

print('\nPossible child states:');
pprint.pprint(EstadoNovo.expandState());

print('\nPossible Ops:');
pprint.pprint(EstadoNovo.possibleOps());

print('\nWorld:');
pprint.pprint(initialState.World);

print('\nGoal Cask:');
print(EstadoNovo.GoalCask);

print('\nGoal achieved?');
print(EstadoNovo.goalAchieved());

print('\nEstadoNovo same as initialState?:');
print(EstadoNovo == initialState);
