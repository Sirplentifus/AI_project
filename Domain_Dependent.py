import copy
from Domain_Independent import *;

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

class state(genericState):
    CasksProps = dict(); #dictionary with all the casks' properties, indexed by their ID strings
    Stacks = dict(); #dictionary of all the stacks indexed by their ID strings
    World = dict(); #Has all the nodes (including stacks) that exist in the form of edgeTo lists
    
    RobotPosition = 'EXIT';
    RobotCask = ''; #Empty string denotes lack of cask
    
    GoalCask = ''; #Cask that is to be moved to EXIT node
    OpToThis = operation(); #Operation that went from father state to this state - POSSIBLY USELESS
    OpToThis_str = '';#Operation that went from father state to this state in a form that is more readable and compatible with the output format
    
     
    
    
    
    
    #initializes from file if a file_handle is specified
    def __init__(self, fileHandle=None, GoalCask='', newHeuristicObj = DefaultHeuristic()):
        if(fileHandle==None or GoalCask==''):
            return;
            
        while(1):
            line_str=fileHandle.readline();
            params = line_str.split();
            if(len(line_str) == 0):
                break;
            if(line_str.isspace()):
                continue;
            elif(line_str[0] == 'C'):
                self.CasksProps[params[0]] = cask(int(params[1]), float(params[2]));
            elif(line_str[0] == 'S'):
                S = stack(int(params[1]));
                self.Stacks[params[0]] = S;
                self.World.setdefault(params[0], []);
                
                for i in range(2, len(params)):
                    S.Casks.append(params[i]); #LeftOverLength's for all stacks have to be updated later
                    #self.insertToStack(params[0], params[i]); #Can't use this - makes errors if casks appear after stacks in which they are
                
                
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
        
        #initializing the heuristic
        self.HeuristicObj = newHeuristicObj;
        self.HeuristicObj.HeuristicPrep(self);
        
        #In the following lines of code, certain conditions are checked for.
        #Situations that make the problem unsolvable raise exceptions, while situations that are just strange raise warnings.
        #A problem can still be unsolvable and raise no exceptions nor warnings. Exemples are:
        #   The cask to be retrieved in in a sub-graph that does not connect to the EXIT node
        #   The casks above the cask to be retrieved cannot fit in any way in the remaining stacks
        
        #Checking if the cask to retrieve is in one of the stacks
        CaskInWorld = False;
        for Sid in self.Stacks:
            S = self.Stacks[Sid];
            if( [x for x in S.Casks if x == self.GoalCask] ):
                CaskInWorld = True;
                break;
        if(not CaskInWorld):
            raise(ValueError('The cask to be retrieved isn\'t in any of the stacks'));
        
        #Checking if the cask to retrieve has its propreties defined
        if(self.CasksProps.get(self.GoalCask) == None):
            raise(ValueError('The cask to be retrieved isn\'t wasn\'t defined'));
        
        #Checking if the stacks are connected to some other node. If an unconnected node is found, a warning is printed, unless it contains the goalCask, in which case an exception is raised.
        for Sid in self.Stacks:
            if( not self.World.get(Sid) ):
                if( self.Stacks[Sid].Casks.count(self.GoalCask) == 1 ):
                    raise(ValueError('The cask to be retrieved is in an unconnected stack'));
                else:
                    print('Warning - At least one of the stacks is not connected to any node');
                break;
            
        #Computing LeftOverLength for all the stacks
        for Sid in self.Stacks:
            S = self.Stacks[Sid];
            for Cid in S.Casks:
                S.LeftOverLength = S.LeftOverLength - self.CasksProps[Cid].Length;
            if(S.LeftOverLength < 0):
                raise(ValueError('At least one of the stacks was initialized with casks that don\'t fit in it'));
                
        #~ print('Starting node heuristic: %g'%self.HeuristicObj.HCost(self));
            
    def __repr__(self):
        HCost = self.HeuristicObj.HCost(self);
        return'<RobotPosition:%s,\n RobotCask:%s,\n OpToThis: %s,\n GCost: %g, HCost: %g, FCost: %g\n Stacks: %s>'%(self.RobotPosition, self.RobotCask, self.OpToThis_str, self.GCost, HCost, self.FFunction(), self.Stacks);
    
    #Implements abstract function to get the current branch of the node tree
    def allOpsToThis(self): #Returns a string which represents all the operations that lead to this node, from the initial state (marked has having OpToThis_str as an empty string)
        this_node = self;
        ret = '%g\n'%this_node.GCost;
        
        while(this_node.OpToThis_str):
            ret = this_node.OpToThis_str + '\n' + ret;
            this_node = this_node.parent;
            
        return ret;
    
    #Implements abstract function to copy a node
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
        ret.HeuristicObj = self.HeuristicObj
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
        
    #Implements abstract function to apply an abstract operation
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
<<<<<<< HEAD
    
    #Returns a list of all the possible operations in this state
    #If the robot is carrying the goal cask, it is never advantageous to
    #unload it, so this operation was BANNED
    def possibleOps(self): 
=======
                        
    #Implements abstract function that returns a list of all possible abstract operations
    def possibleOps(self): #Returns a list of all the possible operations in this state
>>>>>>> cd3cc0fca5e9c296772bb07267a7c7464d20875b
        EdgeList = self.World[self.RobotPosition];
        N = len(EdgeList);
        ret = [];
        for i in range(0,N):
            ret.append(operation('MOVE', i));
        
        
        if(self.RobotPosition[0] == 'S'):
            if(self.RobotCask and self.Stacks[self.RobotPosition].LeftOverLength >= self.CasksProps[self.RobotCask].Length and self.RobotCask!=self.GoalCask):
                ret.append(operation('UNLOAD'));
            elif(self.Stacks[self.RobotPosition].Casks and not self.RobotCask):
                ret.append(operation('LOAD'));
        
        return ret;
    
    #Implements abstract function that determines whether the goal has been achieved
    def goalAchieved(self): #Returns true if the goal (moving GoalCask to 'EXIT' node) has been achieved and false otherwise
        return (self.RobotPosition=='EXIT' and self.RobotCask==self.GoalCask);
        
    #Checks if two states are the same. Note that a state's parent, Gcost, OpToThis and other things are irrelevant.
    #All that matters for this comparison is if the stacks have the same casks in the same order (this implies the robotCask is the same), and if the robot is in the same position
    def __eq__(self, other):
        return (self.Stacks==other.Stacks) and (self.RobotPosition==other.RobotPosition);
    
    
#TODO REMOVE
#The following function is just a convenience for testing, and should not be used by the problem solving algortihm
#It moves to a specified Node destination. If it's not possible to go there, an exception will be raised of "the index out of bounds" kind
def MoveTo(FirstState, Destination):
    AffectedState = FirstState.copy();
    
    if(Destination == 'LOAD'):
        AffectedState.applyOp(operation('LOAD'));
    elif(Destination == 'UNLOAD'):
        AffectedState.applyOp(operation('UNLOAD'));
    else:
        possible_edges = AffectedState.World[AffectedState.RobotPosition];
        OpDest = [i for i in range(0,len(possible_edges)) if possible_edges[i].IDto == Destination]
        AffectedState.applyOp(operation('MOVE', OpDest[0]));
        
    return AffectedState;
