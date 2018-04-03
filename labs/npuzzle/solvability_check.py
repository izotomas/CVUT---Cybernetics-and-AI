import npuzzle
 
def is_solvable(env):
    '''
    True or False?
    '''
    # your code comes here
    size = env._NPuzzle__size
    tiles = env._NPuzzle__tiles
    inv = __inversion_count(tiles, size)
    blank = __blank_row_number_from_bottom(tiles, size) 
    if __is_even(size):
        ''''the blank is on an even row counting from the bottom 
        (second-last, fourth-last, etc.) and number of inversions is odd.

        the blank is on an odd row counting from the bottom 
        (last, third-last, fifth-last, etc.) 
        and number of inversions is even.
        '''
        if (__is_even(inv)):
            return not __is_even(blank)
        else:
            return __is_even(blank)
    else:
        return __is_even(inv) # number of inversion must be even

def __blank_row_number_from_bottom(tiles, size):
    index = tiles.index(None)
    row = index // size
    row_decs = size - row
    return row_decs

def __is_even(N):
    return N % 2 == 0

def __inversion_count(tiles, size):
    inversion_count = 0
    for i in range(size * size - 1):
        n = tiles[i]
        for j in range(i, size * size - 1):
            n_next = tiles[j+1]
            if n_next is not None and n is not None and n > n_next:
                inversion_count += 1
    return inversion_count


 
if __name__=="__main__": # testing suite
    env = npuzzle.NPuzzle(3) # instance of NPuzzle class
    env.reset()              # random shuffle
    env.visualise()          # just to show the tiles
    # just check
    print(is_solvable(env))  # should output True or False<Paste>
