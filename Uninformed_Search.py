import sys;

from Domain_Dependent import *;

#Solves the problem using an uninformed uniform cost search - always expanding the lowest cost node
def General_Search(start_node):
    frontier = [start_node];
    explored = [];
    newNode = start_node.copy();
    
    #~ while(1):
        #~ assert frontier;
        #~ node = frontier.pop();
        #~ if(
        
    newNode = MoveTo(start_node, 'C');
    newNode = MoveTo(newNode, 'D');
    newNode = MoveTo(newNode, 'A');
    newNode = MoveTo(newNode, 'S1');
    newNode = MoveTo(newNode, 'LOAD');
    newNode = MoveTo(newNode, 'A');
    newNode = MoveTo(newNode, 'S11');
    newNode = MoveTo(newNode, 'UNLOAD');
    newNode = MoveTo(newNode, 'A');
    newNode = MoveTo(newNode, 'S1');
    newNode = MoveTo(newNode, 'LOAD');
    newNode = MoveTo(newNode, 'A');
    newNode = MoveTo(newNode, 'D');
    newNode = MoveTo(newNode, 'C');
    newNode = MoveTo(newNode, 'EXIT');
    
    return newNode;

        



fh = open(sys.argv[1],'r');#sys.stdin;
initialState = state(fh, sys.argv[2]);

solution = General_Search(initialState);
print(solution.allOpsToThis());

print('problem solved?: %s'%solution.goalAchieved());

