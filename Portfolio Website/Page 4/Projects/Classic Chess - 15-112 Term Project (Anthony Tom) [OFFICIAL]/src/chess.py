from cmu_graphics import *
from chess_classes import ChessBoard, Piece
from minimax_program import *
import copy
import random
import time
import os, pathlib
    
# CMU Graphics
def onAppStart(app):
    startGame(app)

def startGame(app):
    createBoard(app)
    preferenceInformation(app)
    selectionInformation(app)
    checkInformation(app)
    scoreInformation(app)
    timerInformation(app)

def createBoard(app):
    app.board = ChessBoard()
    app.board.initializeBoard()
    app.boardWidth = app.width - 200
    app.boardHeight = app.height - 200
    app.boardLeft = app.width/2 - app.boardWidth/2 - 20
    app.boardTop = app.height/2 - app.boardHeight/2
    app.cols, app.rows = 8, 8
    app.cellWidth = app.boardWidth / app.cols
    app.cellHeight = app.boardHeight / app.rows

def preferenceInformation(app):
    app.modes = {0: '1v1', 1:'easy', 2:'medium', 3:'hard', 4:'extreme'}
    app.mode = None
    app.press, app.hold = True, False
    app.holding = False
    app.showInfo = False
    app.showMoves = False
    app.information = """
    INFORMATION: 

    To learn the rules of chess, visit
    en.wikipedia.org/wiki/Rules_of_chess
        The descriptions below are "Pressed Key - Action"
    Modes:
        0 - Player vs. Player Mode
        1 - Easy AI
        2 - Medium AI
        3 - Hard AI
        4 - Extreme AI
    Commands:
        c - Click mode (pieces)
        d - Drag and drop mode (pieces)
        e - Automated move (computer)
        i - Show info screen
        m - Show game moves
        s - Restart game
        Arrow Keys - Move selected cells
        b, n, q, r (clicked pawn) - promotes pawn
    """

def selectionInformation(app):
    app.clicked = False
    app.clickedCellRow, app.clickedCellCol = None, None # for pawn promotion
    app.selectedCellRow, app.selectedCellCol = None, None
    app.validMove, app.invalidMove = False, False
    app.whiteTurn = True

def checkInformation(app):
    app.whiteCheck = False
    app.blackCheck = False
    app.whiteCheckmate = False
    app.blackCheckmate = False
    app.stalemate = False
    
def scoreInformation(app):
    app.scoring = {'P':1, 'N':3, 'B':3, 'R':5, 'Q':9, 'K':1000}
    app.whiteScore = 0
    app.blackScore = 0

def timerInformation(app):
    app.stepsPerSecond = 50
    app.whiteTimer, app.blackTimer = 180, 180
    app.steps = 0
    app.beginGame = False
    app.gameOver = False

def onStep(app):
    if app.beginGame and not app.gameOver:
        if app.mode == '1v1':
            app.steps += 1
            if app.steps % 50 == 0:
                if app.whiteTurn:
                    app.whiteTimer -= 1
                else:
                    app.blackTimer -= 1
            if (app.whiteTimer <= 0) or (app.blackTimer <= 0):
                app.gameOver = True
        
def redrawAll(app):
    if not app.beginGame:
        drawStartScreen(app)
        if app.showInfo: drawInfoScreen(app)
    elif not app.gameOver:
        drawBackground(app)
        drawTurn(app)
        drawCoordinates(app)
        drawBoard(app)
        drawTimers(app)
        drawScores(app)
        if app.showInfo: drawInfoScreen(app)
        if app.showMoves: drawMoves(app)
    else: # Game is Over
        drawGameOver(app)

def drawStartScreen(app):
    drawRect(0, 0, app.width, app.height, fill='lightblue')
    drawLabel('Classic Chess', app.width/2, app.height/2 - 40, size=50, 
              font='monospace')
    drawLabel('by Anthony Tom', app.width/2, app.height/2 + 10, size=20, 
              font='monospace')
    drawLabel(f"Press 'i' for Information", 
              app.width/2, app.height/2 + 60, size=25, font='monospace')
    drawLabel(f'Select a mode (0, 1, 2, 3, 4) to start', app.width/2, 
              app.height/2 + 90, size=25, font='monospace')

def drawBackground(app):
    drawRect(0, 0, app.width, app.height, fill=gradient('blue', 'cyan'))
    drawLabel(f"Press 'i' for Information", 150, 20, size=15, font='monospace')

def drawTurn(app):
    drawLabel(f'Turn: {app.board.getTurn().title()}', app.width/2, 50, 
              size=30, font='monospace')

def drawCoordinates(app):
    if app.whiteTurn:
        columns = 'abcdefgh'
        rows = '87654321'
    else:
        columns = 'hgfedcba'
        rows = '12345678'
    for col in range(8):
        labelX = (app.boardLeft) + (col * app.cellWidth) + (app.cellWidth/2)
        labelY = app.boardTop - 10
        drawLabel(columns[col], labelX, labelY, size=20, font='monospace')
    for row in range(8):
        labelX = app.boardLeft - 10
        labelY = (app.boardTop) + (row * app.cellHeight) + (app.cellHeight/2)
        drawLabel(rows[row], labelX, labelY, size=20, font='monospace')

def drawMoves(app):
    # Draws a list of the chess game moves (app.board.get)
    drawRect(0, 0, app.width, app.height, fill='orange')
    drawLabel('Game Moves', app.width/2, 40, size=30, font='monospace')
    movesList = app.board.getMoves()
    for i in range(len(movesList)):
        columnMoves = 15
        drawLabel(f'{i+1}. {movesList[i]}', (i//columnMoves)*150 + 80, 
                  (i*40)%(40*columnMoves) + 70, size=20, font='monospace')
    
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)
    for row in range(app.rows):
        for col in range(app.cols):
            drawPiece(app, row, col)
    if app.clicked:
        if (app.selectedCellRow, app.selectedCellCol) != (None, None):
            drawSelectedCell(app, app.selectedCellRow, app.selectedCellCol)
        if not app.invalidMove:
            currPiece = app.board.getPiece(app.selectedCellRow, 
                app.selectedCellCol)
            if type(currPiece) != Piece:
                pass
            elif app.whiteTurn and currPiece.getColor() == 'w':
                drawPossibleLegalMoves(app, app.selectedCellRow,
                    app.selectedCellCol)
            elif not app.whiteTurn and currPiece.getColor() == 'b':
                drawPossibleLegalMoves(app, app.selectedCellRow, 
                    app.selectedCellCol)
    
def drawCell(app, row, col):
    # Coordinates start at 0, 0
    cellLeft = app.boardLeft + col * app.cellWidth
    cellTop = app.boardTop + row * app.cellHeight
    brown = rgb(184, 139, 74)
    lightBrown = rgb(227, 193, 111)
    cellColor = brown if (row + col) % 2 == 0 else lightBrown
    drawRect(cellLeft, cellTop, app.cellWidth, app.cellHeight, fill=cellColor)

def drawPiece(app, row, col):
    if app.board.getPiece(row, col) == '__':
        pass
    else:
        piece = app.board.getPiece(row, col)
        scale = 0.6
        cellLeft = (app.boardLeft + (1-scale)/2*app.cellWidth + 
                    col * app.cellWidth)
        cellTop = (app.boardTop + (1-scale)/2*app.cellHeight + 
                   row * app.cellHeight)
        pieceLeft = cellLeft + (app.cellWidth / 2)
        pieceTop = cellTop + (app.cellHeight / 2)
        drawImage(f'chess_images/{piece}.png', cellLeft, cellTop, 
            width=app.cellWidth*scale, height=app.cellHeight*scale)

def drawSelectedCell(app, row, col):
    if app.validMove:
        cellColor = 'green'
    elif (app.invalidMove) or (app.board.getPiece(row, col) == '__'):
        cellColor = 'red'
    elif app.whiteTurn:
        pieceColor = app.board.getPiece(row, col).getColor()
        if pieceColor == 'w':
            cellColor = 'cyan'
        else:
            cellColor = 'red'
    elif not app.whiteTurn:
        pieceColor = app.board.getPiece(row, col).getColor()
        if pieceColor == 'b':
            cellColor = 'cyan'
        else:
            cellColor = 'red'
    else:
        cellColor = 'cyan'
    cellLeft = app.boardLeft + col * app.cellWidth
    cellTop = app.boardTop + row * app.cellHeight
    cellRight = cellLeft + app.cellWidth
    cellBottom = cellTop + app.cellHeight
    drawLine(cellLeft, cellTop, cellRight, cellTop)
    drawLine(cellRight, cellTop, cellRight, cellBottom)
    drawLine(cellRight, cellBottom, cellLeft, cellBottom)
    drawLine(cellLeft, cellBottom, cellLeft, cellTop)
    drawRect(cellLeft, cellTop, app.cellWidth, app.cellHeight, 
        opacity=50, fill=cellColor)
            
def drawPossibleLegalMoves(app, row, col):
    moves = app.board.possibleLegalMoves(row, col)
    for move in moves: # every move is a (row, col) tuple
        moveRow = move[0]
        moveCol = move[1]
        cellLeft = app.boardLeft + moveCol * app.cellWidth
        cellTop = app.boardTop + moveRow * app.cellHeight
        pieceLeft = cellLeft + (app.cellWidth / 2)
        pieceTop = cellTop + (app.cellHeight / 2)
        if app.board.legalMove(row, col, moveRow, moveCol):
            if app.board.canEnPassant(row, col, moveRow, moveCol):
                drawStar(pieceLeft, pieceTop, app.cellWidth/2, 5, 
                         fill='orange', opacity=75)
            elif app.board.canCastleKing(row, col, moveRow, moveCol):
                drawStar(pieceLeft, pieceTop, app.cellWidth/2, 5, 
                         fill='pink', opacity=75)
            elif app.board.getPiece(moveRow, moveCol) == '__':
                drawCircle(pieceLeft, pieceTop, app.cellWidth/10, fill='blue')
            else:
                drawStar(pieceLeft, pieceTop, app.cellWidth/2, 5, 
                         fill='orange', opacity=75)
                
def drawTimers(app):
    if app.mode == '1v1':
        whiteBold = app.whiteTurn
        drawLabel(f'White: {app.whiteTimer}s', app.width/2 - 80, 
            app.boardTop + app.boardHeight + 20, bold=whiteBold, size=20, 
            font='monospace')
        drawLabel(f'Black: {app.blackTimer}s', app.width/2 + 80, 
            app.boardTop + app.boardHeight + 20, bold=(not whiteBold), size=20, 
            font='monospace')

def drawScores(app):
    if app.mode == '1v1':
        shiftDown = 50
    else:
        shiftDown = 40
    drawLabel(f'Scores:  White - {app.whiteScore},  Black - {app.blackScore}', 
        app.width/2, app.boardTop + app.boardHeight + shiftDown, size=20, 
        font='monospace')
    
def drawInfoScreen(app):
    drawRect(0, 0, app.width, app.height, fill='yellow')
    information = app.information
    informationList = information.splitlines()
    for i in range(len(informationList)):
        drawLabel(informationList[i], 0, 20 + i*20, size=20, align='left', 
                  font='monospace')

def drawGameOver(app):
    drawRect(0, 0, app.width, app.height, fill='cyan')
    drawLabel('Game Over', app.width/2, app.height/2, size=40, font='monospace')
    tie = False
    winner = None
    method = None
    if (app.board.inCheckmate('b')):
        winner = 'Player White wins by checkmate!'
    elif (app.board.inCheckmate('w')):
        winner = 'Player Black wins by checkmate!'
    elif (app.blackTimer <= 0):
        winner = 'Player White wins by time!'
    elif (app.whiteTimer <= 0):
        winner = 'Player Black wins by time!'
    elif app.board.inStalemate('b') or app.board.inStalemate('w'):
        tie = True
    if winner != None:
        drawLabel(winner, app.width/2, app.height/2+60, size=30, 
                  font='monospace')
    elif tie:
        drawLabel('Tie by Stalemate!', app.width/2, app.height/2+60, size=30, 
                  font='monospace')

def onKeyPress(app, key):
    if app.clicked:
        newRow = app.selectedCellRow
        newCol = app.selectedCellCol
        if key == 'up': newRow = app.selectedCellRow - 1
        elif key == 'down': newRow = app.selectedCellRow + 1
        elif key == 'left': newCol = app.selectedCellCol - 1
        elif key == 'right': newCol = app.selectedCellCol + 1
        if (0 <= newRow <= 7) and (0 <= newCol <= 7):
            app.selectedCellRow = newRow
            app.selectedCellCol = newCol
    if not app.beginGame and key in '01234':
        app.beginGame = True
        app.mode = app.modes[int(key)]
        if key in '1234': app.board.setAI()
    elif key == 's': startGame(app)
    elif key in 'bnqr':
        promotePawn(app, key)
        computerMove(app, app.mode)
    elif key == 'c': app.press, app.hold = True, False
    elif key == 'd': app.press, app.hold = False, True
    elif key == 'e': computerMove(app, app.mode)

def onKeyHold(app, keys):
    if 'i' in keys:
        app.showInfo = True
    elif 'm' in keys:
        app.showMoves = True

def onKeyRelease(app, keys):
    if 'i' in keys:
        app.showInfo = False
    elif 'm' in keys:
        app.showMoves = False

def onMousePress(app, mouseX, mouseY):
    if app.hold:
        row, col = getCell(app, mouseX, mouseY)
        app.clickedCellRow, app.clickedCellCol = row, col
        selectCell(app, row, col)

def onMouseHold(app, mouseX, mouseY):
    if not app.holding:
        app.holding = True
        row, col = getCell(app, mouseX, mouseY)
        app.clickedCellRow, app.clickedCellCol = row, col
        selectCell(app, row, col)

def onMouseRelease(app, mouseX, mouseY):
    app.holding = False
    row, col = getCell(app, mouseX, mouseY)
    app.clickedCellRow, app.clickedCellCol = row, col
    selectCell(app, row, col)
    if not app.whiteTurn and app.mode != '1v1':
        computerMove(app, app.mode)

def endPositions(app):
    # Returns checkmate and stalemate statuses
    if app.whiteTurn and app.board.inCheckmate('w'):
        # w is checkmated
        app.gameOver = True
    elif not app.whiteTurn and app.board.inCheckmate('b'):
        # b is checkmated
        app.gameOver = True
    elif app.whiteTurn and app.board.inStalemate('w'):
        # w is stalemated
        app.gameOver = True
    elif not app.whiteTurn and app.board.inStalemate('b'):
        # b is stalemated
        app.gameOver = True

def togglePlayer(app):
    # Changes to the next player's turn
    if app.mode == '1v1':
        if app.whiteTurn:
            app.whiteTimer += 2
        else:
            app.blackTimer += 2
    app.whiteTurn = not app.whiteTurn

def getCell(app, x, y):
    # Returns the row and column if a selected cell
    if ((app.boardLeft <= x <= (app.boardLeft + app.boardWidth)) and 
        (app.boardTop <= y <= (app.boardTop + app.boardHeight))):
            row = int((y - app.boardTop) // app.cellHeight)
            col = int((x - app.boardLeft) // app.cellWidth)
            return row, col
    else:
        return None, None

def computerMove(app, mode):
    if mode == 'easy': easyComputerMove(app)
    elif mode == 'medium': mediumComputerMove(app)
    elif mode == 'hard': hardComputerMove(app)
    elif mode == 'extreme': extremeComputerMove(app)
    else: pass

def easyComputerMove(app):
    # Easy Mode computer chooses random pieces and makes random moves.
    allPieceCoordinates = []
    for row in range(8):
        for col in range(8):
            if app.board.getPiece(row, col) != '__':
                if app.whiteTurn:
                    if app.board.getPiece(row, col).getColor() == 'w':
                        coordinate = (row, col)
                        allPieceCoordinates.append(coordinate)
                else:
                    if app.board.getPiece(row, col).getColor() == 'b':
                        coordinate = (row, col)
                        allPieceCoordinates.append(coordinate)
    while True:
        if app.whiteTurn: moves = app.board.colorPossibleLegalMoves('w')
        else: moves = app.board.colorPossibleLegalMoves('b')
        randomPiece = random.choice(allPieceCoordinates)
        currRow = randomPiece[0]
        currCol = randomPiece[1]
        possibleMoves = app.board.possibleLegalMoves(currRow, currCol)
        if possibleMoves != []:
            randomMove = random.choice(possibleMoves)
            selectCell(app, currRow, currCol)
            selectCell(app, randomMove[0], randomMove[1])
            break
        elif moves == []: break
        else: continue

def mediumComputerMove(app):
    # Medium Mode computer uses the minimax algorithm (depth 3) to make moves.
    move = minimaxMove(app)
    if (None not in move[0]) and (None not in move[1]):
        startRow, startCol = move[0][0], move[0][1]
        endRow, endCol = move[1][0], move[1][1]
        selectCell(app, startRow, startCol)
        selectCell(app, endRow, endCol)

def hardComputerMove(app):
    # Hard Mode computer will capture a random piece. If it cannot 
    # capture a random piece, it will make a random move.
    allPieceCoordinates = getComputerMoves(app)[0]
    allPossibleCaptures = getComputerMoves(app)[1]
    allPossibleMoves = getComputerMoves(app)[2]
    random.shuffle(allPieceCoordinates)
    lastRow = app.board.getBoard()[7]
    if (app.whiteTurn) and ('Pw' in lastRow):
        currPiece = app.board.getPiece(7, lastRow.index('Pw'))
        currPiece.promote('Qw')
    elif (not app.whiteTurn) and ('Pb' in lastRow):
        currPiece = app.board.getPiece(7, lastRow.index('Pb'))
        currPiece.promote('Qb')
    elif len(allPossibleCaptures) > 0:
        randomComputerCapture(app, allPieceCoordinates)
    elif len(allPossibleMoves) > 0:
        randomComputerMove(app, allPieceCoordinates)

def extremeComputerMove(app):
    # Extreme Mode computer will capture the highest scoring piece. 
    # If it cannot capture a piece, it will make a random move.
    allPieceCoordinates = getComputerMoves(app)[0]
    allPossibleCaptures = getComputerMoves(app)[1]
    allPossibleMoves = getComputerMoves(app)[2]
    random.shuffle(allPieceCoordinates)
    lastRow = app.board.getBoard()[7]
    if (app.whiteTurn) and ('Pw' in lastRow):
        currPiece = app.board.getPiece(7, lastRow.index('Pw'))
        currPiece.promote('Qw')
    elif (not app.whiteTurn) and ('Pb' in lastRow):
        currPiece = app.board.getPiece(7, lastRow.index('Pb'))
        currPiece.promote('Qb')
    elif len(allPossibleCaptures) > 0:
        bestComputerCapture(app, allPieceCoordinates)
    elif len(allPossibleMoves) > 0:
        randomComputerMove(app, allPieceCoordinates)

def getComputerMoves(app):
    # Returns the possible start, capture, and move coordinates.
    allPieceCoordinates = []
    allPossibleCaptures = []
    allPossibleMoves = []
    for row in range(8):
        for col in range(8):
            if app.board.getPiece(row, col) != '__':
                if (app.whiteTurn) and (
                    app.board.getPiece(row, col).getColor() == 'w'):
                        coordinate = (row, col)
                        captures = app.board.possibleLegalCaptures(row, col)
                        moves = app.board.possibleLegalMoves(row, col)
                        allPieceCoordinates.append(coordinate)
                        allPossibleCaptures.extend(captures)
                        allPossibleMoves.extend(moves)
                elif (not app.whiteTurn) and (
                    app.board.getPiece(row, col).getColor() == 'b'):
                        coordinate = (row, col)
                        captures = app.board.possibleLegalCaptures(row, col)
                        moves = app.board.possibleLegalMoves(row, col)
                        allPieceCoordinates.append(coordinate)
                        allPossibleCaptures.extend(captures)
                        allPossibleMoves.extend(moves)
    return (allPieceCoordinates, allPossibleCaptures, allPossibleMoves)

def randomComputerMove(app, allPieceCoordinates):
    # Makes a random move
    for coordinate in range(len(allPieceCoordinates)):
        currPiece = allPieceCoordinates[coordinate]
        currRow = currPiece[0]
        currCol = currPiece[1]
        possibleMoves = app.board.possibleLegalMoves(currRow, currCol)
        random.shuffle(possibleMoves)
        if len(possibleMoves) > 0:
            moveRow = possibleMoves[0][0]
            moveCol = possibleMoves[0][1]
            selectCell(app, currRow, currCol)
            selectCell(app, moveRow, moveCol)
            break

def randomComputerCapture(app, allPieceCoordinates):
    # Captures a random capturable piece if available
    for coordinate in range(len(allPieceCoordinates)):
        currPiece = allPieceCoordinates[coordinate]
        currRow = currPiece[0]
        currCol = currPiece[1]
        possibleCaptures = app.board.possibleLegalCaptures(currRow, currCol)
        random.shuffle(possibleCaptures)
        if len(possibleCaptures) > 0:
            captureRow = possibleCaptures[0][0]
            captureCol = possibleCaptures[0][1]
            selectCell(app, currRow, currCol)
            selectCell(app, captureRow, captureCol)
            break

def bestComputerCapture(app, allPieceCoordinates):
    # Determines the best capturable piece, then captures it
    startResult = None
    endResult = None
    highestCaptureScore = 0
    for coordinate in range(len(allPieceCoordinates)):
        startCoordinate = allPieceCoordinates[coordinate]
        startRow = startCoordinate[0]
        startCol = startCoordinate[1]
        startCapturePiece = app.board.getPiece(startRow, startCol)
        possibleCaptures = app.board.possibleLegalCaptures(startRow, 
            startCol)
        for capture in possibleCaptures:
            endRow = capture[0]
            endCol = capture[1]
            endCapturePiece = app.board.getPiece(endRow, endCol)
            captureScore = app.scoring[endCapturePiece.getType()]
            if (endResult == None) or (captureScore > 
                highestCaptureScore):
                startResult = (startRow, startCol)
                endResult = (endRow, endCol)
                highestCaptureScore = captureScore
    startResultRow, startResultCol = startResult[0], startResult[1]
    endRusultRow, endResultCol = endResult[0], endResult[1]
    selectCell(app, startResultRow, startResultCol)
    selectCell(app, endRusultRow, endResultCol)

"""def loadSound(relativePath): # From CMU 15-112 TA Evan Lohn
    # The sound file worked on my computer, but not for my TP Mentor Melody Gao's.
    # Convert to absolute path (because pathlib.Path only takes absolute paths)
    absolutePath = os.path.abspath(relativePath)
    # Get local file URL
    url = pathlib.Path(absolutePath).as_uri()
    # Load Sound file from local URL
    return Sound(url)
"""

def selectCell(app, row, col):
    resetCells(app)
    setMoveProperties(app, row, col)
    endPositions(app)
    """# Sounds did not work on my TP Mentor's computer
    if app.validMove:
        loadSound('../sound_effects/move.mp3').play()
    elif app.invalidMove:
        loadSound('../sound_effects/error.mp3').play()"""

def resetCells(app):
    # Resets the chess board cell properties
    if app.validMove:
        app.validMove = False
        app.selectedCellRow, app.selectedCellCol = None, None
    elif app.invalidMove:
        app.invalidMove = False
        app.selectedCellRow, app.selectedCellCol = None, None      

def setMoveProperties(app, row, col):
    # Establishes chess board cell properties
    if (row, col) == (app.selectedCellRow, app.selectedCellCol):
        app.clicked = False
        app.selectedCellRow, app.selectedCellCol = None, None
    elif (app.selectedCellRow, app.selectedCellCol) == (None, None):
        app.clicked = True
        app.selectedCellRow, app.selectedCellCol = row, col
    elif app.board.legalMove(app.selectedCellRow, app.selectedCellCol, 
                row, col):
        legalMoveAction(app, row, col)
    else:
        nonMoveAction(app, row, col)

def legalMoveAction(app, row, col):
    # Actions for legal moves
    endPiece = app.board.getPiece(row, col)
    if endPiece != '__' and app.whiteTurn:
        app.whiteScore += app.scoring[endPiece.getType()]
    elif endPiece != '__'and not app.whiteTurn:
        app.blackScore += app.scoring[endPiece.getType()]
    app.board.movePiece(app.selectedCellRow, app.selectedCellCol, 
        row, col)
    app.validMove = True
    app.selectedCellRow, app.selectedCellCol = 7-row, 7-col 
    togglePlayer(app)
    app.board.changePlayer()

def nonMoveAction(app, row, col):
    # Actions for illegal moves
    if row == None or col == None: return None
    elif not (0 <= row <= 7) or not (0 <= col <= 7): return None
    firstPiece = app.board.getPiece(app.selectedCellRow, app.selectedCellCol)
    nextPiece = app.board.getPiece(row, col)
    if firstPiece == None or nextPiece == None:
        app.invalidMove = True
        app.selectedCellRow, app.selectedCellCol = None, None
    elif firstPiece == '__' and nextPiece == '__':
        app.invalidMove = True
        app.selectedCellRow, app.selectedCellCol = row, col
    elif firstPiece != None and nextPiece != '__':
        if app.whiteTurn and nextPiece.getColor() == 'w':
            app.invalidMove = False
            app.selectedCellRow, app.selectedCellCol = row, col
        elif not app.whiteTurn and nextPiece.getColor() == 'b':
            app.invalidMove = False
            app.selectedCellRow, app.selectedCellCol = row, col
        else:
            app.invalidMove = True
            app.selectedCellRow, app.selectedCellCol = row, col
    else:
        app.invalidMove = True
        app.selectedCellRow, app.selectedCellCol = row, col
    
def promotePawn(app, key):
    # Promotion of a pawn when selected with a key press
    if (app.clickedCellRow, app.clickedCellCol) != (None, None):
        row = app.clickedCellRow
        col = app.clickedCellCol
        piece = app.board.getPiece(row, col)
        if (piece == '__'): pass
        elif ((app.whiteTurn and piece.getColor() == 'w') or 
            (not app.whiteTurn and piece.getColor() == 'b')):
            if piece != '__':
                if ((piece.getName() == 'Pw' and row == 0) or 
                    (piece.getName() == 'Pb' and row == 7)):
                    if key in 'bnqr':
                        currPiece = app.board.getPiece(row, col)
                        app.board.getPiece(row, col).promote(key.upper())
                        app.validMove = True
                        app.selectedCellRow, app.selectedCellCol = row, col
                        togglePlayer(app)
                        app.board.changePlayer()

def main():
    runApp(width=700, height=700)

main()

"""
Sources:
- Chess Piece Images: https://commons.wikimedia.org/wiki/Category:PNG_chess_
    pieces/Standard_transparent
- Sounds: https://www.soundjay.com/button-sounds-2.html (Button Sounds 11, 12)
    11, Button Sound 12)
- Rules of Chess: https://en.wikipedia.org/wiki/Rules_of_chess
"""