from parser import parse
from memory import Memory
from allocation_algorithms import *

#=============================================================================
MAIN_MEM = 1600
#MAIN_MEM = 340 
OS_MEM   = 80
#=============================================================================

def run_simulation( plist, algorithm = None, quiet = True, time = 0 ):
    """
    Runs 'first', 'best', 'next' or 'worst' algorithm on a list of processes. 
    If 'quiet', then there is no user interaction.
    """
    TIME = 0
    END  = max( [p.exit_time for p in plist] )

    M = Memory(MAIN_MEM, OS_MEM, plist)
    M.display(t=TIME)

    while ( TIME < END ):

        TIME += 1

        if (not quiet and time == TIME):
            break

        changed = 0
        changed += M.remove_all(plist, TIME)
        changed += M.add_all(plist, TIME, algorithm)

        if (changed > 0 and quiet):
            M.display(t=TIME)

    if (not quiet):
        M.display(t=TIME)


if __name__ == "__main__":
    f_name = "input1.txt"
    plist = parse(f_name)
    #run_simulation(plist, algorithm = first_fit)
    #run_simulation(plist, algorithm = worst_fit)
    #run_simulation(plist, algorithm = best_fit)
    #run_simulation(plist, algorithm = noncontig)
