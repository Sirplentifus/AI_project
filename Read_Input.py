import sys;
import pprint;
from GraphClasses import *
    
initialState = state();

initialState.GoalCask = sys.argv[1];

fh = open('../input.txt','r');#sys.stdin;

while(1):
    a=fh.readline();
    params = a.split();
    if(len(a) == 0):
        print('Finished reading\n');
        break;
    if(a.isspace()):
        continue;
    elif(a[0] == 'C'):
        initialState.CasksProps[params[0]] = cask(int(params[1]), float(params[2]));
    elif(a[0] == 'S'):
        S = stack(int(params[1]));
        initialState.Stacks[params[0]] = S;
        
        for i in range(2, len(params)):
            initialState.insertToStack(params[0], params[i]);
        
        
    elif(a[0] == 'E'):
        NodeLeftID = params[1];
        NodeRightID = params[2];
        Cost = float(params[3]);
        
        EdgeToRight = edgeTo(NodeRightID, Cost);
        EdgeToLeft = edgeTo(NodeLeftID, Cost);
        
        NodeLeft = initialState.World.setdefault(NodeLeftID, []);
        NodeLeft.append(EdgeToRight);
        
        NodeRight = initialState.World.setdefault(NodeRightID, []);
        NodeRight.append(EdgeToLeft);
        
    else:
        continue; #project description says that "All other lines should be ignored"

if(initialState.CasksProps.get(initialState.GoalCask) == None):
    raise(ValueError('The cask to be retireved isn\'t present in the world'));

#Everything below are tests

EstadoNovo = initialState.copy();
EstadoNovo.applyOp(operation('MOVE', 0));
MoveTo(EstadoNovo, 'B');
MoveTo(EstadoNovo, 'A');
MoveTo(EstadoNovo, 'S1');
EstadoNovo.applyOp(operation('LOAD'));
#~ MoveTo(EstadoNovo, 'A');
#~ MoveTo(EstadoNovo, 'B');
#~ MoveTo(EstadoNovo, 'C');
#~ MoveTo(EstadoNovo, 'EXIT');

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

print('\nStack S2 is equal to S3?:');
print(EstadoNovo.Stacks['S1'] == EstadoNovo.Stacks['S2']);
