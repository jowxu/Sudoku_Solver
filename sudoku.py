"""
Sudoku Helper
This program provides helper functions for a sudoku
game. It can check a board to determine whether the
rows, columns, and subsquares are correct. It can 
also solve a board if a solution exists.

One of the test boards was taken from
https://lipas.uwasa.fi/~timan/sudoku/s10b.txt
"""
NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
INTERVALS = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

def read_board(filename:str) -> list[list[int]]:
	"""Reads a file containing a 9x9 sudoku
	board formated as nine rows of nine
	comma-separated integers. Creates a list
	containing nine lists where each list
	is a row of the text file. 
	The parameter filename is the location 
	of the file.
	Returns the list of lists.
	Example file text:
	0,5,0,0,1,0,0,4,0
	1,0,1,0,0,0,6,0,2
	0,0,0,9,0,5,0,0,0
	2,0,8,0,3,0,5,0,1
	0,4,0,0,7,0,0,2,0
	9,0,1,0,8,0,4,0,6
	0,0,0,4,0,1,0,0,0
	3,0,4,0,0,0,7,0,9
	0,2,0,0,6,0,0,1,0
	
	Expected data structure:
			[
                [0,5,0,0,1,0,0,4,0],
                [1,0,1,0,0,0,6,0,2],
                [0,0,0,9,0,5,0,0,0],
                [2,0,8,0,3,0,5,0,1],
                [0,4,0,0,7,0,0,2,0],
                [9,0,1,0,8,0,4,0,6],
                [0,0,0,4,0,1,0,0,0],
                [3,0,4,0,0,0,7,0,9],
                [0,2,0,0,6,0,0,1,0]
            ] 

	"""
	file_board = open(filename, 'r')
	board = []
	for line in file_board:
		removed_n = line.replace('\n', '')
		line_list = removed_n.split(',')
		board.append(line_list)
	for row in range(9):
		for column in range(9):
			board[row][column] = int(board[row][column])
	return board

def check_rows(board: list[list[int]]) -> bool:
	"""Returns True if every row in the board
	data structure contains all numbers 1-9 
	and False otherwise.
	"""
	for row in board:
		row_set = set(row) #https://www.geeksforgeeks.org/python-sets/
		for number in row:
			if number not in NUMBERS:
				return False
		if len(row) != len(row_set):
			return False
	return True

def check_columns(board: list[list[int]]) -> bool:
	"""Returns True if every column in the board
	data structure contains all numbers 1-9 
	and False otherwise.
	""" 
	for column in range(9):
		column_set = set([])
		for row in board:
			if row[column] not in NUMBERS:
				return False
			column_set.add(row[column])
		if len(board) != len(column_set):
			return False
	return True

def check_squares(board: list[list[int]]) -> bool:
	"""Returns True if every subsquare in the board
	data structure contains all numbers 1-9 
	and False otherwise.
	"""
	for subsquare_row in [0, 3, 6]:
		for subsquare_column in [0, 3 ,6]:
			subsquare_list = []
			for row in range(subsquare_row, subsquare_row + 3):
				for column in range(subsquare_column, subsquare_column + 3):
					if board[row][column] not in NUMBERS:
						return False
					subsquare_list.append(board[row][column])
			subsquare_set = set(subsquare_list)
			if len(subsquare_list) != len(subsquare_set):
				return False
	return True

def candidate_values(board: list[list[int]], 
						row: int, 
						column: int) -> list[int]:
	"""Takes as parameters a board and two ints
	specifying the row and column of a particular
	square. Returns a list of all possible integers
	that can go in the given square. 
	This function does not "look ahead". It will 
	return a list of the numbers that do not appear
	in the row specified by row, nor the column 
	specified by column, nor the subsquare in 
	which the square is located.
	"""
	used_numbers = []
	for row_number in board[row]:
		if row_number in NUMBERS:
			used_numbers.append(row_number)
	for row_i in range(9):
		column_number = board[row_i][column]
		if column_number in NUMBERS:
			used_numbers.append(column_number)
	row_interval = designate_interval(row)
	column_interval = designate_interval(column)
	for row_index in row_interval:
		for column_index in column_interval:
			subsquare_number = board[row_index][column_index]
			if subsquare_number in NUMBERS:
				used_numbers.append(subsquare_number)
	used_set = set(used_numbers)
	available_numbers = []
	for number in NUMBERS:
		if number not in used_set:
			available_numbers.append(number)
	return available_numbers

def designate_interval(location: int) -> list[int]:
	"""Takes the row or column index and returns the interval
	as a list.
	"""
	if location >= 0 and location <= 2:
		return INTERVALS[0]
	elif location >= 3 and location <= 5:
		return INTERVALS[1]
	return INTERVALS[2]

def check_no_zeroes(board: list[list[int]]) -> bool:
	"""Checks the boards for any zeroes.
	Returns True if there are no zeroes and False otherwise.
	"""
	zeroes = 0
	for row in board:
		if 0 in row:
			zeroes += 1
	return zeroes == 0

def find_zero(board: list[list[int]]) -> tuple:
	"""scans the board for the next zero
	and returns the x,y coordinates.
	"""
	for x in range(9):
		for y in range(9):
			if board[x][y] == 0:
				return x, y

def solve(board: list[list[int]]) -> bool:
	"""Takes a board as a parameter. Returns
	True if the board can be solved and False
	if not. 
	If the board can be solved then the board
	data structure will contain the solution
	when the function completes. If the board
	cannot be solved then the board will have
	all of the original data after the function
	completes.
	"""
	if check_no_zeroes(board):
		return (check_rows(board) and check_columns(board) and check_squares(board))
	x, y = find_zero(board)
	if candidate_values(board, x, y) == []:
		return False
	for candidate in candidate_values(board, x, y):
		board[x][y] = candidate
		solution = solve(board)
		if solution:
			return True
	board[x][y] = 0
	return False

def generate_intro():
	"""Prints out the intro to the program.
	"""
	print('**************************************************')
	print('Welcome to Sudoku Helper!')
	print('You give me a text file containing')
	print('a sudoku board, and I can tell you')
	print('whether it is a valid solution.')
	print('I can also give you a solution...')
	print('...if one exists...I\'m not a magician.')
	print('**************************************************')

def check_solution(board: list[list[int]]) -> bool:
	"""Checks what conditions are met and what are not.
	Returns True if every condition is met and False otherwise.
	Prints corresponding message based on result.
	"""
	if (check_rows(board) and check_columns(board) and check_squares(board)):
		print('Congratulations, your board is a valid solution!')
		return True
	elif (not check_rows(board) and not check_columns(board) and not check_squares(board)):
		print('Sorry......invalid rows......invalid columns......invalid subsquares...')
		return False
	elif (check_rows(board) and not check_columns(board) and not check_squares(board)):
		print('Sorry......invalid columns......invalid subsquares...')
		return False
	elif (not check_rows(board) and check_columns(board) and not check_squares(board)):
		print('Sorry......invalid rows......invalid subsquares...')
		return False
	elif (not check_rows(board) and not check_columns(board) and check_squares(board)):
		print('Sorry......invalid rows......invalid columns...')
		return False
	elif (check_rows(board) and check_columns(board) and not check_squares(board)):
		print('Sorry......invalid subsquares...')
		return False
	elif (check_rows(board) and not check_columns(board) and check_squares(board)):
		print('Sorry......invalid columns...')
		return False
	elif (not check_rows(board) and check_columns(board) and check_squares(board)):
		print('Sorry......invalid rows...')
		return False

def nice_looking_board(board: list[list[int]]) -> str:
	"""Creates a nice looking board as a str
	and returns it.
	"""
	result = f''
	for x in range(9):
		for y in range(9):
			result += f'{str(board[x][y])} '
		if x != 8:
			result += '\n'
	return result

def sudoku_helper():
	"""The main input function where all the user input
	is recorded and used. Calls upon all the other
	functions as necessary.
	"""
	generate_intro()
	using = True
	while using:
		correct_file = False
		while not correct_file:
			try:
				board_file = str(input('Where is the board you would like help with? '))
				board = read_board(board_file)
				correct_file = True
			except:
				print('Please input the correct board file name.')
		board_evaluation = check_solution(board)
		correct_input = False
		while not correct_input:
			if board_evaluation:
				correct_input = True
			else:
				ask_to_solve = ''
				while not (ask_to_solve == 'yes' or ask_to_solve == 'no'):
					ask_to_solve = str(input('Would you like me to solve this for you? ')).lower()
					if ask_to_solve == 'yes' or ask_to_solve == 'no':
						if ask_to_solve == 'yes':
							correct_solution = solve(board)
							if correct_solution:
								print('Yay! I found a solution.')
								print(nice_looking_board(board))
							else:
								print('Sorry, your board cannot be solved.')
						correct_input = True
					else:
						print('Please reply with yes or no.')
		go_again = ''
		while not (go_again == 'yes' or go_again == 'no'):
			go_again = str(input('Would you like to go again? ')).lower()
			if not (go_again == 'yes' or go_again == 'no'):
				print('Please reply with yes or no.')
			elif go_again == 'no':
				using = False

def main():
	sudoku_helper()

if __name__ == '__main__':
	main()