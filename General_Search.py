from Domain_Dependent import *;
#~ import pdb; #To use for debugging


#Solves the problem using an uninformed uniform cost search - always expanding the lowest cost node
def General_Search(start_node):
    frontier = [start_node];
    explored = [];
    
    
    while(True):
        assert frontier;
        
        #Get the node with the lowest F cost... 
        node = min(frontier, key = lambda node: node.FFunction());
        #...and remove it from the frontier
        frontier.remove(node);
        #~ pdb.set_trace();

        if(node.goalAchieved()):
            #~ print('\nNumber of nodes created: %d\n'%( len(explored) + len(frontier) + 1));
            return node;
        #Add current node to explored nodes list
        explored.append(node);
        nodeChildren = node.expandState();
        for nodeChild in nodeChildren:
            
            #Check that the child node was not already explored, and skip it if it was
            matches = [x for x in explored if x==nodeChild];
            if(matches):
                continue;
                
            #Checking if the child node is in the frontier, in which case the node with the lowest GCost is kept there
            matches = [x for x in frontier if x==nodeChild];
            if(matches):
                if(len(matches) > 1):
                    raise(ValueError('Multiple matches in frontier - this should not be possible'));
                
                match = matches[0];
                frontier.remove(match);
                
                lowestCostNode = min([match, nodeChild], key = lambda node: node.FFunction());
                
                frontier.append(lowestCostNode);

                
            else:
                frontier.append(nodeChild);
    
