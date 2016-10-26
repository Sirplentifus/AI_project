from Domain_Dependent import *;
import pdb; #To use for debugging

#Solves the problem using an uninformed uniform cost search - always expanding the lowest cost node
def General_Search(start_node):
    frontier = [start_node];
    explored = [];
    
    while(1):
        assert frontier;
        frontier = sorted(frontier, key = lambda node: node.FFunction(), reverse = True);
        node = frontier.pop();
        #~ pdb.set_trace();
        if(node.goalAchieved()):
            return node;
        explored.append(node);
        nodeChildren = node.expandState();
        for nodeChild in nodeChildren:
            
            #Checking that the child node was not already explored, and skipping if it was
            matches = [x for x in explored if x==nodeChild];
            if(matches):
                continue;
                
            #Checking if the child node is in the frontier, in which case the node with the lowest GCost is kept there
            matches = [x for x in frontier if x==nodeChild];
            if(matches):
                matches.append(nodeChild);
                lowestCostNode = min(matches, key = lambda node: node.FFunction());
                
                for x in matches:
                    if(x != lowestCostNode):
                        frontier.remove(x);
                
            else:
                frontier.append(nodeChild);
