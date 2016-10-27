

class DefaultHeuristic:
    def HeuristicPrep(self, State):
        pass;
        
    def HCost(self, State):
        return 0;

class genericState:
    
    #the parent to this node. Made in copy function. Not represented due to recursion.
    parent = None;
    
    GCost = 0;
    HeuristicObj = DefaultHeuristic(); #Same as having no heuristic
    
    #Abstract function to get the current branch of the node tree
    def allOpsToThis(self):
        pass;
    
    #Abstract function to copy a node
    def copy(self):
        pass;
    
    #Abstract function to apply an abstract operation    
    def applyOp(self, op):
        pass;
        
    #Abstract function that returns a list of all possible abstract operations
    def possibleOps(self):
        pass;
        
    #Creates a list of all the possible children states for this state
    #This does not depend on the implementation of the problem
    def expandState(self): 
        AllOps = self.possibleOps();
        ChildStates = [];
         
        for i in range(0,len(AllOps)):
            newState = self.copy();
            newState.applyOp(AllOps[i]);
            ChildStates.append(newState);
        
        return ChildStates;
    
    #Abstract function that determines whether the goal has been achieved
    def goalAchieved(self):
        pass;
        
    #F Function is domain-independent
    #Here we use the A* F function, g(n)+h(n)
    def FFunction(self):
        return self.GCost + self.HeuristicObj.HCost(self);
