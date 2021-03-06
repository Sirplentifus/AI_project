#~ import pdb;


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
            HCost +=  (1 + State.CasksProps[Cid].Weight)*2;
        
        if(GoalCaskMoved):
            raise(ValueError('The goal cask was moved to a different stack - this should not have happened'));

        return HCost;
    
    def HCost(self, State):
        return self.HCost_CaskPart(State);

class GhostRobotHeuristic(TeleportingRobotHeuristic):
        
    ShortestCostsToStacks = dict();
    ShortestCostsToEXIT = dict();
    
    #Returns a dictionary with the lowest cost to go from each map node (indexing the dictionary) to MapNode
    #Performs something similar to a uniform cost search, but on the map nodes
    def GetLowestCosts(self, State, MapNode):
        ShortestCostsToMapNode = dict();
        
        #~ pdb.set_trace();
        
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
            
        self.ShortestCostsToEXIT = self.GetLowestCosts(State, 'EXIT');
    
    def HCost_MovementPart(self, State):
        
        HCost = 0;
        #~ pdb.set_trace();
        
        #If a robot is not carrying any cask, it will eventually have to go to the 
        #stack which has the goal stack. The minimum possible cost for this is computed
        if(not State.RobotCask):
            HCost += self.ShortestCostsToStacks[self.StackWithGoalCask][State.RobotPosition];
        
        
        if(State.RobotCask == State.GoalCask):
            #If the robot is carrying the goal cask, it will have to go to EXIT. No other action makes sense, so the minimum cost to EXIT is computed.
            HCost += self.ShortestCostsToEXIT[State.RobotPosition]*(1+State.CasksProps[State.GoalCask].Weight);
        else:
            #If the robot is carryng another cask, or no cask, it will eventually have to carry the GoalCask to the EXIT, so this cost is computed.
            HCost += self.ShortestCostsToEXIT[self.StackWithGoalCask]*(1+State.CasksProps[State.GoalCask].Weight);
            
        
        return HCost;
            
    
    def HCost(self, State):
        HCost = self.HCost_CaskPart(State);
        HCost += self.HCost_MovementPart(State);
        return HCost;

class InfiniteStacksHeuristic(GhostRobotHeuristic):
    
    StackClosestToGoalStack = '';
    
    #Redefining this function to also find the StackClosestToGoalStack
    def HeuristicPrep(self, State):
        self.HeuristicPrep_CaskPart(State);
        
        
        for Sid in State.Stacks:
            self.ShortestCostsToStacks[Sid] = self.GetLowestCosts(State, Sid);
        
        
        for Sid in State.Stacks:
            if(not self.StackClosestToGoalStack or (Sid!=self.StackWithGoalCask \
                and self.ShortestCostsToStacks[Sid][self.StackWithGoalCask] <  \
                self.ShortestCostsToStacks[self.StackClosestToGoalStack][self.StackWithGoalCask])):
                
                self.StackClosestToGoalStack = Sid;
        
        #~ pdb.set_trace();    
            
        self.ShortestCostsToEXIT = self.GetLowestCosts(State, 'EXIT');
        
        
    
    #Redefining this function to include cost of taking the casks above GoalCask to the nearest stack
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
        #plus the cost of moving them to the nearest stack
        GoalCaskMoved = True;
        for Cid in reversed(State.Stacks[self.StackWithGoalCask].Casks):
            if(Cid == State.GoalCask):
                GoalCaskMoved = False;
                break;
            
            #This is the part that is different in this heuristic:
            HCost += (1 + State.CasksProps[Cid].Weight)* \
                (2 + self.ShortestCostsToStacks[self.StackWithGoalCask][self.StackClosestToGoalStack]);
            #    ^- Loading & Unloading                 ^ 
            #      Carrying (movement) the casks from the StackWithGoalCask to the StackClosestToGoalStack
            
            HCost += self.ShortestCostsToStacks[self.StackWithGoalCask][self.StackClosestToGoalStack];
            #     ^- Moving back from the StackClosestToGoalStack to the StackWithGoalCask
            
        if(GoalCaskMoved):
            raise(ValueError('The goal cask was moved to a different stack - this should not have happened'));

        return HCost;
        
    

