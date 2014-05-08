# SPECIFICATION:
#
# check_sudoku() determines whether its argument is a valid Sudoku
# grid. It can handle grids that are completely filled in, and also
# grids that hold some empty cells where the player has not yet
# written numbers.
#
# First, your code must do some sanity checking to make sure that its
# argument:
#
# - is a 9x9 list of lists
#
# - contains, in each of its 81 elements, an integer in the range 0..9
#
# If either of these properties does not hold, check_sudoku must
# return None.
#
# If the sanity checks pass, your code should return True if all of
# the following hold, and False otherwise:
#
# - each number in the range 1..9 occurs only once in each row 
#
# - each number in the range 1..9 occurs only once in each column
#
# - each number the range 1..9 occurs only once in each of the nine
#   3x3 sub-grids, or "boxes", that make up the board
#
# This diagram (which depicts a valid Sudoku grid) illustrates how the
# grid is divided into sub-grids:
#
# 5 3 4 | 6 7 8 | 9 1 2
# 6 7 2 | 1 9 5 | 3 4 8
# 1 9 8 | 3 4 2 | 5 6 7 
# ---------------------
# 8 5 9 | 7 6 1 | 4 2 3
# 4 2 6 | 8 5 3 | 7 9 1
# 7 1 3 | 9 2 4 | 8 5 6
# ---------------------
# 9 6 1 | 5 3 7 | 0 0 0
# 2 8 7 | 4 1 9 | 0 0 0
# 3 4 5 | 2 8 6 | 0 0 0
# 
# Please keep in mind that a valid grid (i.e., one for which your
# function returns True) may contain 0 multiple times in a row,
# column, or sub-grid. Here we are using 0 to represent an element of
# the Sudoku grid that the player has not yet filled in.

# check_sudoku should return None
ill_formed = [[5,3,4,6,7,8,9,1,2],
              [6,7,2,1,9,5,3,4,8],
              [1,9,8,3,4,2,5,6,7],
              [8,5,9,7,6,1,4,2,3],
              [4,2,6,8,5,3,7,9],  # <---
              [7,1,3,9,2,4,8,5,6],
              [9,6,1,5,3,7,2,8,4],
              [2,8,7,4,1,9,6,3,5],
              [3,4,5,2,8,6,1,7,9]]

# check_sudoku should return True
valid = [[5,3,4,6,7,8,9,1,2],
         [6,7,2,1,9,5,3,4,8],
         [1,9,8,3,4,2,5,6,7],
         [8,5,9,7,6,1,4,2,3],
         [4,2,6,8,5,3,7,9,1],
         [7,1,3,9,2,4,8,5,6],
         [9,6,1,5,3,7,2,8,4],
         [2,8,7,4,1,9,6,3,5],
         [3,4,5,2,8,6,1,7,9]]

# check_sudoku should return False
invalid = [[5,3,4,6,7,8,9,1,2],
           [6,7,2,1,9,5,3,4,8],
           [1,9,8,3,8,2,5,6,7],
           [8,5,9,7,6,1,4,2,3],
           [4,2,6,8,5,3,7,9,1],
           [7,1,3,9,2,4,8,5,6],
           [9,6,1,5,3,7,2,8,4],
           [2,8,7,4,1,9,6,3,5],
           [3,4,5,2,8,6,1,7,9]]

# check_sudoku should return True
easy = [[2,9,0,0,0,0,0,7,0],
        [3,0,6,0,0,8,4,0,0],
        [8,0,0,0,4,0,0,0,2],
        [0,2,0,0,3,1,0,0,7],
        [0,0,0,0,8,0,0,0,0],
        [1,0,0,9,5,0,0,6,0],
        [7,0,0,0,9,0,0,0,1],
        [0,0,1,2,0,0,3,0,6],
        [0,3,0,0,0,0,0,5,9]]

# check_sudoku should return True
hard = [[1,0,0,0,0,7,0,9,0],
        [0,3,0,0,2,0,0,0,8],
        [0,0,9,6,0,0,5,0,0],
        [0,0,5,3,0,0,9,0,0],
        [0,1,0,0,8,0,0,0,2],
        [6,0,0,0,0,4,0,0,0],
        [3,0,0,0,0,0,0,1,0],
        [0,4,0,0,0,0,0,0,7],
        [0,0,7,0,0,0,3,0,0]]

BOXES = [range(3),range(3,6),range(6,9)]

def check_sudoku(grid):
    try:
        chk = [len(grid)==9 and isinstance(grid,list)] + \
              map(lambda L: len(L)==9 and isinstance(L,list), grid) + \
              [isinstance(i,int) and 0<=i<=9 for L in grid for i in L]
        if not all(chk): return None ## Specification Check
    except:
        return None ## If the input isn't a nested iterable or something

    grid_transposed = [[grid[i][j] for i in range(9)] for j in range(9)]
    grid_boxes      = [[grid[i][j] for i in BOXES[m] for j in BOXES[n]]
                       for m in range(3) for n in range(3)]
    
    def counts(L): return all(L.count(i)<=1 for i in range(1,10))
    
    rows  = map(counts, grid)
    cols  = map(counts, grid_transposed)
    boxes = map(counts, grid_boxes)
    
    return all(rows + cols + boxes)

def box(r, c):
    """Returns the "Box" number that square(r,c) is in.
       What is the word that means "quadrant", except there
       are 9 of them? "Nonant"? This gives you the nonant."""
    b1, b2 = -1, -1
    for i in range(3):
        if r in BOXES[i]: b1 = i
        if c in BOXES[i]: b2 = i
    return 3*b1+b2

def copy_zeroes(zeroes,r,c,b,n):
    """Copies the mutable list zeroes = [[r,c,b,set(candidates)],...]
       Also removes n from any other entry with the same r, c, or b.
       Returns False if a contradiction is found."""
    new_z = []
    for i,j,k,candidates in zeroes:
        new_set = set(candidates) - set([n]) if i==r or j==c or k==b else set(candidates)
        if not new_set: return False ## If setting grid[i][j] results in a contradiction
        new_z.append([i,j,k,new_set])
    new_z.sort(key=lambda Z: len(Z[3])) ## Ensures the smallest number of branches are searched
    return new_z

def generate_grids(grid, zeroes):
    """Generator function that yields new grids by filling the square with
    the least number of candidate values.  Returns None for contradiction."""
    r,c,b,candidates = zeroes.pop(0)
    while candidates:
        n = candidates.pop()
        new_zeroes = copy_zeroes(zeroes,r,c,b,n)
        if new_zeroes != False: ## If grid[i][j] = n doesn't immediately cause a contradiction
            new_grid = [[grid[i][j] for j in range(9)] for i in range(9)]
            new_grid[r][c] = n
            yield [new_grid, new_zeroes]
    yield [None, None]
                 
def search_sudoku(grid, zeroes):
    """Recursively finds the correct solution to a sudoku grid.
       zeroes => [[r,c,b,candidates],...]
            r => row #, c => col #, b => box #
            candidates => set of possible values for grid[r][c]
       Outputs either a solution grid, or None if branch ends with contradiction"""
    if not zeroes: return grid
    for new_grid, new_zeroes in generate_grids(grid, zeroes):
        attempt = search_sudoku(new_grid, new_zeroes)
        if attempt: return attempt
    return None

def solve_sudoku(grid):
    """Solves a sudoku puzzle of the form described in check_sudoku()"""
    chk = check_sudoku(grid)
    if not chk: return chk

    ## Initialize the candidates list. Known squares will be filled in first
    zeroes = [[r,c,box(r,c),set([sq])] if sq!=0
              else [r,c,box(r,c),set(range(1,10))]
              for r,row in enumerate(grid)
              for c, sq in enumerate(row)]
    zeroes.sort(key=lambda Z: len(Z[3]))
    return search_sudoku(grid, zeroes)

def show_sudoku(grid):
    if not check_sudoku(grid): return
    line = '- '*13
    for i, row in enumerate(grid):
        if i%3==0: print line
        for j, sq in enumerate(row):
            if j%3==0: print '|',
            print sq,
        print '|'
    print line
    
def is_sudoku_solution(grid, solution):
    chk = check_sudoku(grid) and check_sudoku(solution)
    if not chk: return chk

    solution_contains_grid = [grid[i][j] == solution[i][j]
                              for i in range(9) for j in range(9)
                              if grid[i][j] != 0]

    solution_no_zeroes     = [solution[i][j] != 0
                              for i in range(9) for j in range(9)]

    return all(solution_contains_grid + solution_no_zeroes)

def differential_test(f1, f2):
    def _f1(*args):
        a1, a2 = f1(args), f2(args)
        assert a1==a2
        return a1
    return _f1

def test_sudoku():
    assert is_sudoku_solution(easy,solve_sudoku(easy)) == True
    assert is_sudoku_solution(hard,solve_sudoku(hard)) == True
    assert is_sudoku_solution(hard,solve_sudoku(easy)) == False
    return 'tests pass'
    
print test_sudoku()
