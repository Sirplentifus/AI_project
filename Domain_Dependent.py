import copy

class cask: #describes a cask
    
    def __init__(self, newLength=0, newWeight=0):
        self.Length = newLength;
        self.Weight = newWeight;
        
    def __repr__(self):
        return '<Length: %d, Weight: %g>'%(self.Length, self.Weight);

class stack: #Describes a stack and the IDs of the casks it contains
    
    def __init__(self, newMaxLength):
        self.MaxLength = newMaxLength;
        self.LeftOverLength = newMaxLength;
        self.Casks = []; #List of cask IDs
        
    def __repr__(self):
        return'<MaxLength: %d, LeftOverLength: %d, Casks: %s>\n'%(self.MaxLength, self.LeftOverLength, self.Casks);
        
    #Checks if the 2 stacks contain the same casks
    def __eq__(self, other):
        return self.Casks == other.Casks;
        
class operation: #describes any valid state changing operation
    
    def __init__(self, newOpType='', newDest = -1):
        self.OpType = newOpType; #Describes the type of operation. Can be 'MOVE', 'LOAD' or 'UNLOAD'
        self.Dest = newDest; #Index of the edge we are to move along. Only used if OpType is 'MOVE'
        
    def __repr__(self):
        return '<OpType: %s, Dest: %d>'%(self.OpType, self.Dest);

class edgeTo: #represents a connection. Only makes sense when a member of a map node
    def __init__(self, newIDto='', newLength=0):
        self.IDto = newIDto;
        self.Length = newLength;
        
    def __repr__(self):
        return '<IDto: %s, Length: %g>'%(self.IDto, self.Length);


class state:
    CasksProps = dict(); #dictionary with all the casks' properties, indexed by their ID strings
    Stacks = dict(); #dictionary of all the stacks indexed by their ID strings
    World = dict(); #Has all the nodes (including stacks) that exist in the form of edgeTo lists
    
    RobotPosition = 'EXIT';
    RobotCask = ''; #Empty string denotes lack of cask
    
    GoalCask = ''; #Cask that is to be moved to EXIT node
    OpToThis = operation(); #Operation that went from father state to this state - POSSIBLY USELESS
    OpToThis_str = '';#Operation that went from father state to this state in a form that is more readable and compatible with the output format
    
    parent = None; #the parent to this node. Made in copy function. Not represented due to recursivity.
    
    GCost = 0;
    
    #initializes from file if a file_handle is specified
    def __init__(self, fileHandle=None, GoalCask=''):
        if(fileHandle==None or GoalCask==''):
            return;
            
        while(1):
            line_str=fileHandle.readline();
            params = line_str.split();
            if(len(line_str) == 0):
                print('Finished reading\n');
                break;
            if(line_str.isspace()):
                continue;
            elif(line_str[0] == 'C'):
                self.CasksProps[params[0]] = cask(int(params[1]), float(params[2]));
            elif(line_str[0] == 'S'):
                S = stack(int(params[1]));
                self.Stacks[params[0]] = S;
                
                for i in range(2, len(params)):
                    self.insertToStack(params[0], params[i]);
                
                
            elif(line_str[0] == 'E'):
                NodeLeftID = params[1];
                NodeRightID = params[2];
                Cost = float(params[3]);
                
                EdgeToRight = edgeTo(NodeRightID, Cost);
                EdgeToLeft = edgeTo(NodeLeftID, Cost);
                
                NodeLeft = self.World.setdefault(NodeLeftID, []);
                NodeLeft.append(EdgeToRight);
                
                NodeRight = self.World.setdefault(NodeRightID, []);
                NodeRight.append(EdgeToLeft);
                
            else:
                continue; #project description says that "All other lines should be ignored"
        
        self.GoalCask = GoalCask;
        
        if(self.CasksProps.get(self.GoalCask) == None):
            raise(ValueError('The cask to be retireved isn\'t present in the world'));
    
    def __repr__(self):
        return'<RobotPosition:%s,\n RobotCask:%s,\n OpToThis: %s,\n GCost: %g,\n Stacks: %s>'%(self.RobotPosition, self.RobotCask, self.OpToThis_str, self.GCost, self.Stacks);
    
    def copy(self):
        ret = state();
        ret.RobotPosition = self.RobotPosition
        ret.RobotCask = self.RobotCask;
        ret.Stacks = copy.deepcopy(self.Stacks); #stacks vary from state to state, so they're deeply copied
        ret.CasksProps = self.CasksProps; #copied by reference
        ret.World = self.World; #Copied by reference
        ret.GoalCask = self.GoalCask;
        ret.OpToThis = self.OpToThis;
        ret.parent = self; #Setting the reference to the new state's parent
        ret.GCost = self.GCost;
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
            
            self.OpToThis_str = 'move %s '%(self.RobotPosition)
            DestinationEdge = (self.World[self.RobotPosition])[op.Dest];
            self.RobotPosition = DestinationEdge.IDto;
            
            if(self.RobotCask):
                OpCost = 1 + self.CasksProps[self.RobotCask].Weight;
            else:
                OpCost = 1;    
            OpCost = OpCost*DestinationEdge.Length;
            
            self.OpToThis_str = self.OpToThis_str + '%s %g'%(self.RobotPosition, OpCost);
        elif(op.OpType == 'LOAD'):
            if(self.RobotPosition[0] != 'S'):
                raise(ValueError('Invalid op - cannot load while not on a stack node'));
                            
            if(self.RobotCask):
                raise(ValueError('Invalid op - cannot load while carrying a cask'));
                
            self.RobotCask = self.removeFromStack(self.RobotPosition);
            OpCost = 1 + self.CasksProps[self.RobotCask].Weight;
            self.OpToThis_str = 'load %s %s %g'%(self.RobotCask, self.RobotPosition, OpCost);
            
        elif(op.OpType == 'UNLOAD'):
            if(self.RobotPosition[0] != 'S'):
                raise(ValueError('Invalid op - cannot unload while not on a stack node'));
            
            if(not self.RobotCask):
                raise(ValueError('Invalid op - cannot unload while not carrying any cask'));
            
            OpCost = 1 + self.CasksProps[self.RobotCask].Weight;
            self.OpToThis_str = 'unload %s %s %g'%(self.RobotCask, self.RobotPosition, OpCost);    
            self.insertToStack(self.RobotPosition, self.RobotCask);
            self.RobotCask = '';
            
        else:
            raise(ValueError('Invalid op - invalid OpType'));
        
        self.OpToThis = op;
        self.GCost = self.GCost+OpCost;
                        
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
        
    #Checks if two states are the same. Note that a state's parent, Gcost, OpToThis and other things are irrelevant.
    #All that matters for this comparison is if the stacks have the same casks in the same order (this implies the robotCask is the same), and if the robot is in the same position
    def __eq__(self, other):
        return (self.Stacks==other.Stacks) and (self.RobotPosition==other.RobotPosition);

#The following function is just a convenience for testing, and should not be used by the problem solving algortihm
#It moves to a specified Node destination. If it's not possible to go there, an exception will be raised of "the index out of bounds" kind
def MoveTo(AffectedState, Destination):
    possible_edges = AffectedState.World[AffectedState.RobotPosition];
    OpDest = [i for i in range(0,len(possible_edges)) if possible_edges[i].IDto == Destination]
    AffectedState.applyOp(operation('MOVE', OpDest[0]));
