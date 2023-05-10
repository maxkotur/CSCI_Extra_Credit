grid = [
    ["-", "-", "-", "-", "Y"],
    ["R", "B", "-", "-", "-"],
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
        if ord(grid[row-1][col-1]) - ord(grid[row-1][col]) != 1:
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

def get_unassigned_variables(grid):
    """Returns a list of unassigned variables in the grid."""
    unassigned_vars = []
    for i in range(5):
        for j in range(5):
            if grid[i][j] == '-':
                unassigned_vars.append((i, j))
    return unassigned_vars

def get_mrv_cell(grid):
    """Returns the cell with the fewest remaining values."""
    unassigned_vars = get_unassigned_variables(grid)
    mrv_cell = None
    min_remaining_values = float('inf')
    for cell in unassigned_vars:
        row, col = cell
        remaining_values = len(get_remaining_values(grid, row, col))
        if remaining_values < min_remaining_values:
            mrv_cell = cell
            min_remaining_values = remaining_values
    return mrv_cell

def get_remaining_values(grid, row, col):
    """Returns a set of remaining values that can be assigned to the given cell."""
    used_values = set(grid[row]) | set(grid[i][col] for i in range(5))
    if row == col:
        used_values |= set(grid[i][i] for i in range(5))
    if row + col == 4:
        used_values |= set(grid[i][4-i] for i in range(5))
    return set('ABCDEFGHIJKLMNOPQRSTUVWXY') - used_values

def count_valid_choices(grid, row, col, letter):
    count = 0
    if letter != grid[row][col] and is_valid(grid, row, col, letter):
        count += 1
    return count


def get_lcv_order(grid, row, col, assigned_letters):
    letter_counts = {}
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXY":
        if letter not in assigned_letters:
            letter_counts[letter] = count_valid_choices(grid, row, col, letter)
    return sorted(letter_counts, key=lambda letter: letter_counts[letter])


def is_full(grid):
    for row in grid:
        if "-" in row:
            return False
    return True



def solve(grid, row=0, col=0, assigned_letters=None):
    if assigned_letters is None:
        assigned_letters = set([grid[row][col] for row in range(5) for col in range(5) if grid[row][col] != "-"])
    # Base case: if we have filled all the cells, return True
    if is_full(grid):
        return True
    # Get the cell with the fewest possible choices
    row, col = get_mrv_cell(grid)
    # Try assigning each letter to the cell in order of increasing cost
    for letter in get_lcv_order(grid, row, col, assigned_letters):
        if letter not in assigned_letters and is_valid(grid, row, col, letter):
            print(f"valid:{letter}")
            grid[row][col] = letter
            assigned_letters.add(letter)
            if solve(grid, row, col, assigned_letters):
                return True

            grid[row][col] = "-"
            assigned_letters.remove(letter)
    # If none of the letters worked, backtrack
    print("backtrack")
    return False


solve(grid)
for row in grid:
    print(row)
