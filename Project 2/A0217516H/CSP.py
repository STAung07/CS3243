import random
import sys
import heapq
import time

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# Helper functions to aid in your implementation. Can edit/remove
class Piece:
    # type attribute
    type = ""

    def __init__(self, pieceType):
        self.type = pieceType
    
    def getType(self):
        if self.type == "Rook":
            return "R"
        elif self.type == "Bishop":
            return "B"
        elif self.type == "Knight":
            return "N"
        elif self.type == "Queen":
            return "Q"
        else:
            return "K"

    # reachable_states method for each piece type => for enemy pieces
    def getPiecePath(self, currPosCol, currPosRow, board):
        if self.type == "Rook":
            return self.getRookPath(currPosCol, currPosRow, board)
        elif self.type == "Bishop":
            return self.getBishopPath(currPosCol, currPosRow, board)
        elif self.type == "Knight":
            return self.getKnightPath(currPosCol, currPosRow, board)
        elif self.type == "Queen":
            return self.getQueenPath(currPosCol, currPosRow, board)
        else:
            return self.getKingPath(currPosCol, currPosRow, board)

    # returns list of positions threatened by curr piece
    def getRookPath(self, currPosCol, currPosRow, board):
        threatList = [] # list of tuples of Positions threatened
        # check top
        r = currPosRow
        while (currPosCol,r+1) in board:
            r = r+1
            if not self.isObstacle((currPosCol, r), board):
                threatList.append((currPosCol, r))
            else:
                break
        # check down
        r = currPosRow
        while (currPosCol,r-1) in board:
            r = r-1
            if not self.isObstacle((currPosCol, r), board):
                threatList.append((currPosCol, r))
            else:
                break
        # check right
        c = currPosCol
        while (self.getNextCol(c, 1), currPosRow) in board:
            c = self.getNextCol(c, 1)
            if not self.isObstacle((c, currPosRow), board):
                threatList.append((c, currPosRow))
            else: 
                break
        # check left
        c = currPosCol
        while (self.getPrevCol(c, 1), currPosRow) in board:
            c = self.getPrevCol(c, 1)
            if not self.isObstacle((c, currPosRow), board):
                threatList.append((c, currPosRow))
            else: 
                break
        return threatList

    def getBishopPath(self, currPosCol, currPosRow, board):
        threatList = []

        # top right diagonal
        c, r = currPosCol, currPosRow
        while((self.getNextCol(c, 1), r+1) in board):
            c = self.getNextCol(c, 1)
            r = r+1
            if not self.isObstacle((c, r), board):
                threatList.append((c, r))
            else:
                break

        # top left diagonal
        c, r = currPosCol, currPosRow
        while((self.getPrevCol(c, 1), r+1) in board):
            c = self.getPrevCol(c, 1)
            r = r+1
            if not self.isObstacle((c, r), board):
                threatList.append((c, r))
            else:
                break

        # bottom right diagonal
        c, r = currPosCol, currPosRow
        while((self.getNextCol(c, 1), r-1) in board):
            c = self.getNextCol(c, 1)
            r = r-1
            if not self.isObstacle((c, r), board):
                threatList.append((c, r))
            else:
                break

        # top right diagonal
        c, r = currPosCol, currPosRow
        while((self.getPrevCol(c, 1), r-1) in board):
            c = self.getPrevCol(c, 1)
            r = r-1
            if not self.isObstacle((c, r), board):
                threatList.append((c, r))
            else:
                break

        return threatList

    def getKnightPath(self, currPosCol, currPosRow, board):
        threatList = []

        pos1 = (self.getNextCol(currPosCol, 1), currPosRow+2)
        if pos1 in board and not self.isObstacle(pos1, board):
            threatList.append(pos1)

        pos2 = (self.getPrevCol(currPosCol, 1), currPosRow+2)
        if pos2 in board and not self.isObstacle(pos2, board):
            threatList.append(pos2)

        pos3 = (self.getNextCol(currPosCol, 1), currPosRow-2)
        if pos3 in board and not self.isObstacle(pos3, board):
            threatList.append(pos3)

        pos4 = (self.getPrevCol(currPosCol, 1), currPosRow-2)
        if pos4 in board and not self.isObstacle(pos4, board):
            threatList.append(pos4)

        pos5 = (self.getNextCol(currPosCol, 2), currPosRow+1)
        if pos5 in board and not self.isObstacle(pos5, board):
            threatList.append(pos5)

        pos6 = (self.getNextCol(currPosCol, 2), currPosRow-1)
        if pos6 in board and not self.isObstacle(pos6, board):
            threatList.append(pos6)

        pos7 = (self.getPrevCol(currPosCol, 2), currPosRow+1)
        if pos7 in board and not self.isObstacle(pos7, board):
            threatList.append(pos7)

        pos8 = (self.getPrevCol(currPosCol, 2), currPosRow-1)
        if pos8 in board and not self.isObstacle(pos8, board):
            threatList.append(pos8)

        return threatList

    def getQueenPath(self, currPosCol, currPosRow, board):
        threatList = []

        threatList = self.getBishopPath(currPosCol, currPosRow, board) + self.getRookPath(currPosCol, currPosRow, board)

        return threatList

    def getKingPath(self, currPosCol, currPosRow, board):
        threatList = []

        # top right
        pos1 = (self.getNextCol(currPosCol, 1), currPosRow+1)
        if pos1 in board and not self.isObstacle(pos1, board):
            threatList.append(pos1)

        # horizontal right
        pos2 = (self.getNextCol(currPosCol, 1), currPosRow)
        if pos2 in board and not self.isObstacle(pos2, board):
            threatList.append(pos2)

        # bottom right
        pos3 = (self.getNextCol(currPosCol, 1), currPosRow-1)
        if pos3 in board and not self.isObstacle(pos3, board):
            threatList.append(pos3)

        # bottom straight
        pos4 = (currPosCol, currPosRow-1)
        if pos4 in board and not self.isObstacle(pos4, board):
            threatList.append(pos4)

        # bottom left
        pos5 = (self.getPrevCol(currPosCol, 1), currPosRow-1)
        if pos5 in board and not self.isObstacle(pos5, board):
            threatList.append(pos5)

        # horizontal left
        pos6 = (self.getPrevCol(currPosCol, 1), currPosRow)
        if pos6 in board and not self.isObstacle(pos6, board):
            threatList.append(pos6)

        # top left
        pos7 = (self.getPrevCol(currPosCol, 1), currPosRow+1)
        if pos7 in board and not self.isObstacle(pos7, board):
            threatList.append(pos7)

        # top straight
        pos8 = (currPosCol, currPosRow+1)
        if pos8 in board and not self.isObstacle(pos8, board):
            threatList.append(pos8)

        return threatList

    def isObstacle(self, key, board):
        return board[key].type == 1

    def getNextCol(self, currPosCol, n):
        return chr(ord(currPosCol) + n)

    def getPrevCol(self, currPosCol, n):
        return chr(ord(currPosCol) - n)

class Position:
    type = 0 # 0: empty, 1: obstacle, 2: piece
    piece = None

    def __init__(self, type, piece):
        self.type = type
        self.piece = piece

class Board:
    boardDict = {}
    row = 0
    col = 0
    variables = [0, 0, 0, 0, 0]
    domain = {} # (col, row): true / false
    piecePosition = {} # (col, row): piece 

    def __init__ (self, filename):
        self.parseFile(filename)        

    def parseFile(self, filename):
        # get file and content        
        f = open(filename, "r") 
        for row in f:
            # get number of rows
            if row.startswith("Rows:"):
                self.row = int(row[5:])
            # get number of cols
            elif row.startswith("Cols:"):
                self.col = int(row[5:])
                self.populateBoardAndDomain()
            # get pos of obstacles
            elif row.startswith("Position of Obstacles (space between):"):
                if row[38] == "-":
                    pass
                else:
                    obstacles = row[38:].split()
                    for obstacle in obstacles:
                        obstacleCol, obstacleRow = self.getColAndRow(obstacle)
                        self.boardDict[(obstacleCol, obstacleRow)] = Position(1, None)
                        self.domain.pop((obstacleCol, obstacleRow))
            # get number of pieces
            elif row.startswith("Number of King, Queen, Bishop, Rook, Knight (space between):"):
                numPieces = row[60:].split()
                for i in range(5):
                    self.variables[i] = numPieces[i]

    def getPiecePositionDict(self):
        return self.piecePosition
    
    def getVariables(self):
        return self.variables
    
    def getVariableDict(self):
        variableDict = {}
        count = 0
        for i in self.variables:
            var = int(i)
            if count == 0:
                variableDict["King"] = var
            elif count == 1:
                variableDict["Queen"] = var
            elif count == 2:
                variableDict["Bishop"] = var
            elif count == 3:
                variableDict["Rook"] = var
            elif count == 4:
                variableDict["Knight"] = var
            count += 1
        return variableDict

    def getDomain(self):
        return self.domain

    def populateBoardAndDomain(self):
        for i in range(self.row):
            for j in range(self.col):
                key = self.getKey(j,i)
                self.boardDict[key] = Position(0, None)
                self.domain[key] = True
    
    def getColAndRow(self, pos):
        posCol = pos[0]
        posRow = int(pos[1:])
        return posCol, posRow
    
    def getKey(self, col, row):
        return (chr(col + 97), row)

class State:
    variables = {}
    domain = {}
    piecePosition = {}

    def __init__(self, variables, domain, piecePosition):
        self.variables = variables
        self.domain = domain
        self.piecePosition = piecePosition

class ValidPosition:
    position = None # (col, row)
    threateningSpots = [] # list of spots a position for a piece will threaten
    numThreateningSpots = 0 

    def __init__(self, position, threateningSpots, numThreateningSpots):
        self.position = position
        self.threateningSpots = threateningSpots
        self.numThreateningSpots = numThreateningSpots

    def __lt__(self, other):
        return self.numThreateningSpots < other.numThreateningSpots
    def __eq__(self, other): 
        return self.numThreateningSpots == other.numThreateningSpots

# check if complete assignment, i.e. all values for all pieces in variable dictionary are 0
def checkCompleteAssignment(variables):
    for _, val in variables.items():
        if val != 0:
            return False
    return True

def countNumUnassignedVariables(variables):
    return sum(variables.values())

def countNumValidDomain(domain):
    return len(domain)

def selectUnassignedVariable(state):
    if state.variables["Queen"] > 0:
        return "Queen"
    if state.variables["Bishop"] > 0:
        return "Bishop"
    if state.variables["Rook"] > 0:
        return "Rook"
    if state.variables["King"] > 0:
        return "King"
    if state.variables["Knight"] > 0:
        return "Knight"

# returns pq of assignable values; valid positions that threaten the least other squares
def orderDomainValues(pieceType, state, board):
    currPiece = Piece(pieceType)
    validPositions = [] # list of ValidPosition => (col, row), threateningSpots => minHeap order by len(threateningSpots)
    heapq.heapify(validPositions)
    for key,_ in state.domain.items():
        threateningSpots = []
        isValid = True
        possibleThreateningSpots = currPiece.getPiecePath(key[0], key[1], board)
        for spot in possibleThreateningSpots: # check if placing piece on that position will threaten any existing pieces
            if board[spot].type == 2:
                isValid = False
                break
            threateningSpots.append(spot)
        if isValid:
            numThreateningSpots = len(threateningSpots)
            priority = random.randrange(numThreateningSpots)
            if pieceType == "Queen" and (key[0] == 'a' or key[1] == 0):
                priority = numThreateningSpots    
            validPos = ValidPosition(key, threateningSpots, numThreateningSpots) # get number of spots it threatens
            heapq.heappush(validPositions, (priority, validPos)) # push to list of validPositions for curr variable
    return validPositions

# recursively search
def backtrackSearch(state, board):

    if checkCompleteAssignment(state.variables):
        return state
    var = selectUnassignedVariable(state)
    values = orderDomainValues(var, state, board)
    # pop out 
    while values:
        value = (heapq.heappop(values))[1] # value that reduces the least number of spots
        nextStateDomain = state.domain.copy()
        nextStateDomain.pop(value.position)
        nextStatePiecePositions = state.piecePosition.copy()
        nextStatePiecePositions[value.position] = var
        nextStateVariables = state.variables.copy()
        nextStateVariables[var] -= 1
        board[value.position] = Position(2, Piece(var))
        for spot in value.threateningSpots:
            if nextStateDomain.get(spot) is not None:
                nextStateDomain.pop(spot)
        numValidDomain = countNumValidDomain(nextStateDomain)
        numUnassignedVariables = countNumUnassignedVariables(nextStateVariables)
        if numValidDomain >=  numUnassignedVariables:
            nextState = State(nextStateVariables, nextStateDomain, nextStatePiecePositions)
            result = backtrackSearch(nextState, board)
            if result != None:
                return result
        board[value.position] = Position(0, None)
    return None

def search(testfile):
    board = Board(testfile)
    initPiecePositions = board.getPiecePositionDict().copy()
    initVariables= board.getVariableDict()
    initDomain = board.getDomain()

    initState = State(initVariables, initDomain, initPiecePositions)
    # backtrack search
    state = backtrackSearch(initState, board.boardDict)
    return state.piecePosition

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_CSP():
    # You can code in here but you cannot remove this function or change the return type
    testfile = sys.argv[1] #Do not remove. This is your input testfile.

    goalState = search(testfile)
    return goalState #Format to be returned

