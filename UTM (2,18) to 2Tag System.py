import time

# Creates Rogozhin's (2,18) UTM and sets up the states translations for a 2-Tag System
states = [None,None]
states[0] = {
    '1'   : ['c2' ,'L',0], # 01 - A
    '1>'  : ['1<1','R',0], # 02 - B
    '1<'  : ['c2' ,'L',0], # 03 - C
    '1>1' : ['1'  ,'R',0], # 04 - D
    '1<1' : ['1>1','L',0], # 05 - E
    'b'   : ['b<' ,'R',0], # 06 - F
    'b>'  : ['b<1','R',0], # 07 - G
    'b<'  : ['b'  ,'L',0], # 08 - H
    'b>1' : ['b'  ,'R',0], # 09 - I
    'b<1' : ['b>1','L',0], # 10 - J
    'b2'  : ['b3' ,'L',1], # 11 - K
    'b3'  : ['b>1','L',1], # 12 - L
    'c'   : ['1>' ,'L',1], # 13 - M
    'c>'  : ['c<' ,'R',0], # 14 - N
    'c<'  : ['c>1','L',0], # 15 - O
    'c>1' : ['c<1','R',1], # 16 - P
    'c<1' : ['HALT',0,-1], # 17 - R
    'c2'  : ['1<' ,'R',0], # 18 - S
}
states[1] = {
    '1'   : ['1<' ,'R',1], # 01 - A
    '1>'  : ['1<' ,'R',1], # 02 - B
    '1<'  : ['1>' ,'L',1], # 03 - C
    '1>1' : ['1<1','R',1], # 04 - D
    '1<1' : ['1'  ,'L',1], # 05 - E
    'b'   : ['b2' ,'R',0], # 06 - F
    'b>'  : ['b<' ,'R',1], # 07 - G
    'b<'  : ['b>' ,'L',1], # 08 - H
    'b>1' : ['b<1','R',1], # 09 - I
    'b<1' : ['b>' ,'L',1], # 10 - J
    'b2'  : ['b'  ,'R',0], # 11 - K
    'b3'  : ['b<1','R',1], # 12 - L
    'c'   : ['c<' ,'R',1], # 13 - M
    'c>'  : ['c<' ,'R',1], # 14 - N
    'c<'  : ['c>' ,'L',1], # 15 - O
    'c>1' : ['c2' ,'R',1], # 16 - P
    'c<1' : ['c2' ,'L',0], # 17 - R
    'c2'  : ['c'  ,'L',1], # 18 - S
}

# Tag Alphabet
'''
    Each letter in the alphabet is a # of '1's 
    The length of the '1's is determed by (len(previous letter) + M - 1)
    where M is the number of tags in the system (in this case 2)
'''
tA = {
    'a' : ['1']   , # Used to input a number to the program
    'E' : ['1']*4 , # Denotes there was an Even number of A
    'O' : ['1']*7 , # Denotes there was an Odd number of A
    '0' : ['1']*10, # A 0 for binary output
    '1' : ['1']*13, # A 1 for binary output
}

# Production Equations
'''
    S
'''
pE = {
    'a' : ['b','b'] + tA['a'],                                                                   # A > A
    'E' : ['b','b'] + tA['O'] + ['1','b'] + tA['E'] + ['1','b'] + tA['0'] + ['1','b'] + tA['0'], # E > 00EO
    'O' : ['b','b'] + tA['O'] + ['1','b'] + tA['E'] + ['1','b'] + tA['1'] + ['1','b'] + tA['1'], # O > 11EO
    '0' : ['b','b'] + tA['0'] + ['1','b'] + tA['0'],                                             # 0 > 00
    '1' : ['b','b'] + tA['1'] + ['1','b'] + tA['1'],                                             # 1 > 11
}

# Input to the Turing Machine
machineInput = (tA['a'] + ['c'])*3  # 3x A

# Set up tape and position in the tape
tape = ['END>', 'c<1', 'c<1'] + pE['1'] + pE['0'] + pE['O'] + pE['E'] + pE['a'] + ['b','b'] + machineInput + tA['E'] + ['c'] + tA['O'] + ['c', '<END']
tagSystem = 0
pos = len(['END>', 'c<1', 'c<1'] + pE['1'] + pE['0'] + pE['O'] + pE['E'] + pE['a'] + ['b','b']) - 1
data = pos + 1


currentRound = 0
runUntil = 10000
saves = [currentRound]
f = open('C:\\Users\\JayMc\\Desktop\\Programing\\My Python\\MTG to computer\\save.txt','w')
currentOut = ''
lastOut = ''

# Main Function
while True:
    currentRound = currentRound + 1
    if (tape[pos] == 'END>'):
        tape.insert(1, '1>')
        pos = pos + 1
    if (tape[pos] == '<END'):
            tape.append('<END')
            tape[pos] = '1<'


    # Ways to print whats happening
    #print('|'.join(str("% 3s" % (e)) for e in (tape[data:]))) # Prints tape thats left of production equations
    currentOut = '|'.join(str("% 3s" % (e)) for e in (tape[data:]))
    if (currentOut != lastOut):
        f.write('|'.join(str("% 3s" % (e)) for e in (tape[1:])) + '\n')
        lastOut = currentOut
    
    # Extra text features
    #print(" " + "    " * (pos-1) + "   | ^ |", end=" ")            # Displays head for referance
    #print(" Pos: " + str(pos) + " Tag: " + str(tagSystem), end="") # Display pos and tagSystem
    #print(" Turn: " + str(currentRound), end="")                   # Display Current Turn
    #print("")                                                      # Endline used to space out each line
    #print("")                                                      # All extra text feature must be used with this


    # Save if I am at the left edge?
    if (tape[pos] == 'c<1'):
        saves.append(currentRound)

    #time.sleep(2) # To make it run slower, can be switched for input

    if ((states[tagSystem].get(tape[pos]))[0] == 'HALT' or (currentRound == runUntil)):
        print("Halt - Program done")
        break

    if (states[tagSystem].get(tape[pos])[1] == 'L'):
        move = -1
    if (states[tagSystem].get(tape[pos])[1] == 'R'):
        move = 1
    tape[pos], tagSystem, pos = states[tagSystem].get(tape[pos])[0], states[tagSystem].get(tape[pos])[2], (pos + move)

print('|'.join(str("% 3s" % (e)) for e in (saves)))
f.close()

'''
tape = ['END>', 'c<1', 'c<1', 'b', 'b', '1', '1', 'b', '1', 'b', 'b', '1', 'c', '1', 'c', '1', 'c','<END']
#notes >>       |P[n+1]       |P[1]                         |P[0]     |A[r]     |A[s]     |A[t]
#        END>,  Halt,         a<a,                          P[0],     aaa,                          <END
tagSystem = 0
pos = 11

Turn 004 goes to part 2
Turn 088 goes to part 3
Turn XXX goes back to 1

A universal Turing machine U simulates a tagSystem-system as follows >
Let T be a tagSystem-system on A = {a[1], . . . , a[n+1]} (A is the alphabet with letters N letters, N+1 is Halt) 
And with productions a[i] -> P[a[i]]. The production is what you append to the end
To each letter a[i] from A is an associated a positive number N[i] and codes a[i] and a~[i] (may be a[i] = a~[i]), of the form U*N[i] (= uu . . . u, N[i] times), 
Where u is a string of symbols of the machine U.
The codes a[i] (or a~[i]) are separated by marks on the tape of U. 
For i from { 1,. . . , n}, the production a[i] -> P[a[i]] == a[i1]a[i2] . . . a[im] of the tagSystem-system T,
is coded by P[i] = A[im[i]],A[im[i]-1] . . .A[i2]A[i1]. (I think its saying the production rules are coded inversely, aka A > AB would be coded BA)
The initial word B = a[r]a[s]a[t] . . . a[w], to be transformed by the tagSystem-system T, 
is coded by S = A[r]A[s]A[t]...A[w] (S = A~[r]A~[s]A~[t]...A~[w]).

This means the intial tape of the UTM is:
Q[L]P[n+1]P[n]...P[1]P[0]A[r]A[s]A[t]...A[w]Q[r] (aka production rules and then word)
where Q[L] and Q[R] are respectively infinite to the left and to the right parts of the tape of the UTM and consist only of blank symbols, 
P[n+1] is the code of the halting symbol a[n+l], 
PO is the additional code consisting of several marks, 
And the head of the UTM is located on the left side of the code S in the state q1 (In UTM(2,18) the head of the UTM is located on the right side of the code PO in the state q1). 

Let T be an arbitrary tagSystem-system, S1 and S2 be the codes of the words B[1] and B[2], respectively, 
And T[B[1]] -> B[2]. Then the UTM U transforms: 
Q[L]P[n+1]P[n]...P[1]lP[0]S[1]Q[R] -> Q[L]P[n+1]P[n]...P[1]P[0]RS[2]Q[R] (R corresponds to the cells which were bearing the codes of the deleted first two symbols))
The work of the UTM can be divided into three stages: 
(i) On the first stage, the UTM searches the code P[r] corresponding to the code A, and then the UTM deletes the codes A[r] and A[s], (i.e. it deletes the mark between them). 
(ii) On the second stage, the UTM writes the code P[r] in Q[r] of the tape in the reversed order. 
(iii) On the third stage the UTM restores its own tape for a new cycle of modelling. 
The number N[i] corresponding to the symbol a[i] of the tagSystem-system has the property that there are exactly N[r] marks at each cycle of modelling between the code P[r] and the code A[r] 
(In UTM(2,18) there are N[r] + 1 marks, but the additional mark in PO is deleted immediately at the beginning of the first stage). 

On the first stage of modelling, the head of the UTM goes through a number of marks in the part P equal to the number of symbols u in the code A[r].
After the first stage the tape of the UTM is Q[L]P[n+1]P[n]...P[r+1]P[r]P'[r-1]...P'[1]P'[0]R'A'[r]A[s]A[t]...A[w]Q[r]
And the head of the UTM locates the mark between A: and A,. 
Then the UTM deletes this mark and the second stage of modelling begins. (c)

After the second stage, the tape of the UTM is Q[L]P[n+1]P[n]...P[r+1]P''[r]P''[r-1]...P''[1]P''[0]R''A[t]...A[w]A[r1]A[r2]...A[rm]Q[r]
and the head of the UTM is located on the left side of P''[r] and the third stage of modelling begins. 

After the third stage, the tape of the UTM is Q[L]P[n+1]P[n]...P[1]P[0]RA[t]...A[w]A[r1]A[r2]...A[rm]Q[r]
 and the head of the UTM is located on the right side of R. (c<1)
 
 The UTM with 2 states and 18 symbols
 m = 2 becase it has 2 states
The Letters > N[1] = 1, N[k+1] = N[k] + m[k] + 1 (aka a = 1, b = 1111, c = 1111111, etc)
The Production > P[a[i]] = a[i1]a[i2]...a[im] is P[i] = bb1*N[im[i]]1b1*N[im[i-1]]...1b1*N[i2]1b1*N[i1] (aka 'bb', letter amount of '1', '1b', ..., letter amount of '1')
'''
