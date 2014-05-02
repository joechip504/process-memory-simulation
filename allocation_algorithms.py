from parser import parse, Process
from memory import Memory

def first_fit( M, p ):
    """
    Takes in a memory configuration and a process, and returns a list of
    free locations in memory corresponding to the placement of p in 
    memory. Returns an empty list upon failure.
    """
    for i in range( len(M.memory) ):
        blocks = []
        for j in range( p.memory ):
            if (M.memory[i+j] != "."):
                break
            blocks.append( i + j )

            if len(blocks) == p.memory:
                return blocks

            if (i + j == len(M.memory) - 1):
                break

    return []

def worst_fit( M, p ):
    """
    Searches a configuration for the largest block of unallocated memory
    and attempts to place P. Returns an empty list upon failure.
    """

    # Find the largest free block and the index in M where it begins.
    block_size, begins = 0, 0
    for i in range( len(M.memory) ):
        candidate_block_size = 0
        for j in range( len(M.memory) - i):
            if (M.memory[i+j] == '.'):
                candidate_block_size += 1
            else:
                break


        if (candidate_block_size > block_size):
            block_size, begins = candidate_block_size, i

        if (i + block_size == len(M.memory)):
            break

    # If the block is large enough to hold P, place it.
    if (block_size < p.memory):
        return []
    
    return [begins + i for i in range(p.memory)]

def best_fit( M, p ):
    """
    Searches a configuration for the smallest block of unallocated memory
    and attempts to place P. Returns an empty list upon failure.
    """
    block_size, begins = M.main_mem + 1, 0

    # i scans through Memory m, and j indicates the start of a block
    i, j, candidate_block_size = 0, 0, 0
    while (i < M.main_mem):
        if (M.memory[i] == '.'):
            candidate_block_size += 1

        else:
            if (candidate_block_size < block_size and
                    candidate_block_size >= p.memory):
                block_size, begins = candidate_block_size, j 

            candidate_block_size = 0
            j = i+1

        i += 1

    if (candidate_block_size < block_size and
                        candidate_block_size >= p.memory):
                    block_size, begins = candidate_block_size, j 

    if (block_size < p.memory):
        return []
    
    return [begins + i for i in range(p.memory)]

def noncontig(M, p):
    """
    Allocate frames in any order. If an OUT-OF-MEMORY error occurs, bail
    out completely instead of returning an empty list, since defragmenting
    won't help.
    """
    free = sum( [1 for i in M.memory if i == '.'] )

    if (free < p.memory):
        print("ERROR: OUT-OF-MEMORY. SIMULATION EXITING...")
        sys.exit(1)

    config = []
    for i in range(len(M.memory)):
        if (len(config) == p.memory):
            break
        if (M.memory[i] == '.'):
            config.append(i)

    return config

def get_next_fit( M ):
    """
    To remember the previous call of the function, wrap next_fit in a closure. 
    i_ is the index where the search left off. Start i_ at the first free
    index in memory, if one is available.
    """
    i_ = 0
    while ( i_ < M.main_mem ):
        if (M.memory[i_] == '.'):
            break

        i_ += 1

    def next_fit(M, p):
        nonlocal i_
        visited = 0
        blocks = []

        while (True):

            if (len(blocks) == p.memory):
                return blocks

            elif M.memory[i_ % M.main_mem] == '.':
                blocks.append(i_ % M.main_mem)

            else:
                blocks = []

            i_ += 1
            visited += 1

            # If we've come full circle, set i back to it's original value
            # and bail out.
            if (visited == M.main_mem):
                i_ -= M.main_mem
                break

        if (len(blocks) == p.memory):
            return blocks
        else:
            return []

    return next_fit

if __name__ == '__main__':
    pass
    #f_name = "input1.txt"
    #plist = parse(f_name)
