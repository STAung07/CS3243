import random
import sys
import copy
 
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
    goal = 0
    pieces = [0, 0, 0, 0, 0]
    isPlaced = {}
 
    def __init__ (self, filename):
        self.parseFile(filename)        
 
    def parseFile(self, filename):
        # get file and content        
        f = open(filename, "r")  
        isPositionsList = False 
        for row in f:
            # get number of rows
            if row.startswith("Rows:"):
                self.row = int(row[5:])
            # get number of cols
            elif row.startswith("Cols:"):
                self.col = int(row[5:])
                self.populateBoard()
            # get pos of obstacles
            elif row.startswith("Position of Obstacles (space between):"):
                if row[38] == "-":
                    pass
                else:
                    obstacles = row[38:].split()
                    for obstacle in obstacles:
                        obstacleCol, obstacleRow = self.getColAndRow(obstacle)
                        self.boardDict[(obstacleCol, obstacleRow)] = Position(1, None)
            # get min number fo peices left in goal s.t they dont threaten each other
            elif row.startswith("K (Minimum number of pieces left in goal):"):
                self.goal = int(row[42:])
            # get number of pieces
            elif row.startswith("Number of King, Queen, Bishop, Rook, Knight (space between):"):
                numPieces = row[60:].split()
                for i in range(5):
                    self.pieces[i] = numPieces[i]
            elif row.startswith("Position of Pieces [Piece, Pos]:"):
                isPositionsList = True
            elif isPositionsList:
                piece = row[1:len(row)-2].split(",")
                pieceType = piece[0]
                piecePosCol, piecePosRow = self.getColAndRow(piece[1])
                self.boardDict[(piecePosCol, piecePosRow)] = Position(2, pieceType)
                self.isPlaced[((piecePosCol, piecePosRow), pieceType)] = True
 
    def getIsPlacedDict(self):
        return self.isPlaced
 
    def getK(self):
        return self.goal
 
    def populateBoard(self):
        for i in range(self.row):
            for j in range(self.col):
                self.boardDict[self.getKey(j,i)] = Position(0, None)
 
    def populateThreatenDicts(self):
        threatens = {}
        threatensCount = {}
        threatenedBy = {}
        threatenedByCount = {}
 
 
        for key, value in self.boardDict.items():
            if value.type == 2:
                currPieceType = value.piece
                currPiece = Piece(value.piece)
                list = currPiece.getPiecePath(key[0], key[1], self.boardDict)
 
                for item in list:
                    if self.boardDict[item].type == 2:
                        threatensKey = (key, currPieceType)
                        threatenedByKey = (item, self.boardDict[item].piece) # ((col, row), pieceType)
                        # get threatens for curr piece
                        if threatensKey in threatens:
                            threatens[threatensKey].append(threatenedByKey)
                            threatensCount[threatensKey] += 1
                        else:
                            threatens[threatensKey] = [threatenedByKey]
                            threatensCount[threatensKey] = 1
 
                        # get threatenedBy for curr piece
                        if threatenedByKey in threatenedBy:
                            threatenedBy[threatenedByKey].append(threatensKey)
                            threatenedByCount[threatenedByKey] += 1
                        else:
                            threatenedBy[threatenedByKey] = [threatensKey]
                            threatenedByCount[threatenedByKey] = 1
 
        return threatens, threatensCount, threatenedBy, threatenedByCount
 
    def getNumPiecesOnBoard(self, state):
        ans = 0
        for _, value in state.isPlacedDict.items():
            if value == True:
                ans += 1
        return ans
 
    def calculateThreats(self, isPlaced, threatens, threatenedBy):
        threats = 0
        for key, value in isPlaced.items():
            if value == True:
                if key in threatens:
                    for item in threatens[key]: # pieces a current key threatens
                        if isPlaced[item] == True: # if piece is on the board
                            threats += 1 # increment threats
                if key in threatenedBy:
                    for item in threatenedBy[key]: # pieces a current key is threatenedby
                        if isPlaced[item] == True: # if piece is on board
                            threats += 1
        
        return threats
 
    def randomRestartKey(self, state):
    # all pieces on board, pick random key
        return random.choice(list(state.isPlacedDict.keys()))
 
    def removePiece(self, key, threatens, threatenedBy, state):
        state.isPlacedDict[key] = False # remove piece

        state.numThreatened = self.calculateThreats(state.isPlacedDict, threatens, threatenedBy)

        return state
 
    # find piece that causes most conflict
    def calculateHeuristic(self, key, state, threatens, threatenedBy):
        count = 0
        if key in threatens:
            for item in threatens[key]:
                if state.isPlacedDict[item] == True:
                    count += 1
        if key in threatenedBy:
            for item in threatenedBy[key]:
                if state.isPlacedDict[item] == True:
                    count += 1
        
        return count
 
    def findMinimum(self, state, threatens, threatenedBy):
        remainingPieces = []
        for key, value in state.isPlacedDict.items():
            if value == True:
                remainingPieces.append(key)
        
        nextState = copy.deepcopy(state)
        maxConflict = 0
        pieceHeuristic = {}
        for piece in remainingPieces: # find max and tag heuristic value to piece
            nextState = copy.deepcopy(state)
            currConflict = self.calculateHeuristic(piece, nextState, threatens, threatenedBy)
            pieceHeuristic[piece] = currConflict
            if currConflict > maxConflict:
                maxConflict = currConflict
        
        possibleMax = []
        for key, value in pieceHeuristic.items():
            if value == maxConflict:
                possibleMax.append(key)
        
        minPiece = random.choice(list(possibleMax))

        minState = self.removePiece(minPiece, threatens, threatenedBy, nextState)
        return minState
    
    def getColAndRow(self, pos):
        posCol = pos[0]
        posRow = int(pos[1:])
        return posCol, posRow
    
    def getKey(self, col, row):
        return (chr(col + 97), row)
 
class State:
    # state stores the current piecesDict
    isPlacedDict = {}
    numThreatened = 0
 
    def __init__(self, isPlacedDict, numThreatened):
        self.isPlacedDict = isPlacedDict
        self.numThreatened = numThreatened
 
def search(testfile):
    # initialise board
    board = Board(testfile)
    threatens, initThreatensCount, threatenedBy, initThreatenedByCount = board.populateThreatenDicts()
    initIsPlaced = board.getIsPlacedDict().copy()
    
    # get number of threats at the start
    initNumThreatened = board.calculateThreats(initIsPlaced, threatens, threatenedBy)
    # initial isPlacedDict; all pieces on board
    #initState = State(copy.deepcopy(board.getIsPlacedDict()), copy.deepcopy(initThreatenedBy)) # initial state; all pieces placed
    initState = State(initIsPlaced, initNumThreatened) # initial state; all pieces placed
 
    initNumPieces = board.getNumPiecesOnBoard(initState)
 
    k = board.getK() # target number of pieces to remain
 
    # intermediate state; to be adjusted during search
    state = copy.deepcopy(initState)

    numPieces = initNumPieces
 
    # steepest hill climbing with random restart when no. of pieces placed is < k
    while (1):
        numThreatenedPieces = state.numThreatened
        # random restart when == k pieces and not goal
        if numThreatenedPieces == 0 and numPieces >= k:
            break
        else: 
            if numPieces < k:
                numPieces = initNumPieces
                state = copy.deepcopy(initState)
                #state = initState
                # choose random piece to remove from initial state
                randomKey = board.randomRestartKey(state)
                # removePiece based on randomKey
                state = board.removePiece(randomKey, threatens, threatenedBy, state)
                numPieces -= 1
            else: # remove piece that results in the lowest numThreatenedPieces
                state = board.findMinimum(state, threatens, threatenedBy)
                numPieces -= 1
 
    # ans to be returned
    ans = {}
 
    for key, value in state.isPlacedDict.items():
        if value == True:
            ans[key[0]] = key[1]
 
    return ans
 
 
### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)
 
# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    # You can code in here but you cannot remove this function or change the return type
    testfile = sys.argv[1] #Do not remove. This is your input testfile.
 
    goalState = search(testfile)
    return goalState #Format to be returned

# print(run_local())