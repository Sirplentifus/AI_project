import copy

class cask: #describes a cask
    
    def __init__(self, newLength=0, newWeight=0):
        self.Length = newLength;
        self.Weight = newWeight;
        
    def __repr__(self):
        return '<Length: %d, Weight: %.1f>'%(self.Length, self.Weight);

class stack: #Describes a stack and the IDs of the casks it contains
    
    def __init__(self, newMaxLength):
        self.MaxLength = newMaxLength;
        self.LeftOverLength = newMaxLength;
        self.Casks = []; #List of cask IDs
        
    def __repr__(self):
        return'<MaxLength: %d, LeftOverLength: %d, Casks: %s>\n'%(self.MaxLength, self.LeftOverLength, self.Casks);
        
class operation: #describes any valid change changing operation
    
    def __init__(self, newOpType='', newDest = -1):
        self.OpType = newOpType; #Describes the type of operation. Can be 'MOVE', 'LOAD' or 'UNLOAD'
        self.Dest = newDest; #Index of the edge we are to move along. Only used if OpType is 'MOVE'
        
    def __repr__(self):
        return '<OpType: %s, Dest: %d>'%(self.OpType, self.Dest);

class edgeTo: #represents a connection. Only makes sense when a member of a map node
    def __init__(self, newIDto='', newCost=0):
        self.IDto = newIDto;
        self.Cost = newCost;
        
    def __repr__(self):
        return '<IDto: %s, Cost: %.1f>'%(self.IDto, self.Cost);


class state:
    CasksProps = dict(); #dictionary with all the casks' properties, indexed by their ID strings
    Stacks = dict(); #dictionary of all the stacks indexed by their ID strings
    World = dict(); #Has all the nodes (including stacks) that exist in the form of edgeTo lists
    
    RobotPosition = 'EXIT';
    RobotCask = ''; #Empty string denotes lack of cask
    
    GoalCask = ''; #Cask that is to be moved to EXIT node
    OpToThis = operation(); #Operation that went from father state to this state
    
    GCost = 0;
    
    def __repr__(self):
        return'<RobotPosition:%s,\nRobotCask:%s,\n Stacks: %s>'%(self.RobotPosition, self.RobotCask, self.Stacks);
    
    def copy(self):
        ret = state();
        ret.RobotPosition = self.RobotPosition
        ret.RobotCask = self.RobotCask;
        ret.Stacks = copy.deepcopy(self.Stacks);
        ret.World = self.World; #Copied by reference
        ret.GoalCask = self.GoalCask;
        ret.OpToThis = self.OpToThis;
        return ret;
        
    def insertToStack(self, StackID, CaskID): #Insert a cask to a stack. Raises exception if it doesn't fit
        C = self.CasksProps[CaskID];
        S = self.Stacks[StackID];
        
        if(S.LeftOverLength < C.Length):
            raise(ValueError('Stack cannot fit this cask'));
            return;
            
        S.LeftOverLength = S.LeftOverLength - C.Length;
        S.Casks.append(CaskID);
    
    def removeFromStack(self, StackID): #removes a cask from a stack, and returns its ID string. Raises exception if it's empty
        S = self.Stacks[StackID];
        
        if(not S.Casks):
            raise(ValueError('Stack is empty'));
        
        CaskID = S.Casks.pop();
        C = self.CasksProps[CaskID];
        
        S.LeftOverLength = S.LeftOverLength + C.Length;
        
        return CaskID;
        
    def applyOp(self, op): #Applies an operation to a state. Raises exception if it's not a valid operation.
        if(op.OpType == 'MOVE'):
            moveInd = op.Dest;
            if(moveInd<0 or moveInd>=len(self.World[self.RobotPosition])):
                raise(ValueError('Invalid op - invalid op.Dest'));
            
            DestinationEdge = (self.World[self.RobotPosition])[op.Dest];
            self.RobotPosition = DestinationEdge.IDto;
        elif(op.OpType == 'LOAD'):
            if(self.RobotPosition[0] != 'S'):
                raise(ValueError('Invalid op - cannot load while not on a stack node'));
                            
            if(self.RobotCask):
                raise(ValueError('Invalid op - cannot load while carrying a cask'));
                
            self.RobotCask = self.removeFromStack(self.RobotPosition);    
            
        elif(op.OpType == 'UNLOAD'):
            if(self.RobotPosition[0] != 'S'):
                raise(ValueError('Invalid op - cannot unload while not on a stack node'));
            
            if(not self.RobotCask):
                raise(ValueError('Invalid op - cannot unload while not carrying any cask'));
                
            self.insertToStack(self.RobotPosition, self.RobotCask);
            self.RobotCask = '';
            
        else:
            raise(ValueError('Invalid op - invalid OpType'));
            
    def possibleOps(self): #Returns a list of all the possible operations in this state
        EdgeList = self.World[self.RobotPosition];
        N = len(EdgeList);
        ret = [];
        for i in range(0,N):
            ret.append(operation('MOVE', i));
        
        if(self.RobotPosition[0] == 'S'):
            if(self.RobotCask and self.Stacks[self.RobotPosition].LeftOverLength >= self.CasksProps[self.RobotCask].Length):
                ret.append(operation('UNLOAD'));
            elif(self.Stacks[self.RobotPosition].Casks and not self.RobotCask):
                ret.append(operation('LOAD'));
        
        return ret;
        
    def expandState(self): #Creates a list of all the possible children states for this state
        AllOps = self.possibleOps();
        ChildStates = [];
         
        for i in range(0,len(AllOps)):
            newState = self.copy();
            newState.applyOp(AllOps[i]);
            ChildStates.append(newState);
        return ChildStates;
    
    def goalAchieved(self): #Returns true if the goal (moving GoalCask to 'EXIT' node) has been achieved and false otherwise
        return (self.RobotPosition=='EXIT' and self.RobotCask==self.GoalCask);

#The following function is just a convenience for testing, and should not be used by the problem solving algortihm
#It moves to a specified Node destination. If it's not possible to go there, an exception will be raised of "the index out of bounds" kind
def MoveTo(AffectedState, Destination):
    possible_edges = AffectedState.World[AffectedState.RobotPosition];
    OpDest = [i for i in range(0,len(possible_edges)) if possible_edges[i].IDto == Destination]
    AffectedState.applyOp(operation('MOVE', OpDest[0]));
