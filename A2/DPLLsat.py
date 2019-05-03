#!/usr/bin/python3

import sys, getopt, random

class SatInstance:
    def __init__(self):
        pass
    def from_file(self, inputfile):
        self.clauses = list()
        self.VARS = set()
        self.p = 0
        self.cnf = 0
        with open(inputfile, "r") as input_file:
            self.clauses.append(list())
            maxvar = 0
            for line in input_file:
                tokens = line.split()
                if len(tokens) != 0 and tokens[0] not in ("p", "c"):
                    for tok in tokens:
                        lit = int(tok)
                        maxvar = max(maxvar, abs(lit))
                        if lit == 0:
                            self.clauses.append(list())
                        else:
                            self.clauses[-1].append(lit)
                if tokens[0] == "p":
                    self.p = int(tokens[2])
                    self.cnf = int(tokens[3])
            assert len(self.clauses[-1]) == 0
            self.clauses.pop()
            if not (maxvar == self.p):
                print("Non-standard CNF encoding!")
                sys.exit(5)
      # Variables are numbered from 1 to p
        for i in range(1,self.p+1):
            self.VARS.add(i)
    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s



def main(argv):
   inputfile = ''
   verbosity=False
   inputflag=False
   try:
      opts, args = getopt.getopt(argv,"hi:v",["ifile="])
   except getopt.GetoptError:
      print ('DPLLsat.py -i <inputCNFfile> [-v] ')
      sys.exit(2)
   for opt, arg in opts:
       if opt == '-h':
           print ('DPLLsat.py -i <inputCNFfile> [-v]')
           sys.exit()
    ##-v sets the verbosity of informational output
    ## (set to true for output veriable assignments, defaults to false)
       elif opt == '-v':
           verbosity = True
       elif opt in ("-i", "--ifile"):
           inputfile = arg
           inputflag = True
   if inputflag:
       instance = SatInstance()
       instance.from_file(inputfile)
       solve_dpll(instance, verbosity)
   else:
       print("You must have an input file!")
       print ('DPLLsat.py -i <inputCNFfile> [-v]')


""" Question 2 """
# Finds a satisfying assignment to a SAT instance,
# using the DPLL algorithm.
# Input: a SAT instance and verbosity flag
# Output: print "UNSAT" or
#    "SAT"
#    list of true literals (if verbosity == True)
#    list of false literals (if verbosity == True)
#
#  You will need to define your own
#  solve(VARS, F), pure-elim(F), propagate-units(F), and
#  any other auxiliary functions

def count(F): #count number of occurrances of each val
    counter = {}
    for c in F:
        for x in c:
            if x in counter:
                counter[x] += 1
            else:
                counter[x] = 1
    return counter

def removeClause(F, unit):
    modified = []
    for clause in F:
        if unit in clause: continue #remove all clauses containing same unit
        if -unit in clause:
            c = []
            for x in clause:
                if x != -unit:
                    c.append(x)
            if len(c) == 0: return -1 #unsat
            modified.append(c)
        else:
            modified.append(clause)
    return modified

def propagate_units(F):
    vars = []
    unit_clauses = [x for x in F if len(x) == 1] #add as unit if clause length is 1
    while len(unit_clauses) > 0: #while there are unit clauses
        unit = unit_clauses[0]
        F = removeClause(F, unit[0]) #remove all clauses containing unit
        vars += [unit[0]]
        if F == -1:
            return -1, []
        if not F:
            return F, vars
        unit_clauses = [x for x in F if len(x) == 1] #recalculate unit clauses
    return F, vars

def pure_elim(F):
    vars = []
    pures = []
    counter = count(F)
    for l, y in counter.items():
        if -l not in counter: pures.append(l) #no negated values, then add as pure
    for pure in pures:
        F = removeClause(F, pure) #remove all clauses containing unit
    vars += pures
    return F, vars

def solve(vars, F):
    F, pure = pure_elim(F) #pure literal elimination
    F, unit = propagate_units(F) #unit propogation

    vars += (unit + pure)
    if F == - 1:
        return []
    if not F:
        return vars
    
    #random variable selection
    counter = count(F)
    var = random.choice(counter.keys())

    #recursive call
    solution = solve(vars + [var], removeClause(F, var))
    if not solution:
        solution = solve(vars + [-var], removeClause(F, -var))
    return solution

def format_output(F):
    true_l = []
    false_l = []
    literals = F
    
    for var in F:
        if var > 0:
            true_l.append(var)
        else:
            false_l.append(var)
    print(str(true_l))
    print(str(false_l))

def solve_dpll(instance, verbosity):
#    print(instance)
    #print(instance.VARS)
    #print(verbosity)
    ###########################################
    # Start your code
    clauses = instance.clauses
    solution = solve([], clauses)
    
    if solution:
        print ("SAT")
        if verbosity==True:
            format_output(solution)
    else:
        print ("UNSAT")

    # End your code
    return True
    ###########################################


if __name__ == "__main__":
   main(sys.argv[1:])
