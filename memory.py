from pprint import pprint
import sys 

class Memory:

    def __init__(self, main_mem_size = 1600, os_proc_size = 80, plist = None):
        """
        Initialize memory as a list with mem_size empty entries.
        The first os_proc_size entries are marked with '#'.
        """
        self.main_mem = main_mem_size
        self.os_mem = os_proc_size

        self.memory = ['#' if i < os_proc_size else '.' 
                for i in range(main_mem_size)]

        if (plist is not None):
            self.load(plist)

    def load(self, plist):
        """
        Load all processes starting at time 0 into memory using
        contiguous memory allocation.
        """
        for p in plist:
            if (p.arrival_time != 0):
                continue
            for i in range(p.memory):
                for j in range(self.main_mem):
                    if self.memory[j] == '.':
                        self.memory[j] = p.name
                        break

    def add(self, p, method):
        """
        Add a process p to memory according to function 'method'. 
        Returns 1 on success, and 0 to indicate OUT-OF-MEMORY error.
        """
        blocks = method(self, p)

        if (not blocks):
            return 0

        for b in blocks:
            self.memory[b] = p.name

        return 1

    def remove(self, p):
        """Remove a process p from memory."""
        for i in range(self.main_mem):
            if (self.memory[i] == p.name):
                self.memory[i] = '.'

    def add_all(self, plist, t, method = None):
        """
        Call add() on all processes arriving at time t. Returns
        total number of processes added.
        """
        added = 0
        for p in plist:
            if p.arrival_time == t:
                rc = self.add(p, method)

                # If the add was unsuccessful, defragment and try again.
                if (rc == 0):
                    self.defragment()

                    #If a defragment did not help, game over.
                    rc = self.add(p, method)
                    if (rc == 0):
                        print("ERROR: OUT-OF-MEMORY. SIMULATION EXITING...")
                        sys.exit(1)
                        
                added += 1

        return added

    def remove_all(self, plist, t):
        """
        Call remove() on all processes leaving at time t. Returns total
        number of processes removed.
        """
        removed = 0
        for p in plist:
            if p.exit_time == t:
                self.remove(p)
                removed += 1

        return removed

    def display(self, linebreak = 80, t = 0):
        """Display memory, with linebreak characters per line"""
        print("Memory at time {}:".format(t), end = "")
        for i in range(len(self.memory)):
            if (i % self.os_mem  == 0):
                print()
            print(self.memory[i], end="")

        print()

    def defragment(self):
        """
        Shift all processes in memory as far left as possible. Display
        data about the state of memory afterward.
        """

        pset = set()

        for i in range(len(self.memory) - 1):
            for j in range(i, len(self.memory) - 1):
                if (self.memory[i] == '.'):

                    self.memory[i], self.memory[i+1] = \
                    self.memory[i+1], self.memory[i]

                    # If a process has moved, add it to the pset
                    if (self.memory[i] != '.'):
                        pset.add(self.memory[i])

        free = sum([1 for i in self.memory if i == '.'])

        print("Relocated {0} processes to create a free memory block of"
                " {1} units ({2:.2f}% of total memory).".format(
                    len(pset), free, 100*free/len(self.memory)))

if __name__ == '__main__':
    m = Memory(1600, 80)
    m.display()
    m.defragment()



