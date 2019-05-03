#!/usr/bin/python3

import sys, getopt, numpy, math
#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
# num_hours_i_spent_on_this_assignment = 50
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# <Your feedback goes here>
"""
Took a long time reading the assignment to understand the task. I took a long time understanding the format, what was supposed to be returned, and how it should function. Part 2 also took a very long time to understand. Something that could help improve the value is to give us more test formats, and examples to help us better understand what we should be implementing and what the inputs and outputs should look like.
"""
#####################################################
#####################################################

def main(argv):
   inputfile = ''
   N=0
   try:
      opts, args = getopt.getopt(argv,"hn:i:",["N=","ifile="])
   except getopt.GetoptError:
      print ('sudoku.py -n <size of Sodoku> -i <inputputfile>')
      sys.exit(2)
   for opt, arg in opts:
       if opt == '-h':
           print ('sudoku.py  -n <size of Sodoku> -i <inputputfile>')
           sys.exit()
       elif opt in ("-n", "--N"):
           N = int(arg)
       elif opt in ("-i", "--ifile"):
           inputfile = arg
   instance = readInstance(N, inputfile)
   toCNF(N,instance,inputfile+str(N)+".cnf")




def readInstance (N, inputfile):
    if inputfile == '':
        return [[0 for j in range(N)] for i in range(N)]
    with open(inputfile, "r") as input_file:
        instance =[]
        for line in input_file:
            number_strings = line.split() # Split the line on runs of whitespace
            numbers = [int(n) for n in number_strings] # Convert to integers
            if len(numbers) == N:
                instance.append(numbers) # Add the "row" to your list.
            else:
                print("Invalid Sudoku instance!")
                sys.exit(3)
        return instance # a 2d list: [[1, 3, 4], [5, 5, 6]]


""" Question 1 """
def toCNF (N, instance, outputfile):
    """ Constructs the CNF formula C in Dimacs format from a sudoku grid."""
    """ OUTPUT: Write Dimacs CNF to output_file """
    output_file = open(outputfile, "w")
    "*** YOUR CODE HERE ***"

    sudoku = []
    textout = ""
    
    clauses_num = 0
    
    for x in instance:
        for y in x:
            sudoku.append(y)

    
    for i in range(0, N):
        if(sudoku[i] != '0'):
            x = (i // 9)
            y = (i % 9) + 1
            z = int(sudoku[i]) - 1
            textout += ("%d 0\n" % ((x*N+y)+(z*N*N)))
    #at most once
    for x in range(N):
        for y in range(1,N+1):
            for z in range(N):
                for i in range(z+1,N):
                    textout += ("-%d -%d 0\n" % ((x*N+y)+(z*N*N),(x*N+y)+(i*N*N)))
                    clauses_num += 1
    #least once in each row
    for y in range(1,N+1):
        for z in range(N):
            c = ""
            for x in range(N):
                c += str((x*N+y)+(z*N*N))
                c += " "
            c += "0\n"
            textout += c
            clauses_num += 1
    #once in each column
    for x in range(N):
        for z in range(N):
            c = ""
            for y in range(1,N+1):
                c += str((x*N+y)+(z*N*N))
                c += " "
            c += "0\n"
            textout += (c)
            clauses_num += 1
    #at least once in grid
    for z in range(N):
        for i in range(2):
            for j in range(2):
                c = ""
                for x in range(1,4):
                    for y in range(1,4):
                        X = 3*i+x
                        Y = 3*j+y
                        c += str((x*N+y)+(z*N*N))
                        c += " "
                c += "0\n"
                textout += (c)
                clauses_num += 1

    output_file.write("c " + outputfile + "\n")
    output_file.write("p cnf " + str(N*N*N) + " " + str(clauses_num) + "\n")
    output_file.write(textout)

    "*** YOUR CODE ENDS HERE ***"
    output_file.close()




if __name__ == "__main__":
   main(sys.argv[1:])
