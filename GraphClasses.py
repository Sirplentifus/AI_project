#No object has its own ID because I say so

import copy

class cask:
    
    def __init__(self, newLength=0, newWeight=0):
        self.Length = newLength;
        self.Weight = newWeight;
        
    def __repr__(self):
        return '<Length: %d, Weight: %.1f>'%(self.Length, self.Weight);

CaskDict = dict(); #dictionary with all the casks, indexed by their ID strings

class stack: #to be used as a C like structure
    
    def __init__(self, newMaxLength):
        self.MaxLength = newMaxLength;
        self.LeftOverLength = newMaxLength;
        self.Casks = []; #List of cask IDs
        
    def __repr__(self):
        return'<MaxLength: %d, LeftOverLength: %d, Casks: %s>\n'%(self.MaxLength, self.LeftOverLength, self.Casks);
        
class operation:
    
    def __init__(self, newOpType='', newDest = -1):
        self.OpType = newOpType;
        self.Dest = newDest;
        
    def __repr__(self):
        return '<OpType: %s, Dest: %d>'%(self.OpType, self.Dest);

class edgeTo: #represents a connection. Only makes sense when a member of a map node
    def __init__(self, newIDto='', newCost=0):
        self.IDto = newIDto;
        self.Cost = newCost;
        
    def __repr__(self):
        return '<IDto: %s, Cost: %.1f>'%(self.IDto, self.Cost);


class state:
    Stacks = dict(); #dictionary of all the stacks indexed by their ID strings
    World = dict(); #Has all the nodes (including stacks) that exist in the form of edgeTo lists
    
    RobotPosition = 'EXIT';
    RobotCask = '';
    
    GCost = 0;
    
    def __repr__(self):
        return'<RobotPosition:%s,\nRobotCask:%s,\n Stacks: %s>'%(self.RobotPosition, self.RobotCask, self.Stacks);
        
    def insertToStack(self, StackID, CaskID):
        C = CaskDict[CaskID];
        S = self.Stacks[StackID];
        
        if(S.LeftOverLength < C.Length):
            raise(ValueError('Stack cannot fit this cask'));
            return;
            
        S.LeftOverLength = S.LeftOverLength - C.Length;
        S.Casks.append(CaskID);
        
    def copy(self):
        ret = state();
        ret.RobotPosition = self.RobotPosition
        ret.RobotCask = self.RobotCask;
        ret.Stacks = copy.deepcopy(self.Stacks);
        ret.World = self.World; #Copied by reference
        return ret;
        
    def applyOp(self, op):
        if(op.OpType == 'MOVE'):
            moveInd = op.Dest;
            if(moveInd<0 or moveInd>=len(self.World[self.RobotPosition])):
                raise(ValueError('Operação inválida - op.Dest inválido'));
            
            DestinationEdge = (self.World[self.RobotPosition])[op.Dest];
            self.RobotPosition = DestinationEdge.IDto;
        #elif(op.OpType == 'LOAD'):
        else:
            raise(ValueError('Operação inválida - OpType inválido'));
            
    def possibleOps(self):
        EdgeList = self.World[self.RobotPosition];
        N = len(EdgeList);
        ret = [];
        for i in range(0,N):
            ret.append(operation('MOVE', i));
        
        return ret;
            


