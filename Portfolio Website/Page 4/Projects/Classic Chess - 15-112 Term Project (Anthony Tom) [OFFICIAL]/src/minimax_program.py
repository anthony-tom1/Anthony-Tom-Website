import copy

def minimax(app, board, i, depth, whiteScore=0, blackScore=0):
    tempBoard = copy.deepcopy(board)
    if (depth % 2 == 1) and (i > depth-1):
        if tempBoard.getTurn() == 'white': return [whiteScore - blackScore]
        else: return [blackScore - whiteScore]
    elif (depth % 2 == 0) and (i > depth-1):
        if tempBoard.getTurn() == 'white': return [blackScore - whiteScore]
        else: return [whiteScore - blackScore]
    turn = tempBoard.getTurn()
    allPossibleMoves = getAllPossibleMoves(app, tempBoard, turn)
    results = []
    for startCoord in allPossibleMoves:
        for endCoord in allPossibleMoves[startCoord]:
            startRow, startCol = startCoord[0], startCoord[1]
            endRow, endCol = endCoord[0], endCoord[1]
            newWhiteScore, newBlackScore = 0, 0
            endPiece = tempBoard.getPiece(endRow, endCol)
            if endPiece != '__':
                if turn == 'w':
                    newWhiteScore = whiteScore + app.scoring[endPiece.getType()]
                else:
                    newBlackScore = blackScore + app.scoring[endPiece.getType()]
            tempBoard.movePiece(startRow, startCol, endRow, endCol)
            tempBoard.changePlayer()
            if i == 0:
                results.append([startCoord, endCoord] + minimax(app, 
                    tempBoard, i+1, depth, newWhiteScore, newBlackScore))
            else:
                results.append(minimax(app, tempBoard, i+1, depth, 
                    newWhiteScore, newBlackScore))
    return results

def getAllPossibleMoves(app, board, turn):
    allPossibleMoves = dict()
    for row in range(8):
        for col in range(8):
            startCoordinate = (row, col)
            if board.getPiece(row, col) != '__':
                pieceColor = board.getPiece(row, col).getColor()
                if (turn == 'white') and (pieceColor == 'w'):
                    moves = board.possibleLegalMoves(row, col)
                    allPossibleMoves[startCoordinate] = moves
                elif (turn == 'black') and (pieceColor == 'b'):
                    moves = board.possibleLegalMoves(row, col)
                    allPossibleMoves[startCoordinate] = moves
    return allPossibleMoves

def minimaxScores(app):
    """I modified the minimax algorithm by evaluating every possible move 
    by the average of their ending branch scores.
    The computer will carry out the minimax algorithm to a depth of 3."""
    results = minimax(app, app.board, 0, 3)
    scores = dict()
    for result in results:
        move = tuple(result[0:2])
        nonMove = result[2:]
        sumOfScores = 0
        numItems = 0
        for i in range(len(nonMove)):
            for j in range(len(nonMove[i])):
                for k in range(len(nonMove[i][j])):
                    sumOfScores += nonMove[i][j][k]
                    numItems += 1
        if numItems != 0:
            scores[move] = sumOfScores/numItems
    return scores

def minimaxMove(app):
    scores = minimaxScores(app)
    maxMove = None
    maxScore = None
    for move in scores:
        if (maxScore == None) or (scores[move] > maxScore):
            maxMove = move
            maxScore = scores[move]
    return maxMove