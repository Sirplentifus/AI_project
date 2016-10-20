import sys;
        
from GraphClasses import *
    
initialState = state();

fh = open('input.txt','r');#sys.stdin;


while(1):
    a=fh.readline();
    params = a.split();
    if(len(a) == 0):
        print('Finished reading\n');
        break;
    if(a.isspace()):
        continue;
    elif(a[0] == 'C'):
        CaskDict[params[0]] = cask(int(params[1]), int(params[1]));
    elif(a[0] == 'S'):
        S = stack(int(params[1]));
        initialState.Stacks[params[0]] = S;
        
        for i in range(2, len(params)):
            initialState.insertToStack(params[0], params[i]);
        
        
    elif(a[0] == 'E'):
        print('Its an edge');
    else:
        print('Its not valid\n');
        
print(CaskDict);

print(initialState);


