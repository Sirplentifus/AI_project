#No object has its own ID because I say so

class cask:
    
    def __init__(self, newLength=0, newWeight=0):
        self.Length = newLength;
        self.Weight = newWeight;
        
    def __repr__(self):
        return '{Length: %d, Weight: %d}'%(self.Length, self.Weight);

class stack: #to be used as a C like structure
    def __init__(self, newMaxLength):
        self.MaxLength = newMaxLength;
        self.LeftOverLength = newMaxLength;
        self.Casks = []; #List of cask IDs
        
    def __repr__(self):
        return'{MaxLength: %d, LeftOverLength: %d, Casks: %s}\n'%(self.MaxLength, self.LeftOverLength, self.Casks);

CaskDict = dict(); #dictionary with all the casks, indexed by their ID strings

class state:
    Stacks = dict(); #dictionary of all the stacks indexed by their ID strings
    
    def __repr__(self):
        return'{Stacks: %s}'%(self.Stacks);
        
    def insertToStack(self, StackID, CaskID):
        C = CaskDict[CaskID];
        S = self.Stacks[StackID];
        
        if(S.LeftOverLength < C.Length):
            raise(ValueError('Stack cannot fit this cask'));
            return;
            
        S.LeftOverLength = S.LeftOverLength - C.Length;
        S.Casks.append(CaskID);

class edgeTo: #represents a connection. Only makes sense when a member of a mapNode
    def __init__(self, newIDto='', newCost=0):
        self.IDto = newIDto;
        self.Cost = newCost;
        
    def __repr__(self):
        return '{IDto: %s, Cost: %d'%(self.IDto, self-Cost);
    
class mapNode:    
    Connections = []; #list of edgeTo objects

World = dict(); #Has all the nodes (including stacks) that exist in the form of mapNode objects
