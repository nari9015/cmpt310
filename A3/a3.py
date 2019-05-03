import sys
import random
import math
from math import log

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
num_hours_i_spent_on_this_assignment = 25
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# <Your feedback goes here>
#####################################################
#####################################################



# Outputs a random integer, according to a multinomial
# distribution specified by probs.
def rand_multinomial(probs):
    # Make sure probs sum to 1
    assert(abs(sum(probs) - 1.0) < 1e-5)
    rand = random.random()
    for index, prob in enumerate(probs):
        if rand < prob:
            return index
        else:
            rand -= prob
    return 0

# Outputs a random key, according to a (key,prob)
# iterator. For a probability dictionary
# d = {"A": 0.9, "C": 0.1}
# call using rand_multinomial_iter(d.items())
def rand_multinomial_iter(iterator):
    rand = random.random()
    for key, prob in iterator:
        if rand < prob:
            return key
        else:
            rand -= prob
    return 0

class HMM():
    #0.5*0.169*0.01*0.169
    def __init__(self):
        self.num_states = 2
        self.prior = [0.5, 0.5]
        self.transition = [[0.999, 0.001], [0.01, 0.99]]
        self.emission = [{"A": 0.291, "T": 0.291, "C": 0.209, "G": 0.209},
                         {"A": 0.169, "T": 0.169, "C": 0.331, "G": 0.331}]
        self.seq=[]
    # Generates a sequence of states and characters from
    # the HMM model.
    # - length: Length of output sequence
    def sample(self, length):
        sequence = []
        states = []
        rand = random.random()
        cur_state = rand_multinomial(self.prior)
        for i in range(length):
            states.append(cur_state)
            char = rand_multinomial_iter(self.emission[cur_state].items())
            sequence.append(char)
            cur_state = rand_multinomial(self.transition[cur_state])
        return sequence, states
    
    # Generates a emission sequence given a sequence of states
    def generate_sequence(self, states):
        sequence = []
        for state in states:
            char = rand_multinomial_iter(self.emission[state].items())
            sequence.append(char)
        return sequence
    
    # Computes the (natural) log probability of sequence given a sequence of states.
    def logprob(self, sequence, states):
        ###########################################
        prob =[]
        prob = log(self.prior[states[0]]) + log(self.emission[states[0]][sequence[0]])
        for i in range(1,len(sequence)):
            trans = math.log(self.transition[states[i-1]][states[i]])
            emission = math.log(self.emission[states[i]][sequence[i]])
            prob =  trans + emission + prob
        
        return prob
    # End your code
    ###########################################
    
    
    # Outputs the most likely sequence of states given an emission sequence
    # - sequence: String with characters [A,C,T,G]
    # return: list of state indices, e.g. [0,0,0,1,1,0,0,...]
    def viterbi(self, sequence):
        seq = []
        ###########################################
        # Start your code
        P = [[0 for x in range(2)] for y in range(len(sequence))]
        prev= [[0 for x in range(2)] for y in range(len(sequence))]

        P[0][0]= log(self.prior[0]) + log(self.emission[0][sequence[0]])
        P[0][1] = log(self.prior[1]) + log(self.emission[1][sequence[0]])
        
        
        for i in range(1,len(sequence)):
            #emission prob for rich and low regions
            prob_r = log(self.emission[1][sequence[i]])
            prob_l = log(self.emission[0][sequence[i]])
            
            #transition prob for rich and low regions
            P[i][0] = prob_l + max(P[i-1][0] + log(self.transition[0][0]) , P[i-1][1] + log(self.transition[1][0]))
            P[i][1] = prob_r + max(P[i-1][1] + log(self.transition[1][1]) , P[i-1][0] + log(self.transition[0][1]))
            
            #calculate if low or high state
            prev[i][0] =  0 if  max(P[i-1][0] + log(self.transition[0][0]), P[i-1][1] + log(self.transition[1][0])) == (P[i-1][0] + log(self.transition[0][0])) else 1
            prev[i][1] =  0 if max(P[i-1][1] + log(self.transition[1][1]), P[i-1][0] + log(self.transition[0][1])) == P[i-1][0] + log(self.transition[0][1]) else 1
        
        #assemble the seq
        last = P[len(P)-1]
        start = 0
        #determine end of seq    
        if(max(last[0],last[1])) == last[0]:
            start = 0
            seq.append(0)
        else:
            start = 1
            seq.append(1)
        #assemble rest of seq
        lp = len(prev)-1
        for i in range(lp,0,-1):
            val = prev[i][start]
            seq.append(val)
            start = val
        #flip seq
        seq.reverse()
        return seq

    # need to consider transition probabilities

def read_sequence(filename):
    with open(filename, "r") as f:
        return f.read().strip()

def write_sequence(filename, sequence):
    with open(filename, "w") as f:
        f.write("".join(sequence))

def write_output(filename, logprob, states):
    with open(filename, "w") as f:
        f.write(str(logprob))
        f.write("\n")
        for state in range(2):
            f.write(str(states.count(state)))
            f.write("\n")
        f.write("".join(map(str, states)))
        f.write("\n")

hmm = HMM()

file = sys.argv[1]
sequence = read_sequence(file)
viterbi = hmm.viterbi(sequence)
logprob = hmm.logprob(sequence, viterbi)
print (logprob)
name = "my_"+file[:-4]+'_output.txt'
write_output(name, logprob, viterbi)



