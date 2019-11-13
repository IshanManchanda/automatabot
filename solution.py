import requests

api = 'https://api.noopschallenge.com'


def get_challenge():
	return requests.get(api + '/automatabot/challenges/new').json()


def submit_answer(challenge_url, solution):
	r = requests.post(api + challenge_url, json=solution)
	return r.json()


def get_neighbors(board, x, y):
	height, width = len(board), len(board[0])
	neighbors = 0

	# Coordinates of neighboring cells
	cells = [
		(x - 1, y - 1),
		(x - 1, y),
		(x - 1, y + 1),
		(x, y - 1),
		(x, y + 1),
		(x + 1, y - 1),
		(x + 1, y),
		(x + 1, y + 1)
	]

	for cell in cells:
		# Check if the potential cell is within bounds
		if 0 <= cell[0] < height and 0 <= cell[1] < width:
			neighbors += board[cell[0]][cell[1]]
	return neighbors


def simulate(board, rules):
	height, width = len(board), len(board[0])
	new_board = [[0 for i in range(width)] for j in range(height)]

	# Iterate over each cell in the board
	for x in range(height):
		for y in range(width):
			neighbors = get_neighbors(board, x, y)

			# If the cell is alive and the neighbors are enough to survive,
			# or if the cell is dead and the neighbors are enough for birth,
			# the cell stays (or becomes) alive!
			if (board[x][y] and neighbors in rules['survival']) \
				or (not board[x][y] and neighbors in rules['birth']):
				new_board[x][y] = 1
	return new_board


def solve_challenge(challenge):
	challenge_url = challenge['challengePath']
	challenge = challenge['challenge']
	board = challenge['cells']
	rules = challenge['rules']

	print(f'Starting challenge {rules["name"]}')

	for i in range(challenge['generations']):
		board = simulate(board, rules)

	print('Solved! Submitting answer...')
	print(f'Response: {submit_answer(challenge_url, board)}\n')


def main():
	for i in range(10):  # Number of random challenges to solve
		challenge = get_challenge()
		solve_challenge(challenge)


main()
