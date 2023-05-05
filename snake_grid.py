grid = [
    ["-", "-", "-", "-", "Y"],
    ["R", "A", "-", "-", "-"],
    ["-", "-", "-", "-", "-"],
    ["-", "E", "-", "-", "-"],
    ["-", "-", "-", "-", "K"]
]


def is_valid(grid, row, col, letter):
    # Check if the letter is already in the same row or column
    for i in range(5):
        if grid[row][i] == letter or grid[i][col] == letter:
            return False

    # Check if the letter is adjacent to any other letter
    adjacent_letters = []
    if row > 0:
        adjacent_letters.append(grid[row - 1][col])
    if row < 4:
        adjacent_letters.append(grid[row + 1][col])
    if col > 0:
        adjacent_letters.append(grid[row][col - 1])
    if col < 4:
        adjacent_letters.append(grid[row][col + 1])

    num_valid_neighbors = 0
    adjacent_letters = [i for i in adjacent_letters if i != "-"]
    for adj_letter in adjacent_letters:
        if ord(adj_letter) - ord(letter) in [-1, 1]:
            num_valid_neighbors += 1

    if num_valid_neighbors == 0 and len(adjacent_letters) > 0:
        return False

    if row == 1 and col == 4:
        if ord(grid[row-1][col]) - ord(letter) != 1:
            return False

    # Check if the letter would make any other letter invalid
    for i in range(5):
        for j in range(5):
            if grid[i][j] == "-" or (i == row and j == col):
                continue
            if abs(row - i) == 1 and abs(col - j) == 1:
                if ord(grid[i][j]) - ord(letter) == 0:
                    return False

    return True



def solve(grid, row=0, col=0, assigned_letters=None):
    if assigned_letters is None:
        assigned_letters = set([grid[row][col] for row in range(5) for col in range(5) if grid[row][col] != "-"])
    # Base case: if we have filled all the cells, return True
    if row == 5:
        return True
    # Move to the next cell
    if col == 4:
        next_row = row + 1
        next_col = 0
    else:
        next_row = row
        next_col = col + 1
    # If the cell is already filled, move on to the next cell
    if grid[row][col] != "-":
        print("already assigned")
        assigned_letters.add(grid[row][col])
        return solve(grid, next_row, next_col, assigned_letters)
    # Try assigning each letter to the cell
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWX":
        if letter not in assigned_letters and is_valid(grid, row, col, letter):
            print(f"valid:{letter}")
            grid[row][col] = letter
            assigned_letters.add(letter)
            if solve(grid, next_row, next_col, assigned_letters):
                return True

            grid[row][col] = "-"
            assigned_letters.remove(letter)
    # If none of the letters worked, backtrack
    print("backtrack")
    return False


solve(grid)
for row in grid:
    print(row)
