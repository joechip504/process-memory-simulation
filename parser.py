class Process:
    """Simple class to represent one instance of a process"""

    def __init__(self, name_, memory_, arrives, exits):
        self.arrival_time = int(arrives)
        self.exit_time = int(exits)
        self.name = name_
        self.memory = int(memory_)

    def __lt__(self, other):
        return self.arrival_time < other.arrival_time

    def __str__(self):
        return "{:<5}  MEMORY: {:<10} ARRIVES: {:<10}  EXITS: {:<10}".format(
                self.name, self.memory, self.arrival_time, self.exit_time)

def parse(f_name):
    """
    Parse an input file and return a list of Process objects. A new
    process object is created each time a process would enter/exit
    memory. The plist is sorted by arrival_time.
    """
    plist = []
    contents = open(f_name).read().replace("\t", " ").split('\n')

    for line in contents:
        try:
            line = line.split()
            letter, memory = line[0], line[1]

            for i in range(2, len(line), 2):
                plist.append(Process(letter, memory, line[i], line[i+1]))

        except:
            continue


    return sorted(plist)

if __name__ == "__main__":
    l = parse("input1.txt")
    for i in l:
        print(i)
