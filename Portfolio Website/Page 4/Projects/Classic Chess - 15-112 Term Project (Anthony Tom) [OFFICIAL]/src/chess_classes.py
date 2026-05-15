import random
import copy

# Chess Board
class ChessBoard:
    def __init__(self):
        self.board = None
        self.whiteTurn = True
        self.moves = []
        self.ai = False

    def __repr__(self):
        return f'{self.board}'
    
    def getTurn(self):
        if self.whiteTurn == True:
            return 'white'
        else:
            return 'black'
        
    def getMoves(self):
        return self.moves
    
    def addPiece(self, piece, row, col):
        self.board[row][col] = piece

    def getBoard(self):
        return self.board
    
    def initializeBoard(self): 
        # Initializes the board with all pieces in starting positions
        self.board = [['__'] * 8 for i in range(8)]
        bRow1 = ['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb']
        bRow2 = ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb']
        wRow2 = ['Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw']
        wRow1 = ['Rw', 'Nw', 'Bw', 'Qw', 'Kw', 'Bw', 'Nw', 'Rw']
        cols = len(bRow1)
        for i in range(cols):
            newPiece = Piece(bRow1[i][0], bRow1[i][1])
            self.addPiece(newPiece, 0, i)
            newPiece = Piece(bRow2[i][0], bRow2[i][1])
            self.addPiece(newPiece, 1, i)
            newPiece = Piece(wRow2[i][0], wRow2[i][1])
            self.addPiece(newPiece, -2, i)
            newPiece = Piece(wRow1[i][0], wRow1[i][1])
            self.addPiece(newPiece, -1, i)
            
    def setBoard(self, L):
        self.board = copy.deepcopy(L)
    
    def getPiece(self, row, col):
        return self.board[row][col]
    
    def changePlayer(self): 
        # Changes the current player (white or black)
        self.whiteTurn = not self.whiteTurn
        self.flipBoard()
   
    def flipBoard(self):
        self.board = self.board[::-1]
        for row in range(8):
            self.board[row] = self.board[row][::-1] 
    
    def setAI(self):
        self.ai = True
    
    def validMove(self, startRow, startCol, endRow, endCol):
        # Checks if a piece can be moved when it is a player's turn 
        # Check is not considered
        if not self.canMovePiece(startRow, startCol, endRow, endCol):
            return False
        startPiece = self.board[startRow][startCol]
        if type(startPiece) == Piece:
            startColor = startPiece.getColor()
            if startColor == 'w' and self.whiteTurn == False:
                return False
            if startColor == 'b' and self.whiteTurn == True:
                return False
        return True        
  
    def canMovePawn(self, startRow, startCol, endRow, endCol):
        startPiece = self.board[startRow][startCol]
        endPiece = self.board[endRow][endCol]
        if (endPiece == '__') and (startCol == endCol):
            if ((endRow - startRow == -2) and 
                (self.board[startRow-1][startCol] == '__')):
                    return not startPiece.getMoved()
            elif endRow - startRow == -1:
                return True
        elif ((endPiece != '__') and (startPiece.getColor() != 
            endPiece.getColor())):
            return ((endRow - startRow == -1) and 
                (abs(endCol - startCol) == 1))
        else:
            return False
   
    def canMoveRook(self, startRow, startCol, endRow, endCol):
        if startRow == endRow:
            leftCol = min(startCol, endCol)
            rightCol = max(startCol, endCol)
            row = self.board[startRow]
            middle = row[leftCol+1:rightCol]
            for piece in middle:
                if piece != '__':
                    return False
            return True
        elif startCol == endCol:
            column = []
            for row in range(len(self.board)):
                column.append(self.board[row][startCol])
            topRow = min(startRow, endRow)
            bottomRow = max(startRow, endRow)
            middle = column[topRow+1:bottomRow]
            for piece in middle:
                if piece != '__':
                    return False
            return True
        else:
            return False
    
    def canMoveKnight(self, startRow, startCol, endRow, endCol):
        rowDiff = endRow - startRow
        colDiff = endCol - startCol
        return {abs(rowDiff), abs(colDiff)} == {1, 2}
    
    def canMoveBishop(self, startRow, startCol, endRow, endCol):
        rowDiff = endRow - startRow
        colDiff = endCol - startCol
        if abs(rowDiff) == abs(colDiff):
            diagonalDistance = abs(rowDiff)
            rowMult = 1 if rowDiff > 0 else -1
            colMult = 1 if colDiff > 0 else -1
            for i in range(1, diagonalDistance):
                if self.board[startRow+i*rowMult][startCol+i*colMult] != '__':
                    return False
            return True
        else:
            return False
   
    def canMoveQueen(self, startRow, startCol, endRow, endCol):
        return (self.canMoveRook(startRow, startCol, endRow, endCol) or 
            self.canMoveBishop(startRow, startCol, endRow, endCol))
    
    def canMoveKingOnce(self, startRow, startCol, endRow, endCol):
        rowDiff = endRow - startRow
        colDiff = endCol - startCol
        return (abs(rowDiff) <= 1) and (abs(colDiff) <= 1)
    
    def canCastleKing(self, startRow, startCol, endRow, endCol):
        startPiece = self.board[startRow][startCol]
        endPiece = self.board[endRow][endCol]
        if (startPiece == '__') or (endPiece == '__'):
            return False
        elif (startRow != endRow) or (startPiece.getMoved()):
            return False
        elif (endPiece.getType() != 'R'):
            return False
        row = startRow
        leftCol = min(startCol, endCol)
        rightCol = max(startCol, endCol)
        middle = self.board[row][leftCol+1:rightCol]
        for piece in middle:
            if piece != '__':
                return False
        if (startPiece.getName() == 'Kw') and (endPiece.getName() == 'Rw'):
            return True
        elif (startPiece.getName() == 'Kb') and (endPiece.getName() == 'Rb'):
            return True
        else:
            return False
    
    def canEnPassant(self, startRow, startCol, endRow, endCol): 
        startPiece = self.board[startRow][startCol]
        endLocation = self.board[endRow][endCol]
        colDiff = endCol - startCol
        if startPiece == '__':
            return False
        if startPiece.getType() != 'P' or endLocation != '__':
            return False
        if abs(colDiff) != 1:
            return False
        if startPiece.getColor() == 'w' and startRow == 3:
            columns = 'abcdefgh'
            col = columns[endCol]
            endPiece = self.board[3][endCol]
            if (endRow != 2) or (endPiece == '__'):
                return False
            if (endPiece.getMoves() == 1) and (self.moves[-1] == f'P{col}5'):
                return True
        elif startPiece.getColor() == 'b' and startRow == 3:
            columns = 'hgfedcba'
            col = columns[endCol]
            endPiece = self.board[3][endCol]
            if (endRow != 2) or (endPiece == '__'):
                return False
            if (endPiece.getMoves() == 1) and (self.moves[-1] == f'P{col}4'):
                return True
        return False
    
    def canMovePiece(self, startRow, startCol, endRow, endCol):
        if (startRow == None) or (startCol == None):
            return False
        elif (endRow == None) or (endCol == None):
            return False
        coordinates = [startRow, startCol, endRow, endCol]
        for coordinate in coordinates:
            if coordinate < 0 or coordinate > 7:
                return False
        startPiece = self.board[startRow][startCol]
        endPiece = self.board[endRow][endCol]
        if self.canCastleKing(startRow, startCol, endRow, endCol):
            return True
        elif self.canEnPassant(startRow, startCol, endRow, endCol):
            return True
        if startPiece == '__': 
            return False
        if type(endPiece) == Piece:
            endColor = endPiece.getColor()
        startColor, endColor = None, None
        validEnd = (endPiece == '__') or ((endPiece != '__') and 
            (startPiece.getColor() != endPiece.getColor()))
        if not validEnd: return False
        return self.canMovePresentPiece(startPiece, startRow, startCol, 
                                        endRow, endCol)
        
    def canMovePresentPiece(self, startPiece, startRow, startCol, 
                            endRow, endCol):
        if startPiece.getType() == 'P': # Pawns
            return self.canMovePawn(startRow, startCol, endRow, endCol)
        elif startPiece.getType() == 'R': # Rooks
            return self.canMoveRook(startRow, startCol, endRow, endCol)
        elif startPiece.getType() == 'N': # Knights
            return self.canMoveKnight(startRow, startCol, endRow, endCol)
        elif startPiece.getType() == 'B': # Bishops
            return self.canMoveBishop(startRow, startCol, endRow, endCol)
        elif startPiece.getType() == 'Q': # Queens
            return self.canMoveQueen(startRow, startCol, endRow, endCol)
        elif startPiece.getType() == 'K':
            return self.canMoveKingOnce(startRow, startCol, endRow, endCol)
        else: return False
    
    def enPassantMove(self, startRow, startCol, endRow, endCol):
        # Carries out an en passant move (capture)
        columns = 'abcdefgh'
        rows = '87654321'
        if self.whiteTurn:
            endCoord = columns[endCol] + rows[endRow]
        else:
            endCoord = columns[7-endCol] + rows[7-endRow]
        startPiece = self.board[startRow][startCol]
        move = startPiece.getType() + 'x' + endCoord
        self.board[3][endCol] = '__'
        self.moves.append(move)
        self.board[startRow][startCol].hasMoved()
        self.board[startRow][startCol].incrementMove()
        self.board[endRow][endCol] = self.board[startRow][startCol] 
        self.board[startRow][startCol] = '__'
    
    def moveIntoEmptyCell(self, startRow, startCol, endRow, endCol):
        # Moves a piece into an empty cell
        columns = 'abcdefgh'
        rows = '87654321'
        if self.whiteTurn:
            endCoord = columns[endCol] + rows[endRow]
        else:
            endCoord = columns[7-endCol] + rows[7-endRow]
        startPiece = self.board[startRow][startCol]
        move = startPiece.getType() + endCoord
        self.moves.append(move)
        self.board[startRow][startCol].hasMoved()
        self.board[startRow][startCol].incrementMove()
        self.board[endRow][endCol] = self.board[startRow][startCol] 
        self.board[startRow][startCol] = '__'
    
    def castleMove(self, startRow, startCol, endRow, endCol):
        # Carries out a castling move
        self.board[startRow][startCol].hasMoved()
        self.board[startRow][startCol].incrementMove()
        self.board[endRow][endCol].hasMoved()
        self.board[endRow][endCol].incrementMove()
        colDiff = endCol - startCol
        if abs(colDiff) == 3:
            self.moves.append('O-O')
        elif abs(colDiff) == 4:
            self.moves.append('O-O-O')
        row = startRow
        if startCol < endCol:
            self.board[row][startCol+2] = self.board[row][startCol] 
            self.castleMoveChange(row, startCol)
            self.board[row][startCol+1] = self.board[row][endCol]
            self.castleMoveChange(row, endCol)
        elif startCol > endCol:
            self.board[row][startCol-2] = self.board[row][startCol]
            self.castleMoveChange(row, startCol)
            self.board[row][startCol-1] = self.board[row][endCol] 
            self.castleMoveChange(row, endCol)
    
    def castleMoveChange(self, row, col):
        # Helper function for castleMove function
        self.board[row][col].hasMoved()
        self.board[row][col].incrementMove()
        self.board[row][col] = '__'

    def movePiece(self, startRow, startCol, endRow, endCol):
        startPiece = self.board[startRow][startCol]
        endPiece = self.board[endRow][endCol]
        if self.validMove(startRow, startCol, endRow, endCol):
            # Piece objects are maintained through aliasing
            columns = 'abcdefgh'
            rows = '87654321'
            if self.canEnPassant(startRow, startCol, endRow, endCol):
                self.enPassantMove(startRow, startCol, endRow, endCol)
            elif endPiece == '__':
                self.moveIntoEmptyCell(startRow, startCol, endRow, endCol)
            elif self.canCastleKing(startRow, startCol, endRow, endCol):
                self.castleMove(startRow, startCol, endRow, endCol)
            else:
                if self.whiteTurn:
                    endCoord = columns[endCol] + rows[endRow]
                else:
                    endCoord = columns[7-endCol] + rows[7-endRow]
                move = startPiece.getType() + 'x' + endCoord
                self.moves.append(move)
                self.board[startRow][startCol].hasMoved()
                self.board[startRow][startCol].incrementMove()
                self.board[endRow][endCol] = self.board[startRow][startCol] 
                self.board[startRow][startCol] = '__'
    
    def possibleValidMoves(self, row, col):
        # Returns all possible valid (but possibly illegal) moves
        selectedPiece = self.getPiece(row, col)
        if selectedPiece == '__':
            return []
        elif selectedPiece.getType() == 'N':
            return self.validKnightMoves(row, col)
        else:
            moves = []
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    if x == 0 and y == 0:
                        continue
                    moves.extend(self.possibleValidMovesHelper(row, col, row, 
                    col, x, y))
            if selectedPiece.getType() == 'K':
                if self.canCastleKing(row, col, 7, 0):
                    moves.append((7, 0))
                if self.canCastleKing(row, col, 7, 7):
                    moves.append((7, 7))
            return moves
    
    def validKnightMoves(self, row, col): 
        # Knight pieces do not move to adjacent cells
        knightMoves = []
        for i in [-2, -1, 1, 2]:
            for j in [-2, -1, 1, 2]:
                if self.canMovePiece(row, col, row+i, col+j):
                    move = (row+i, col+j)
                    knightMoves.append(move)
        return knightMoves
    
    def possibleValidMovesHelper(self, startRow, startCol, endRow, endCol, dx, 
        dy):
        startPiece = self.board[startRow][startCol]
        if (endRow < 0) or (endRow > 7):
            return []
        elif (endCol < 0) or (endCol > 7):
            return []
        else:
            if (startRow == endRow) and (startCol == endCol):
                return self.possibleValidMovesHelper(startRow, startCol, 
                    endRow + dy, endCol + dx, dx, dy)
            elif self.canMovePiece(startRow, startCol, endRow, endCol):
                return [(endRow, endCol)] + self.possibleValidMovesHelper(
                    startRow, startCol, endRow + dy, endCol + dx, dx, dy)
            else:
                return []
    
    def colorPossibleValidMoves(self, color):
        # Returns a list of all possible valid moves that a side can make
        moves = []
        for row in range(8):
            for col in range(8):
                currPiece = self.getPiece(row, col)
                if currPiece != '__' and currPiece.getColor() == color:
                    moves.extend(self.possibleValidMoves(row, col))
        return moves
   
    def allPossibleValidMoves(self):
        # Returns a list of all possible valid moves (both sides)
        moves = (self.colorPossibleValidMoves('w') + 
            self.colorPossibleValidMoves('b'))
        return moves
   
    def possibleCaptures(self, row, col):
        # Returns a list of all end coordinates with capturable pieces
        moves = self.possibleValidMoves(row, col)
        captures = []
        for move in moves:
            if self.getPiece(row, col) != '__':
                firstPiece = self.getPiece(row, col)
                nextPiece = self.getPiece(move[0], move[1])
                if (nextPiece != '__') and (firstPiece.getColor() != 
                    nextPiece.getColor()):
                        captures.append(move)
        return captures
    
    def legalMove(self, startRow, startCol, endRow, endCol):
        # Returns if a move is legal (valid move and king is not in check)
        if not self.validMove(startRow, startCol, endRow, endCol):
            return False
        tempBoard = copy.deepcopy(self)
        tempBoard.movePiece(startRow, startCol, endRow, endCol)
        if self.whiteTurn and tempBoard.inCheck('w'):
            return False
        elif not self.whiteTurn and tempBoard.inCheck('b'):
            return False
        else:
            return True
    
    def inCheck(self, color):
        # Returns if a player is in check (king is capturable)
        for row in range(8):
            for col in range(8):
                if (self.getPiece(row, col) != '__') and (
                    self.getPiece(row, col).getName() == f'K{color}'):
                        checkRow = row
                        checkCol = col
        otherColor = 'w' if color == 'b' else 'b'
        tempBoard = copy.deepcopy(self)
        tempBoard.flipBoard()
        checkCondition = (7-checkRow, 7-checkCol) in (
            tempBoard.colorPossibleValidMoves(otherColor))
        return checkCondition
    
    def possibleLegalMoves(self, row, col):
        # Returns a list of all possible legal moves
        selectedPiece = self.board[row][col]
        if selectedPiece == '__':
            return []
        elif selectedPiece.getType() == 'N':
            return self.legalKnightMoves(row, col)
        else:
            moves = []
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    if x == 0 and y == 0:
                        continue
                    moves.extend(self.possibleLegalMovesHelper(row, col, row, 
                        col, x, y))
            if selectedPiece.getType() == 'K':
                if self.legalMove(row, col, 7, 0):
                    moves.append((7, 0))
                if self.legalMove(row, col, 7, 7):
                    moves.append((7, 7))
            return moves
    
    def legalKnightMoves(self, row, col): 
        # Knight pieces do not move to adjacent cells
        legalKnightMoves = []
        moves = self.validKnightMoves(row, col)
        for move in moves:
            if self.legalMove(row, col, move[0], move[1]):
                legalKnightMoves.append(move)
        return legalKnightMoves
    
    def possibleLegalMovesHelper(self, startRow, startCol, endRow, endCol, dy, 
        dx):
        startPiece = self.board[startRow][startCol]
        if (endRow < 0) or (endRow > 7):
            return []
        elif (endCol < 0) or (endCol > 7):
            return []
        else:
            if (startRow == endRow) and (startCol == endCol):
                return self.possibleLegalMovesHelper(startRow, startCol, 
                    endRow + dy, endCol + dx, dy, dx)
            elif self.legalMove(startRow, startCol, endRow, endCol):
                return [(endRow, endCol)] + self.possibleLegalMovesHelper(
                    startRow, startCol, endRow + dy, endCol + dx, dy, dx)
            else:
                return []
    
    def possibleLegalCaptures(self, row, col):
        # Returns a list of all possible legal capture moves
        moves = self.possibleLegalMoves(row, col)
        captures = []
        for move in moves:
            if self.getPiece(row, col) != '__':
                firstPiece = self.getPiece(row, col)
                nextPiece = self.getPiece(move[0], move[1])
                if (nextPiece != '__') and (firstPiece.getColor() != 
                    nextPiece.getColor()):
                        captures.append(move)
        return captures
    
    def colorPossibleLegalMoves(self, color):
        # Returns a list of all possible legal moves that a side can make
        moves = []
        for row in range(8):
            for col in range(8):
                currPiece = self.getPiece(row, col)
                if currPiece != '__' and currPiece.getColor() == color:
                    moves.extend(self.possibleLegalMoves(row, col))
        return moves
   
    def inCheckmate(self, color):
        # Returns if a player is in checkmate
        return (len(self.colorPossibleLegalMoves(color)) == 0) and (
            self.inCheck(color))
   
    def inStalemate(self, color):
        # Returns if a player is in stalemate
        piecesLeft = 0
        for row in range(8):
            for col in range(8):
                piece = self.getPiece(row, col)
                if piece != '__':
                    piecesLeft += 1
        if piecesLeft == 2: 
            # 2 Kings Left
            return True
        else:
            return (len(self.colorPossibleLegalMoves(color)) == 0) and (
                not self.inCheck(color))
        
# Chess Pieces
class Piece:
    def __init__(self, type, color):
        self.type = type
        self.color = color
        self.name = self.type + self.color
        self.moved = False
        self.moves = 0
        self.promoted = False
    
    def __repr__(self):
        return f"{self.name}"
    
    def getType(self):
        return self.type
    
    def promote(self, newType):
        if not self.promoted:
            self.type = newType
            self.name = self.type + self.color
            self.promoted = True
    
    def getColor(self):
        return self.color
    
    def getMoved(self):
        return self.moved
    
    def getMoves(self):
        return self.moves
    
    def incrementMove(self):
        self.moves += 1
    
    def getName(self):
        return self.name
    
    def hasMoved(self):
        self.moved = True