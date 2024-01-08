from cmath import inf
import sys

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
KING = "King"
QUEEN = "Queen"
KNIGHT = "Knight"
BISHOP = "Bishop"
ROOK = "Rook"
PAWN = "Pawn"
# Colours: White, Black (First Letter capitalized)
WHITE = "White"
BLACK = "Black"

KING_VALUE = 900
QUEEN_VALUE = 90
KNIGHT_VALUE = 30
BISHOP_VALUE = 30
ROOK_VALUE = 50
PAWN_VALUE = 10

# Helper functions to aid in your implementation. Can edit/remove
class Piece:

    def __init__(self, color):
        self.color = color

    def getPieceType(self):
        return ""

    def getPieceTypePrint(self):
        return ""

    def getColor(self):
        return self.color

    def getColorPrint(self):
        return self.color[0]

    def isEmpty(self, key, board):
        return board[key] == None

    # checks if piece at pos on board is friendly piece i.e. same color as self.color
    def isFriendly(self, key, board):
        if self.isEmpty(key, board):
            return False
        currPosPieceColor = board[key].color
        return self.color == currPosPieceColor

    # checks if piece at pos on board is enemy piece i.e. diff color as self.color
    def isEnemy(self, key, board):
        if self.isEmpty(key, board):
            return False
        currPosPieceColor = board[key].color
        return self.color != currPosPieceColor

    def isObstacle(self, key, board):
        return self.isFriendly(key, board) or self.isEnemy(key, board)

    def getNextCol(self, currPosCol, n):
        return chr(ord(currPosCol) + n)

    def getPrevCol(self, currPosCol, n):
        return chr(ord(currPosCol) - n)

class Knight(Piece):

    def __init__(self, color):
        super().__init__(color)

    def getPieceType(self):
        return KNIGHT

    def getPieceTypePrint(self):
        return "N"

    def getPieceValue(self):
        return KNIGHT_VALUE

    def getThreateningSpots(self, currPosCol, currPosRow, board):
        return self.getPiecePath(currPosCol, currPosRow, board)
    
    def getPossiblePath(self, currPosCol, currPosRow, board):
        return self.getPiecePath(currPosCol, currPosRow, board)

    def getPiecePath(self, currPosCol, currPosRow, board):
        path = []

        pos1 = (self.getNextCol(currPosCol, 1), currPosRow+2)
        if pos1 in board and not self.isFriendly(pos1, board):
            path.append(pos1)

        pos2 = (self.getPrevCol(currPosCol, 1), currPosRow+2)
        if pos2 in board and not self.isFriendly(pos2, board):
            path.append(pos2)

        pos3 = (self.getNextCol(currPosCol, 1), currPosRow-2)
        if pos3 in board and not self.isFriendly(pos3, board):
            path.append(pos3)

        pos4 = (self.getPrevCol(currPosCol, 1), currPosRow-2)
        if pos4 in board and not self.isFriendly(pos4, board):
            path.append(pos4)

        pos5 = (self.getNextCol(currPosCol, 2), currPosRow+1)
        if pos5 in board and not self.isFriendly(pos5, board):
            path.append(pos5)

        pos6 = (self.getNextCol(currPosCol, 2), currPosRow-1)
        if pos6 in board and not self.isFriendly(pos6, board):
            path.append(pos6)

        pos7 = (self.getPrevCol(currPosCol, 2), currPosRow+1)
        if pos7 in board and not self.isFriendly(pos7, board):
            path.append(pos7)

        pos8 = (self.getPrevCol(currPosCol, 2), currPosRow-1)
        if pos8 in board and not self.isFriendly(pos8, board):
            path.append(pos8)

        return path
        
class Rook(Piece):

    def __init__(self, color):
        super().__init__(color)
    
    def getPieceType(self):
        return ROOK

    def getPieceTypePrint(self):
        return "R"

    def getPieceValue(self):
        return ROOK_VALUE
    
    def getThreateningSpots(self, currPosCol, currPosRow, board):
        return self.getPiecePath(currPosCol, currPosRow, board)
    
    def getPossiblePath(self, currPosCol, currPosRow, board):
        return self.getPiecePath(currPosCol, currPosRow, board)

    def getPiecePath(self, currPosCol, currPosRow, board):
        path = [] # list of tuples of Positions threatened
        # check top
        r = currPosRow
        while (currPosCol,r+1) in board:
            r = r+1
            if self.isEmpty((currPosCol, r), board): # if is an empty spot just append
                path.append((currPosCol, r))
            elif self.isFriendly((currPosCol, r), board): # if is a friendly piece, break
                break
            elif self.isEnemy((currPosCol, r), board): # if is enemy, append and break
                path.append((currPosCol, r))
                break
        # check down
        r = currPosRow
        while (currPosCol,r-1) in board:
            r = r-1
            if self.isEmpty((currPosCol, r), board): # if is an empty spot just append
                path.append((currPosCol, r))
            elif self.isFriendly((currPosCol, r), board): # if is a friendly piece, break
                break
            elif self.isEnemy((currPosCol, r), board): # if is enemy, append and break
                path.append((currPosCol, r))
                break
        # check right
        c = currPosCol
        while (self.getNextCol(c, 1), currPosRow) in board:
            c = self.getNextCol(c, 1)
            if self.isEmpty((c, currPosRow), board): # if is an empty spot just append
                path.append((c, currPosRow))
            elif self.isFriendly((c, currPosRow), board): # if is a friendly piece, break
                break
            elif self.isEnemy((c, currPosRow), board): # if is enemy, append and break
                path.append((c, currPosRow))
                break
        # check left
        c = currPosCol
        while (self.getPrevCol(c, 1), currPosRow) in board:
            c = self.getPrevCol(c, 1)
            if self.isEmpty((c, currPosRow), board): # if is an empty spot just append
                path.append((c, currPosRow))
            elif self.isFriendly((c, currPosRow), board): # if is a friendly piece, break
                break
            elif self.isEnemy((c, currPosRow), board): # if is enemy, append and break
                path.append((c, currPosRow))
                break
        return path

class Bishop(Piece):

    def __init__(self, color):
        super().__init__(color)
    
    def getPieceType(self):
        return BISHOP

    def getPieceTypePrint(self):
        return "B"

    def getPieceValue(self):
        return BISHOP_VALUE
    
    def getThreateningSpots(self, currPosCol, currPosRow, board):
        return self.getPiecePath(currPosCol, currPosRow, board)
    
    def getPossiblePath(self, currPosCol, currPosRow, board):
        return self.getPiecePath(currPosCol, currPosRow, board)
    
    def getPiecePath(self, currPosCol, currPosRow, board):
        path = []

        # top right diagonal
        c, r = currPosCol, currPosRow
        while((self.getNextCol(c, 1), r+1) in board):
            c = self.getNextCol(c, 1)
            r = r+1   
            if self.isEmpty((c, r), board): # if is an empty spot just append
                path.append((c, r))
            elif self.isFriendly((c, r), board): # if is a friendly piece, break
                break
            elif self.isEnemy((c, r), board): # if is enemy, append and break
                path.append((c, r))
                break

        # top left diagonal
        c, r = currPosCol, currPosRow
        while((self.getPrevCol(c, 1), r+1) in board):
            c = self.getPrevCol(c, 1)
            r = r+1
            if self.isEmpty((c, r), board): # if is an empty spot just append
                path.append((c, r))
            elif self.isFriendly((c, r), board): # if is a friendly piece, break
                break
            elif self.isEnemy((c, r), board): # if is enemy, append and break
                path.append((c, r))
                break

        # bottom right diagonal
        c, r = currPosCol, currPosRow
        while((self.getNextCol(c, 1), r-1) in board):
            c = self.getNextCol(c, 1)
            r = r-1
            if self.isEmpty((c, r), board): # if is an empty spot just append
                path.append((c, r))
            elif self.isFriendly((c, r), board): # if is a friendly piece, break
                break
            elif self.isEnemy((c, r), board): # if is enemy, append and break
                path.append((c, r))
                break

        # top right diagonal
        c, r = currPosCol, currPosRow
        while((self.getPrevCol(c, 1), r-1) in board):
            c = self.getPrevCol(c, 1)
            r = r-1
            if self.isEmpty((c, r), board): # if is an empty spot just append
                path.append((c, r))
            elif self.isFriendly((c, r), board): # if is a friendly piece, break
                break
            elif self.isEnemy((c, r), board): # if is enemy, append and break
                path.append((c, r))
                break

        return path
        
class Queen(Piece):

    def __init__(self, color):
        super().__init__(color)

    def getPieceType(self):
        return QUEEN

    def getPieceTypePrint(self):
        return "Q"

    def getPieceValue(self):
        return QUEEN_VALUE
    
    def getThreateningSpots(self, currPosCol, currPosRow, board):
        return self.getPiecePath(currPosCol, currPosRow, board)
    
    def getPossiblePath(self, currPosCol, currPosRow, board):
        return self.getPiecePath(currPosCol, currPosRow, board)
    
    def getPiecePath(self, currPosCol, currPosRow, board):
        path = []

        bishop = Bishop(self.color)
        rook = Rook(self.color)

        path = bishop.getPiecePath(currPosCol, currPosRow, board) + rook.getPiecePath(currPosCol, currPosRow, board)

        return path
        
class King(Piece):

    def __init__(self, color):
        super().__init__(color)

    def getPieceType(self):
        return KING

    def getPieceTypePrint(self):
        return "K"

    def getPieceValue(self):
        return KING_VALUE
    
    def getThreateningSpots(self, currPosCol, currPosRow, board):
        return self.getPiecePath(currPosCol, currPosRow, board)
    
    def getPossiblePath(self, currPosCol, currPosRow, board):
        return self.getPiecePath(currPosCol, currPosRow, board)
    
    def getPiecePath(self, currPosCol, currPosRow, board):
        path = []

        # top right
        pos1 = (self.getNextCol(currPosCol, 1), currPosRow+1)
        if pos1 in board and not self.isFriendly(pos1, board):
            path.append(pos1)

        # horizontal right
        pos2 = (self.getNextCol(currPosCol, 1), currPosRow)
        if pos2 in board and not self.isFriendly(pos2, board):
            path.append(pos2)

        # bottom right
        pos3 = (self.getNextCol(currPosCol, 1), currPosRow-1)
        if pos3 in board and not self.isFriendly(pos3, board):
            path.append(pos3)

        # bottom straight
        pos4 = (currPosCol, currPosRow-1)
        if pos4 in board and not self.isFriendly(pos4, board):
            path.append(pos4)

        # bottom left
        pos5 = (self.getPrevCol(currPosCol, 1), currPosRow-1)
        if pos5 in board and not self.isFriendly(pos5, board):
            path.append(pos5)

        # horizontal left
        pos6 = (self.getPrevCol(currPosCol, 1), currPosRow)
        if pos6 in board and not self.isFriendly(pos6, board):
            path.append(pos6)

        # top left
        pos7 = (self.getPrevCol(currPosCol, 1), currPosRow+1)
        if pos7 in board and not self.isFriendly(pos7, board):
            path.append(pos7)

        # top straight
        pos8 = (currPosCol, currPosRow+1)
        if pos8 in board and not self.isFriendly(pos8, board):
            path.append(pos8)

        return path
        
class Pawn(Piece):

    def __init__(self, color):
        super().__init__(color)

    def getPieceType(self):
        return PAWN

    def getPieceTypePrint(self):
        return "P"

    def getPieceValue(self):
        return PAWN_VALUE
    
    def getThreateningSpots(self, currPosCol, currPosRow, board):
        path = []
        # if white => move down
        if self.getColor() == WHITE:
            pos1 = (self.getNextCol(currPosCol, 1), currPosRow+1)
            if pos1 in board and self.isEnemy(pos1, board):
                path.append(pos1)
            pos2 = (self.getPrevCol(currPosCol, 1), currPosRow+1)
            if pos2 in board and self.isEnemy(pos2, board):
                path.append(pos2)
        # if black => move up
        else:
            pos1 = (self.getNextCol(currPosCol, 1), currPosRow-1)
            if pos1 in board and self.isEnemy(pos1, board):
                path.append(pos1)
            pos2 = (self.getPrevCol(currPosCol, 1), currPosRow-1)
            if pos2 in board and self.isEnemy(pos2, board):
                path.append(pos2)
        return path
    
    def getPossiblePath(self, currPosCol, currPosRow, board):
        # if white => move down
        # if black => move up
        path = []
        # if white => move down
        if self.getColor() == WHITE:
            pos = (currPosCol, currPosRow+1)
            if pos in board and self.isEmpty(pos, board):
                path.append(pos)
        # if black => move up
        else:
            pos = (currPosCol, currPosRow-1)
            if pos in board and self.isEmpty(pos, board):
                path.append(pos)
        return path

class Board:
    boardDict = {}
    friendlyPieces = [0, 0, 0, 0, 0, 0]
    enemyPieces = [0, 0, 0, 0, 0, 0]

    def __init__ (self, gameboard):
        self.populateCurrentBoard(gameboard)

    def populateCurrentBoard(self, gameboard):
        self.populateBoard(5, 5)

        for key, val in gameboard.items():
            self.updateBoardDict(key[0], key[1], val[0], val[1])

    def populateBoard(self, row, col):
        for i in range(row):
            for j in range(col):
                key = self.getKey(j,i)
                self.boardDict[key] = None

    def updateBoardDict(self, piecePosCol, piecePosRow, type, color):
        if type == KING:
            self.boardDict[(piecePosCol, piecePosRow)] = King(color)
        elif type == QUEEN:
            self.boardDict[(piecePosCol, piecePosRow)] = Queen(color)
        elif type == ROOK:
            self.boardDict[(piecePosCol, piecePosRow)] = Rook(color)
        elif type == BISHOP:
            self.boardDict[(piecePosCol, piecePosRow)] = Bishop(color)
        elif type == KNIGHT:
            self.boardDict[(piecePosCol, piecePosRow)] = Knight(color)
        elif type == PAWN:
            self.boardDict[(piecePosCol, piecePosRow)] = Pawn(color)

    def getBoardDict(self): 
        return self.boardDict

    def getColAndRow(self, pos):
        posCol = pos[0]
        posRow = int(pos[1:])
        return posCol, posRow
    
    def getKey(self, col, row):
        return (chr(col + 97), row)



class Action:
    def __init__(self, action, value):
        self.action = action
        self.value = value

    def __lt__(self, other):
        return self.value < other.value
    def __eq__(self, other):
        return self.value == other.value
    def __gt__(self, other):
        return self.value > other.value

class Game:
    # actions(): All legal moves in self.state => remove all moves that place self.state.player's king in check(isCheck)
    def actions(self, state):
        # returns list of (actions, resultantState) in increasing / decreasing order of resultantState.value based on self.state.player
        # go through all possible actions and check if it can be included without resulting in a check
        validActions = []
        #losingActions = []
        opponentColor = WHITE

        if state.player == WHITE:
            opponentColor = BLACK
        
        for pos, piece in state.pieces.items():
            initPos = pos
            if state.player == piece[1]: # if piece of current color
                # get piece object
                piece = state.boardDict[pos]
                # get all positions it can move to
                possiblePositions =  piece.getPossiblePath(pos[0], pos[1], state.boardDict)
                # iterate through list of possiblePos
                for finalPos in possiblePositions:
                    action = (initPos, finalPos)
                    resultantState = self.result(state, action)
                    rStateValue = self.evalFunction(resultantState)
                    # if resultant state of action results in check of current player king; dont add (action, resultant)
                    if not self.isCheck(resultantState, state.player, opponentColor):
                        validAction = Action(action, rStateValue)
                        validActions.append(validAction)
                    '''
                    else:
                        losingAction = Action(action, rStateValue)
                        losingActions.append(losingAction)
                    '''
                    
        order = False
        if state.player == WHITE:
            order = True
        validActions.sort(reverse=order)
        '''
        losingActions.sort(reverse=order)
        if len(validActions) != 0:
            return True, validActions
        return False, losingActions
        '''
        return True, validActions


    # isCutOff(depth): checks if depth == 0 and isTerminal (i.e. win / lose / draw)
    def isCutOff(self, state, depth):
        if depth == 2: #or self.isTerminal(state):
            return True

    def isTerminal(self, state):
        # check if standard checkmate / out of valid moves / king capture
        if self.kingCapture(state) or self.outOfValidMoves(state):
            return True

    # if currentplayer has no more moves that do not place him in check => auto lose for state.player
    def outOfValidMoves(self, state):
        if len(self.actions(state)) == 0:
            state.isLose = True
            return True

    # if opponent king still in check at state.players turn => auto win for state.player
    def kingCapture(self, state):
        kingColor = WHITE
        # kingColor is opposite of current player color
        if state.player == WHITE:
            kingColor = BLACK
        
        if self.isCheck(state, kingColor, state.player):
            return True

    # result(action): takes in an action of moving a piece from (action) => (initPos, finalPos) and returns resultant state {update state boardDict[initPos] to None and boardDict[finalPos] to Piece at initPos}
    def result(self, state, action):
        # updates state based on action
        # returns state.value
        resultantStatePieces = state.pieces.copy()
        resultantStateBoardDict = state.boardDict.copy()
        resultantStatePlayer = WHITE
        if state.player == WHITE:
            resultantStatePlayer = BLACK
        initPos = action[0]
        finalPos = action[1]

        # update boardDict
        initBoardDict = resultantStateBoardDict[initPos]
        resultantStateBoardDict[finalPos] = initBoardDict
        resultantStateBoardDict[initPos] = None
        # update pieces
        initPieces = resultantStatePieces[initPos]
        resultantStatePieces[finalPos] = initPieces
        del resultantStatePieces[initPos]

        resultantState = State(resultantStatePieces, resultantStateBoardDict, resultantStatePlayer)
        
        return resultantState

    # evalFunction():
    def evalFunction(self, state):
        '''
        if state.isWin == True:
            return 20
        if state.isLose == True:
            return -19
        '''
        
        numWhitePieces = 0
        numBlackPieces = 0

        for _, piece in state.pieces.items():
            if piece[1] == WHITE:
                numWhitePieces = numWhitePieces + 1
            else:
                numBlackPieces = numBlackPieces + 1
        
        value = numWhitePieces - numBlackPieces
        
        return value
        '''
        opponentColor = WHITE

        if state.player == WHITE:
            opponentColor = BLACK

        if self.isCheck(state, state.player, opponentColor):
            return -1150
        if self.kingCapture(state):
            return 1150
        
        valueWhitePieces = 0
        valueBlackPieces = 0

        for pos, piece in state.pieces.items():
            currPiece = state.boardDict[pos]
            if piece[1] == WHITE:
                valueWhitePieces = valueWhitePieces + currPiece.getPieceValue()
            else:
                valueBlackPieces = valueBlackPieces + currPiece.getPieceValue()
        
        value = valueWhitePieces - valueBlackPieces

        return value
        '''

    # check is kingColor specified is in check i.e. threatened by any piece in opponentColor
    def isCheck(self, state, kingColor, opponentColor):
        # getposition of king of color specified
        kingPos = self.getKing(state, kingColor)
        # go through all player pieces and check if opponentKing position is in path
        for pos, piece in state.pieces.items():
            pieceColor = piece[1]
            if pieceColor == opponentColor:
                # get piece object
                piece = state.boardDict[pos]
                # get list of threatening spots for current piece
                threatenedPositions = piece.getThreateningSpots(pos[0], pos[1], state.boardDict)
                if kingPos in threatenedPositions:
                    return True
        return False

    # get pos of king of color specified
    def getKing(self, state, color):
        for key, val in state.pieces.items():
            if val == (KING, color):
                return key

# stores board and current player, (value of current state)
class State:
    def __init__(self, pieces, boardDict, player):
        self.pieces = pieces
        self.boardDict = boardDict
        self.player = player

#Implement your minimax with alpha-beta pruning algorithm here.
def ab(gameboard):
    board = Board(gameboard)
    boardDict = board.getBoardDict()
    root = State(gameboard, boardDict, WHITE)
    game = Game()
    _, action = maxValue(0, game, root, -inf, inf)
    return action

def maxValue(depth, game, state, alpha, beta):
    if game.isCutOff(state, depth):
        return game.evalFunction(state), (None, None)
    # max node only change alpha => get max out of all min choices
    currValue = -inf
    move = (None, None)
    hasMoves, possibleActions = game.actions(state)
    #if hasMoves:
    for validAction in possibleActions:
        action = validAction.action
        opponentValue, _ = minValue(depth+1, game, game.result(state, action), alpha, beta)
        # if better value current value found; larger value
        if opponentValue > currValue:
            currValue, move = opponentValue, action
            # update alpha if possible
            alpha = max(alpha, currValue)
        # if currentValue more than ancestor beta value; will never be picked => pruning
        if currValue >= beta:
            return currValue, move

    return currValue, move 
    '''
    if len(possibleActions) == 0:
        return currValue, move
    return currValue, possibleActions[0].action   
    '''

def minValue(depth, game, state, alpha, beta):
    if game.isCutOff(state, depth):
        return game.evalFunction(state), (None, None)
    currValue = inf
    move = (None, None)
    hasMoves, possibleActions = game.actions(state)
    #if hasMoves:
    for validAction in possibleActions:
        action = validAction.action
        opponentValue, _ = maxValue(depth+1, game, game.result(state, action), alpha, beta)
        # if better value current value found; smaller value
        if opponentValue < currValue:
            currValue, move = opponentValue, action
            # update beta if possible
            beta = min(beta, currValue)
        # if currentValue less than ancestor alpha value; will never be picked => pruning
        if currValue <= alpha:
            return currValue, move
    return currValue, move 
    '''
    if len(possibleActions) == 0:
        return currValue, move
    return currValue, possibleActions[0].action
    '''


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Colours: White, Black (First Letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Parameters:
# gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
# Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
# Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
#
# Return value:
# move: A tuple containing the starting position of the piece being moved to the new position for the piece. x-axis in String format and y-axis in integer format.
# move example: (('a', 0), ('b', 3))

def studentAgent(gameboard):
    # You can code in here but you cannot remove this function, change its parameter or change the return type
    #config = sys.argv[1] #Takes in config.txt Optional

    move = ab(gameboard)    

    return move #Format to be returned (('a', 0), ('b', 3))
