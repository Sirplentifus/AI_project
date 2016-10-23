import sys;

from Domain_Dependent import *;
from General_Search import *;

class TeleportingRobotHeuristic:
    
    StackWithGoalCask = '';
    
    #All we need to do is figure out where the Goal Cask is
    
    def HeuristicPrep(self, State):
        
        for Sid in State.Stacks:
            if( State.Stacks[Sid].Casks.count(State.GoalCask) == 1 ):
                self.StackWithGoalCask = Sid;
                return;
        
    #Cost of all the loadings and unloading that have to be done
    def HCost(self, State):
        
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
        for Cid in reversed(State.Stacks[self.StackWithGoalCask].Casks):
            if(Cid == State.GoalCask):
                break;
            HCost = HCost + (1 + State.CasksProps[Cid].Weight)*2;
    
        
        return HCost;


fh = open(sys.argv[1],'r');

initialState = state(fh, sys.argv[2], TeleportingRobotHeuristic());
solution = General_Search(initialState);

print(solution.allOpsToThis());
print('problem solved?: %s'%solution.goalAchieved());
