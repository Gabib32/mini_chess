import random
import sys
import time

##########################################################

chess_board = [] 
plyNumber = 1
possible_moves = []
moves_stack = []
transpositions = {}

def get_intDepth():
	global plyNumber

	intDepth = 0
	intDepth = (plyNumber / 2) + (plyNumber % 2)
	return intDepth

def get_strNext():
	global plyNumber

	strNext = ''
	if (plyNumber % 2 == 0):
		strNext = 'B'
	else:
		strNext = 'W'
	return strNext

def set_plyNumber(intDepth, strNext):
	global plyNumber

	if (strNext == 'W'):
		plyNumber = (intDepth * 2) - 1
	else:
		plyNumber = intDepth * 2

	return plyNumber 

def chess_reset():
	global chess_board
	global moves_stack
	global transpositions

	moves_stack = []
	chess_board = []
	chess_boardSet("1 W\nkqbnr\nppppp\n.....\n.....\nPPPPP\nRNBQK\n")
#	evaluated_moves = chess_movesEvaluated()
#	tups = []
#	for move in evaluated_moves:
#		tups.append((move, 0, 0, 0))
#	transpositions = {chess_boardGet() : tups}
	return

def chess_boardGet():

	intDepth = get_intDepth()
	strNext = get_strNext()

	strOut = ''
	strOut += str(intDepth) + ' ' + strNext + '\n'

	for row in range(0, 6):
		for column in range(0, 5):
			strOut += chess_board[row][column]
		strOut += '\n'

	return strOut

def chess_boardSet(strIn):
	global chess_board
	global plyNumber

	strIn = strIn.split('\n')

	intDepth = int(strIn[0].split(" ")[0])
	strNext = strIn[0].split(" ")[1]	
	set_plyNumber(intDepth, strNext)
	del strIn[0]

	chess_board = []
	for row in range(0, 6):
		line = []
		for column in range(0, 5):
			line.append(strIn[row][column])
		chess_board.append(line)
	
	return

def chess_winner():
	# determine the winner of the current state of the game and return '?' or '=' or 'W' or 'B' 

	# Considered false until king found within board.
	white_has_king = False
	black_has_king = False

	for row in chess_board:
		if 'K' in row:
			white_has_king = True
		if 'k' in row:
			black_has_king = True	

	if (black_has_king == False):
		return 'W'

	elif (white_has_king == False):
		return 'B'

	if (plyNumber >= 81):
		return '='
	
	return '?'

def chess_isValid(intX, intY):
	if intX < 0:
		return False
		
	elif intX > 4:
		return False
	
	if intY < 0:
		return False
		
	elif intY > 5:
		return False
	
	return True


def chess_isEnemy(strPiece):
	# with reference to the state of the game, return whether the provided argument is a piece from the side not on move - note that we could but should not use the other is() functions in here but probably
	
	strNext = get_strNext()
	white_pieces = ['K', 'Q', 'B', 'N', 'R', 'P']
	black_pieces = ['k', 'q', 'b', 'n', 'r', 'p']
	
	if (strPiece == '.'):
		return False
	if (strNext == 'W'):
		for piece in black_pieces:
			if (strPiece == piece):
				return True
	elif (strNext == 'B'):
		for piece in white_pieces:
			if (strPiece == piece):
				return True
	return False

def chess_isOwn(strPiece):
	# with reference to the state of the game, return whether the provided argument is a piece from the side on move - note that we could but should not use the other is() functions in here but probably

        strNext = get_strNext()
        white_pieces = ['K', 'Q', 'B', 'N', 'R', 'P']
        black_pieces = ['k', 'q', 'b', 'n', 'r', 'p']

        if (strPiece == '.'):
                return False
        if (strNext == 'W'):
                for piece in white_pieces:
                        if (strPiece == piece):
                                return True
        elif (strNext == 'B'):
                for piece in black_pieces:
                        if (strPiece == piece):
                                return True
	return False

def chess_isNothing(strPiece):
	# return whether the provided argument is not a piece / is an empty field - note that we could but should not use the other is() functions in here but probably
	
	if (strPiece == '.'):
		return True
	else:	
		return False

def chess_eval():
	# with reference to the state of the game, return the the evaluation score of the side on move - note that positive means an advantage while negative means a disadvantage

	score = 0
	king_pts = 1000
	queen_pts = 9
	rook_pts = 5
	bishop_pts = 3
	knight_pts = 3
	pawn_pts = 1
	
	for i in range (0, 6):
		for j in range(0, 5):
			cur_piece = chess_board[i][j]
			if (chess_isOwn(cur_piece)):
				if (cur_piece == 'k' or cur_piece =='K'):
					score += king_pts		
				elif (cur_piece == 'q' or cur_piece =='Q'):
					score += queen_pts
				elif (cur_piece == 'r' or cur_piece =='R'):
					score += rook_pts
				elif (cur_piece == 'b' or cur_piece =='B'):
					score += bishop_pts
				elif (cur_piece == 'k' or cur_piece =='K'):
					score += knight_pts
				elif (cur_piece == 'p' or cur_piece =='P'):
					score += pawn_pts
				else:
					continue

			else:
				if (cur_piece == 'k' or cur_piece =='K'):               
                                        score -= king_pts
                                elif (cur_piece == 'q' or cur_piece =='Q'):
                                        score -= queen_pts
                                elif (cur_piece == 'r' or cur_piece =='R'):
                                        score -= rook_pts
                                elif (cur_piece == 'b' or cur_piece =='B'):
                                        score -= bishop_pts
                                elif (cur_piece == 'k' or cur_piece =='K'):
                                        score -= knight_pts
                                elif (cur_piece == 'p' or cur_piece =='P'):
                                        score -= pawn_pts
                                else:
                                        continue
	return score

def chess_moves():
	# with reference to the state of the game and return the possible moves - one example is given below - note that a move has exactly 6 characters
	global possible_moves

	possible_moves = []
	for row in range (0, 6):
		for column in range (0, 5):
			cur_piece = chess_board[row][column]
			if chess_isOwn(cur_piece):
				cur_row=row
				cur_column=column
				get_piece_moves(cur_piece, row, column)

	"".join(possible_moves)
	return possible_moves

def get_piece_moves(piece, cur_row, cur_column):
	global possible_moves

	king_moves = [[0,1], [1,0], [1,1], [0,-1], [-1,0], [1,-1], [-1,1], [-1,-1]]
	queen_moves = [[0,1], [1,0], [1,1], [0,-1], [-1,0], [1,-1], [-1,1], [-1,-1]]
	rook_moves = [[0,1], [1,0], [0,-1], [-1,0]]
	bishop_moves = [[1,1], [1,-1], [-1,1], [-1,-1]]
	bishop_moves_single = [[0,1], [1,0], [0,-1], [-1,0]]
	knight_moves = [[2,1], [2,-1], [-2,1], [-2,-1], [1,2], [1,-2], [-1,2], [-1,-2]]
	# First index is the move without capture, other two are only on capture
	white_pawn_moves = [[-1,0], [-1,1], [-1,-1]]
	black_pawn_moves = [[1,0], [1,1], [1,-1]]

	# Moves for King
	if (piece == 'k' or piece == 'K'):
		for move in king_moves:
			end_row = cur_row + move[0]
			end_column = cur_column + move[1]
			if (chess_isValid(end_column, end_row)):
				board_value = chess_board[end_row][end_column]
				if (chess_isNothing(board_value) or chess_isEnemy(board_value)):
					possible_moves.append(convert_move(cur_row, cur_column, end_row, end_column))
	
	# Moves for Queen
	if (piece == 'q' or piece == 'Q'):
		for move in queen_moves:
			for i in range(1, 6):
				end_row = cur_row + (move[0] * i)
                        	end_column = cur_column + (move[1] * i)
				if (chess_isValid(end_column, end_row)):
					board_value = chess_board[end_row][end_column]
					if (chess_isOwn(board_value)):
						# Can't jump own teammates
						break
					elif chess_isEnemy(board_value):
                                        	possible_moves.append(convert_move(cur_row, cur_column, end_row, end_column))
						break
					elif chess_isNothing(board_value):
                                        	possible_moves.append(convert_move(cur_row, cur_column, end_row, end_column))
					
	# Moves for Rook
	if (piece == 'r' or piece == 'R'):
		for move in rook_moves:
			for i in range(1, 6):
				end_row = cur_row + (move[0] * i)
                                end_column = cur_column + (move[1] * i)
                                if (chess_isValid(end_column, end_row)):
                                        board_value = chess_board[end_row][end_column]
					if (chess_isOwn(board_value)):
                                                # Can't jump own teammates
                                                break
                                        elif chess_isEnemy(board_value):
                                                possible_moves.append(convert_move(cur_row, cur_column, end_row, end_column))
                                                break
                                        elif chess_isNothing(board_value):
                                                possible_moves.append(convert_move(cur_row, cur_column, end_row, end_column))

	# Moves for Bishop
	if (piece == 'b' or piece == 'B'):
		for move in bishop_moves:
			for i in range(1, 6):
                                end_row = cur_row + (move[0] * i)
                                end_column = cur_column + (move[1] * i)
                                if (chess_isValid(end_column, end_row)):
                                        board_value = chess_board[end_row][end_column]
					if (chess_isOwn(board_value)):
                                                # Can't jump own teammates
                                                break
                                        elif chess_isEnemy(board_value):
                                                possible_moves.append(convert_move(cur_row, cur_column, end_row, end_column))
                                                break
                                        elif chess_isNothing(board_value):
                                                possible_moves.append(convert_move(cur_row, cur_column, end_row, end_column))
		for move in bishop_moves_single:
			end_row = cur_row + move[0]
                        end_column = cur_column + move[1]
                        if (chess_isValid(end_column, end_row)):
                                board_value = chess_board[end_row][end_column]
                                if (chess_isNothing(board_value)):
                                        possible_moves.append(convert_move(cur_row, cur_column, end_row, end_column))

	# Moves for Knight
	if (piece == 'n' or piece == 'N'):
		for move in knight_moves:
			end_row = cur_row + move[0]
                        end_column = cur_column + move[1]
                        if (chess_isValid(end_column, end_row)):
                                board_value = chess_board[end_row][end_column]
				if (chess_isNothing(board_value) or chess_isEnemy(board_value)):
                                        possible_moves.append(convert_move(cur_row, cur_column, end_row, end_column))


	# Moves for white pawns
	if (piece == 'P'):
		for move in white_pawn_moves:
			end_row = cur_row + move[0]
                        end_column = cur_column + move[1]
                        if (chess_isValid(end_column, end_row)):
				board_value = chess_board[end_row][end_column]
                                if (white_pawn_moves[0] == move and chess_isNothing(board_value)):
                                        possible_moves.append(convert_move(cur_row, cur_column, end_row, end_column))
				elif ((white_pawn_moves[1] == move or white_pawn_moves[2] == move) and chess_isEnemy(board_value)):
                                        possible_moves.append(convert_move(cur_row, cur_column, end_row, end_column))

	# Moves for black pawns
	if (piece == 'p'):
                for move in black_pawn_moves:
                        end_row = cur_row + move[0]
                        end_column = cur_column + move[1]
                        if (chess_isValid(end_column, end_row)):
                                board_value = chess_board[end_row][end_column]
                                if (black_pawn_moves[0] == move and chess_isNothing(board_value)):
                                        possible_moves.append(convert_move(cur_row, cur_column, end_row, end_column))
                                elif ((black_pawn_moves[1] == move or black_pawn_moves[2] == move) and chess_isEnemy(board_value)):
                                        possible_moves.append(convert_move(cur_row, cur_column, end_row, end_column))

	return 

def convert_move(start_row, start_column, end_row, end_column):
	value = ''
	letters = ['a', 'b', 'c', 'd', 'e']

	for i in range(0, 5):
		if (start_column == i):
			start_column = letters[i]
		if (end_column == i):
			end_column = letters[i]
	start_row = 6 - start_row
	end_row = 6 - end_row

	value += str(start_column)
	value += str(start_row)
	value += '-'
	value += str(end_column)
	value += str(end_row) +'\n'

	''.join(value)
	return value
	
def chess_movesShuffled():
	# with reference to the state of the game, determine the possible moves and shuffle them before returning them- note that you can call the chess_moves() function in here

	chess_moves()
	shuffled_moves = possible_moves
	random.shuffle(shuffled_moves)

	return shuffled_moves


def chess_movesEvaluated():
	# with reference to the state of the game, determine the possible moves and sort them in order of an increasing evaluation score before returning them - note that you can call the chess_movesShuffled() function in here

	moves = chess_movesShuffled()
	scores = []
	combined = []

	for move in moves:
		chess_move(move)
		score = chess_eval()
		scores.append(score)
		combined.append([move, score])
		chess_undo()
	
	evaluated_moves = []
	sorted_combined = sorted(combined, key=lambda tup: tup[1])

	evaluated_moves = []
	for move in sorted_combined:
		evaluated_moves.append(move[0])

	return evaluated_moves

def get_value_int(value):

	# Strings need to be converted from unicode to int
	value = value.lower()	
	
	if (value == 'a' or value == '6'):
		value = 0
	elif (value == 'b' or value == '5'):
		value = 1
	elif (value == 'c' or value == '4'):
		value = 2
	elif (value == 'd' or value == '3'):
		value = 3
	elif (value == 'e' or value == '2'):
		value = 4
	elif (value == '1'):
		value = 5
	else:
		print("Invalid column value\n")
		return False

	return value

def chess_move(strIn):
	# perform the supplied move (for example 'a5-a4\n') and update the state of the game / your internal variables accordingly - note that it advised to do a sanity check of the supplied move

	global chess_board
	global moves_stack
	global plyNumber
	
	# Get the row and column position as numerical value
	move = strIn
	start = strIn.split("-")[0]
	finish = strIn.split("-")[1]

	start_column = get_value_int(start[0])
	finish_column = get_value_int(finish[0])

	start_row = get_value_int(start[1])
	finish_row = get_value_int(finish[1])

	# Get the value of the piece being moved
	current_piece = chess_board[start_row][start_column]

	# Check to ensure move is in range
	if not (chess_isValid(start_column, start_row)):
		print("Invalid Move: start out of range\n")
		return

	elif not (chess_isValid(finish_column, finish_row)):
		print("Invalid Move: finish out of range\n")
		return

	# Check to ensure piece is owned by player
	elif not (chess_isOwn(current_piece)):
		print("Invalid Move: Not your piece to move\n")
		return

	# If error checking passes, move the piece
	else:
		# Update who's turn it is
		plyNumber += 1

		# Add previous state to the stack for undo function
		undo_piece = chess_board[finish_row][finish_column]
		moves_stack.append((move, undo_piece, current_piece))
	
		# Check for promotion
		if (current_piece == 'P' and finish_row == 0):
			current_piece = 'Q'
		elif (current_piece == 'p' and finish_row == 5):
			current_piece = 'q'

		# Move the piece to the correct position
		chess_board[finish_row][finish_column] = current_piece
		chess_board[start_row][start_column] = '.'

		return

def chess_moveRandom():
	# perform a random move and return it - one example output is given below - note that you can call the chess_movesShuffled() function as well as the chess_move() function in here

	shuffled_moves = chess_movesShuffled()
	#randomNum = random.randint(0, 5)
	#move = shuffled_moves[randomNum - 1]

	move = shuffled_moves[0]
	chess_move(move)
	
	return move

def chess_moveGreedy():
	# perform a greedy move and return it - one example output is given below - note that you can call the chess_movesEvaluated() function as well as the chess_move() function in here

	moves_eval = chess_movesEvaluated()
	
	greedy_move = moves_eval[0]
	chess_move(greedy_move)

	return greedy_move 


def chess_moveNegamax(intDepth, intDuration):
	# perform a negamax move and return it - one example output is given below - note that you can call the the other functions in here
	best = ''
	score = -sys.maxint - 1
#	score = -100000
	temp = 0

	for move in chess_movesShuffled():
		chess_move(move)
		temp = -negaMax(intDepth - 1)
		chess_undo()
	
		if (temp > score):
			best = move
			score = temp

	chess_move(best)
	return best
	
def negaMax(intDepth):
	if (intDepth == 0 or chess_winner() != '?'):
		return chess_eval()

	score = -sys.maxint - 1
	#score = -100000

	for move in chess_movesShuffled():
		chess_move(move)
		score = max(score, -negaMax(intDepth - 1))
		chess_undo()

	return score


def chess_moveAlphabeta(intDepth, intDuration):
	# perform a alphabeta move and return it - one example output is given below - note that you can call the the other functions in here
	
	move_limit = (int(time.time() * 1000) + intDuration)
	best = ''
	#alpha = -100000
	#beta = 100000
	alpha = -sys.maxint - 1
	beta = sys.maxint
	temp = 0
	timer = True

	curDepth = intDepth
	if (intDepth == -1):
		curDepth = 2
		intDepth = 1000

	while (curDepth <= intDepth):
#		print("cur: ", curDepth, "int: ", intDepth)
		for move in chess_movesEvaluated():
#			print("move:", move)
			chess_move(move)
			temp = -alphabeta(curDepth - 1, -beta, -alpha)
			chess_undo()
			
			if (temp > alpha):
				best = move
				alpha = temp
			
			if (int(time.time() * 1000) >= move_limit):
#				print("really reached")
				timer = False
				break
		if not timer:
#			print("timeout reached")
			break

		curDepth += 1
#		print("balls are deeper")

	chess_move(best)
	return best
	

def alphabeta(intDepth, alpha, beta):
	global transpositions

	if ((intDepth == 0) or (chess_winner() != '?')):
		return chess_eval()

	score = -sys.maxint - 1
	#score = -100000	

	# get value from transposition table
	current = chess_boardGet()
	if current in transpositions:
		if transpositions[current][0][3] > intDepth:
#			print(transpositions[current])
			return transpositions[current][0][1] 	

	tups = []
	for move in chess_movesEvaluated():
		chess_move(move)
		score = max(score, -alphabeta(intDepth - 1, -beta, -alpha))
		chess_undo()

		tups.append((move, score, 0, intDepth))
		alpha = max(alpha, score)
		
		if (alpha >= beta):
			break

	
	# update transposition table	
	transpositions[current] = sorted(tups, key=lambda x: x[1])
	
#	for i in transpositions:
#		print i, ":", transpositions[i]
#		print("")

	return score

def chess_undo():
	# undo the last move and update the state of the game / your internal variables accordingly - note that you need to maintain an internal variable that keeps track of the previous history for this
	global chess_board
	global moves_stack
	global plyNumber

	# make sure the stack isn't empty
	if (len(moves_stack) > 0):
		tup = moves_stack.pop()
		move = tup[0]
	
		undo_piece = tup[1]
		current_piece = tup[2]
	
		finish = move.split("-")[0]
		start = move.split("-")[1]

		start_column = get_value_int(start[0])
		finish_column = get_value_int(finish[0])
	
		start_row = get_value_int(start[1])
		finish_row = get_value_int(finish[1])

		# Update who's turn it is
		plyNumber -= 1

		# Move the piece to the correct position
		chess_board[finish_row][finish_column] = current_piece
		chess_board[start_row][start_column] = undo_piece
	else:
		print("No moves on stack")

