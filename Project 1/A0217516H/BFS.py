import sys

# Helper functions to aid in your implementation. Can edit/remove
class Piece:
    # type attribute
    type = ""

    def __init__(self, pieceType):
        self.type = pieceType

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
        return board[key].type == 1 or board[key].type == 2 or board[key].type == 4

    def getNextCol(self, currPosCol, n):
        return chr(ord(currPosCol) + n)

    def getPrevCol(self, currPosCol, n):
        return chr(ord(currPosCol) - n)


# one board for entire run; dictionary of positions 
# key is position in (row, col) format 
# value is type of position {obstacle, enemy, friendly, threat, empty} + step cost to reach that step
class Position:
    # 0: empty; 1: obstacle; 2: enemy; 3: threat; 4: friendly; 5: goal
    type = 0
    stepCost = 0

    def __init__(self, type, stepCost):
        self.type = type
        self.stepCost = stepCost

class Board:
    # dictionary where key is (row, col)
    boardDict = {}
    row = 0
    col = 0
    enemyPieces = [0,0,0,0,0]
    friendlyPieces = [1,0,0,0,0]
    kingStart = ()

    def __init__ (self, filename):
        self.parseFile(filename)        

    def parseFile(self, filename):
        # get file and content        
        f = open(filename, "r")   
        isStepCostsList = False
        isEnemyPiecesList = False
        isFriendlyPiecesList = False
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
                obstacles = row[38:].split()
                for obstacle in obstacles:
                    obstacleCol, obstacleRow = self.getColAndRow(obstacle)
                    self.boardDict[(obstacleCol, obstacleRow)] = Position(1, 1)
            # start of step costs
            elif row.startswith("Step cost to move to selected grids (Default cost is 1) [Pos, Cost]:"):
                isStepCostsList = True
            elif isStepCostsList:
                # if not end of stepCosts; get step costs and update
                if not row.startswith("Number of Enemy King, Queen, Bishop, Rook, Knight (space between):"):
                    info = row[1:len(row) - 2].split(",")
                    currPosCol, currPosRow = self.getColAndRow(info[0])
                    stepCost = info[1]
                    currType = (self.boardDict[(currPosCol, currPosRow)]).type # keep type of current position 
                    self.boardDict[(currPosCol, currPosRow)] = Position(currType, stepCost)
                    
                # end of step costs list; get enemy pieces
                else:
                    isStepCostsList = False
                    numEnemies = row[66:].split()
                    for i in range(5):
                        self.enemyPieces[i] = numEnemies[i]
            # start of enemy pieces
            elif row.startswith("Position of Enemy Pieces:"):
                isEnemyPiecesList = True
            elif isEnemyPiecesList:
                # if not end of enemy list; get Piece and position => calculate and update threatened spots
                if not row.startswith("Number of Own King, Queen, Bishop, Rook, Knight (space between):"):
                    # get enemy currpos and update board
                    enemy = row[1:len(row)-2].split(",")
                    enemyPosCol, enemyPosRow = self.getColAndRow(enemy[1])
                    stepCost = (self.boardDict[(enemyPosCol, enemyPosRow)]).stepCost
                    self.boardDict[(enemyPosCol, enemyPosRow)] = Position(2, stepCost)
                    # create Piece and get list of threatened positions
                    currPiece = Piece(enemy[0])
                    threatenedPosList = currPiece.getPiecePath(enemyPosCol, enemyPosRow, self.boardDict)
                    # update all positions
                    for pos in threatenedPosList:
                        currStepCost = (self.boardDict[pos]).stepCost
                        self.boardDict[pos] = Position(3, currStepCost)
                # end of enemy pieces list; get friendly pieces
                else:
                    isEnemyPiecesList = False
                    numFriendlies = row[64:].split()
                    for i in range(5):
                        self.friendlyPieces[i] = numFriendlies[i]
            # start of friendly pieces
            elif row.startswith("Starting Position of Pieces [Piece, Pos]:"):
                isFriendlyPiecesList = True
            elif isFriendlyPiecesList:
                # if not end of friendly list; get piece and position; update board
                if not row.startswith("Goal Positions (space between):"):
                    friendly = row[1:len(row) - 2].split(",")
                    friendlyPosCol, friendlyPosRow = self.getColAndRow(friendly[1])
                    stepCost = (self.boardDict[(friendlyPosCol, friendlyPosRow)]).stepCost
                    self.boardDict[(friendlyPosCol, friendlyPosRow)] = Position(4, stepCost)
                    if friendly[0] == "King": # get friendly king position
                        self.kingStart = (friendlyPosCol, friendlyPosRow)
                # get goal position
                else:
                    isFriendlyPiecesList = False
                    goalPos = row[31:].split()
                    for goal in goalPos:
                        goalCol, goalRow = self.getColAndRow(goal)
                        stepCost = (self.boardDict[(goalCol, goalRow)]).stepCost
                        self.boardDict[(goalCol, goalRow)] = Position(5, stepCost)
            
        """
        print(self.row)
        print(self.col)
        print(self.enemyPieces)
        print(self.friendlyPieces)
        print(self.kingStart)
        print(self.printBoard())
        """

    # expand from current state
    def expandNode(self,currNode):
        currPos, currPath = currNode.currPos, currNode.path
        # print("expandNode currPos: ", currPos)
        # print("expandNode currPath: ", currPath)
        col, row = currPos[0], currPos[1]
        possiblePos = Piece("King").getPiecePath(col, row, self.boardDict)
        # print(possiblePos)
        nextStates = []
        for pos in possiblePos:
            newPath = currPath.copy()
            # print(newPath)
            if self.isEmpty(pos) or self.isGoal(pos):
                newPath.append([currPos, pos])
                nextStates.append(Node(pos, newPath))
        return nextStates

    def isEmpty(self, pos):
        return self.boardDict[pos].type == 0

    def isGoal(self, pos):
        return self.boardDict[pos].type == 5

    def getKingStart(self):
        return self.kingStart

    def populateBoard(self):
        for i in range(self.row):
            for j in range(self.col):
                self.boardDict[self.getKey(j,i)] = Position(0, 1)

    def printBoard(self):
        for i in range(self.row):
            print("")
            for j in range(self.col):
                currPosition = self.boardDict[self.getKey(j,i)]
                #print(self.getKey(j,i), end = " ")
                print(currPosition.type, currPosition.stepCost, end = " ")
                print("|", end = " ")

    def getColAndRow(self, pos):
        posCol = pos[0]
        posRow = int(pos[1:])
        return posCol, posRow

    def getKey(self, col, row):
        return (chr(col + 97), row)

# state stores position of King and path
class Node:
    currPos = ()
    path = []

    def __init__(self, currPos, path):
        self.currPos = currPos
        self.path = path


def search():
    board = Board(sys.argv[1])

    # get init start Pos
    startPos = board.getKingStart()

    # queue for BFS
    frontier = [Node(startPos, [])]

    # reached hash table
    reached = {}
    reached[startPos] = True

    nodesExplored = 0

    while frontier:
        # pop first in frontier
        #currNode = frontier[0]
        #print(currNode.currPos, end = " ")
        #print(currNode.path)
        currNode = frontier.pop(0)
        nodesExplored += 1

        # go through possible nextstates
        for child in board.expandNode(currNode):
            #print("expanded")
            currPos = child.currPos # get currPos
            if board.isGoal(currPos):
                return child.path, nodesExplored
            if currPos not in reached:
                reached[currPos] = True
                frontier.append(child)
    # failure

    return [], 1

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_BFS():
    # You can code in here but you cannot remove this function or change the return type 
    # search()
    moves, nodesExplored = search() #For reference
    return moves, nodesExplored #Format to be returned

print(run_BFS())
