import sys
from parser import parse
from memory import Memory
from allocation_algorithms import *

#=============================================================================
MAIN_MEM  = 1600
OS_MEM    = 80
#=============================================================================

def run_simulation( plist, algorithm = None, quiet = True):
    """
    Runs 'first', 'best', 'next' or 'worst' algorithm on a list of processes. 
    If 'quiet', then there is no user interaction.
    """
    TIME = time = 0

    END  = max( [p.exit_time for p in plist] )
    M = Memory(MAIN_MEM, OS_MEM, plist)
    M.display(t=TIME)

    # Outer loop to take input from the user. 
    while(True):

        if (not quiet):
            try:
                time = int( input('Enter time to view memory configuration:' ) )
                if (time == 0): 
                    break
            except:
                break

        # Inner loop to run the simulation.
        while ( TIME < END ):

            TIME += 1

            changed = 0
            changed += M.remove_all(plist, TIME )
            changed += M.add_all(plist, TIME, algorithm, quiet = quiet)

            if (not quiet and time == TIME):
                break

            if (changed > 0 and quiet):
                M.display(t=TIME)

        # If the user is controlling the loop, just continue.
        if (not quiet):
            M.display(t=TIME)
            #M = Memory(MAIN_MEM, OS_MEM, plist)
            #TIME = 0
            continue

        break


if __name__ == "__main__":

    # Simple error checking.
    if (len(sys.argv) < 3):
        print("USAGE: {} <input-file> [ first | best | next"
        "| worst | noncontig ]".format(sys.argv[0]))
        sys.exit(1)

    # Make sure user entered a supported algorithm and text file.
    alg_loc = text_loc = -1
    for kword in ["first", "best", "next", "worst", "noncontig"]:
        if kword in sys.argv:
            alg_loc = sys.argv.index(kword)
            break

    for i in range(len(sys.argv)):
        if (sys.argv[i].endswith('.txt')):
            text_loc = i

    if (alg_loc == -1 or text_loc == -1):
        print("USAGE: {} <input-file.txt> [ first | best | next "
        "| worst | noncontig ]".format(sys.argv[0]))
        sys.exit(1)

    else:
        # Check for '-q' flag.
        q = '-q' in sys.argv

        # Map keywords to their corresponding functions.
        lookup = {
                'first': first_fit, 
                'best': best_fit, 
                'worst': worst_fit,
                'noncontig': noncontig, 
                }

        f = None
        plist = parse( sys.argv[text_loc] )

        # Special case for next, since it needs a closure.
        if ( sys.argv[alg_loc] == 'next' ):
            tmp = Memory(MAIN_MEM, OS_MEM, plist)
            f = get_next_fit(tmp)

        else:
            f = lookup[ sys.argv[alg_loc] ]

        run_simulation(plist, algorithm = f, quiet = q)

