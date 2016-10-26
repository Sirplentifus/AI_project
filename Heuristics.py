import pdb;


class TeleportingRobotHeuristic:
    
    StackWithGoalCask = '';
    
    #All we need to do is figure out where the Goal Cask is
    def HeuristicPrep_CaskPart(self, State):
        for Sid in State.Stacks:
            if( State.Stacks[Sid].Casks.count(State.GoalCask) == 1 ):
                self.StackWithGoalCask = Sid;
                return;
    
    def HeuristicPrep(self, State):
        self.HeuristicPrep_CaskPart(State);
        
    #Cost of all the loadings and unloadings that have to be done
    def HCost_CaskPart(self, State):
        
        HCost = 0;
        
        #If current cask is GoalCask, return 0
        if(State.RobotCask == State.GoalCask):
            return 0;
        #If we're carrying any other goal cask, we will have to unload it eventually
        elif(State.RobotCask):
            HCost = 1 + State.CasksProps[State.RobotCask].Weight;
        
        #Cost of loading the Goal cask
        HCost = HCost + 1 + State.CasksProps[State.GoalCask].Weight;
        
        #Cost of loading and unloading all the casks above the GoalCask in the Stack with the Goal Cask
        GoalCaskMoved = True;
        for Cid in reversed(State.Stacks[self.StackWithGoalCask].Casks):
            if(Cid == State.GoalCask):
                GoalCaskMoved = False;
                break;
            HCost = HCost + (1 + State.CasksProps[Cid].Weight)*2;
        
        if(GoalCaskMoved):
            raise(ValueError('The goal cask was moved to a different stack - this should not have happened'));

        return HCost;
    
    def HCost(self, State):
        return self.HCost_CaskPart(State);



class InfiniteStacksHeuristic(TeleportingRobotHeuristic):
    
    ShortestCostsToStacks = dict();
    ShortestCostsToEXIT = dict();
    
    #Returns a dictionary with the lowest gost to go from each map node (indexing the dictionary) to MapNode
    #Performs something similar to a uniform cost search
    def GetLowestCosts(self, State, MapNode):
        ShortestCostsToMapNode = dict();
        
        pdb.set_trace();
        
        for node in State.World:
            ShortestCostsToMapNode[node] = float('inf');
        
        ShortestCostsToMapNode[MapNode] = 0;
        
        frontier = [MapNode];
        #No need for explored list
        
        while(frontier):        
            
            node = min(frontier, key = lambda node: ShortestCostsToMapNode[node] );
            frontier.remove(node);
            
            GCost = ShortestCostsToMapNode[node];
            if(GCost == float('inf')):
                raise(ValueError('GCost equaling infinity was expanded (Shouldn\'t be possible)'));
            
            Edges = State.World[node];
            
            for edge in Edges:
                ChildID = edge.IDto;
                ChildGCost = GCost + edge.Length;
                
                #If this GCost is lower than the one already computed, use this one, and put this node in the frontier
                if(ChildGCost < ShortestCostsToMapNode[ChildID]):
                    frontier.append(ChildID);
                    ShortestCostsToMapNode[ChildID] = ChildGCost;
                
        return ShortestCostsToMapNode;
        
    
    def HeuristicPrep(self, State):
        self.HeuristicPrep_CaskPart(State);
        
        for Sid in State.Stacks:
            self.ShortestCostsToStacks[Sid] = self.GetLowestCosts(State, Sid);
            
        ShortestCostsToEXIT = self.GetLowestCosts(State, 'EXIT');
        
    def HCost(self, State):
        HCost = self.HCost_CaskPart(State);
        
        return HCost;
        
    

