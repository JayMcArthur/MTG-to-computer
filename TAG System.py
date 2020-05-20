
class twoTag:
    def __init__ (self, tape, dictionary):
        self.tape = tape
        self.dict = dictionary

    def step(self):
        self.tape = self.tape[2:] + self.dict[self.tape[0]]

    def run(self, out = 0):
        while self.dict[self.tape[0]] != '!HALT':
            if out == 1:
                input(self.returnTape())
            self.step()
        return self.tape[1:]

    def encode(self, num):
        return 'x'*num

    def returnTape(self):
        return self.tape

decToBin = {
    'x':'x',
    'E':'EO00',
    'O':'EO11',
    '0':'00',
    '1':'11',
    'H':'!HALT'
}

tm = twoTag('x'*4 + 'EO', decToBin)
print(tm.run(1))

'''
/** Commentary:
 * 
 * The below code provides a simulator for a simple
 * "Is N even or odd" 2-tag system, and an embedding
 * for that tag system in UTM 2,18.
 * 
 * The tag system works as follows:
 * 
 * First, encode a "tape" of "x" repeated N times,
 * followed by "eo".
 * 
 * Then, step by step, read the head of the tape,
 * delete two symbols (the 2 in 2-tag), and depending
 * on the value read, write new values to the end
 * of the tape.
 * 
 * If you read an x, write "xx",
 * If you read an e, write "He",
 * If you read an o, write "xHo",
 * If you read an H, halt.
 * 
 * The first non-H character on the tape will be
 * either an e or an o, depending on if the input
 * number was even or odd.
 * 
 * The turing machine works as follows:
 * 
 * The turing tape starts initialized with two pieces:
 * 
 * P - the "program" that describes this 2-tag system
 *     (as opposed to any other)
 * S - the "starting" tape
 * 
 * So, the P would encode the "if you read _, write _"
 * table from above, while the S would encode the number
 * you wanted to test for parity.
 * 
 * Here is an example starting tape for "Is 1 even or odd?"
 * 
 * rrffaaaaaaaafaaaaaaaaaaaafaffaaaaafaaaaaaaaaaaffaafaffamaaaamaaaaaaam
 *                                                      ^----(state: q1)
 * 
 * To explain each chunk, I'm going to break it up like this:
 * 
 * rr ffaaaaaaaafaaaaaaaaaaaafa ffaaaaafaaaaaaaaaaa ffaafa ff amaaaamaaaaaaam
 *                                                          ^----(q1)
 * 
 * On the tape,
 * 
 * "x" gets encoded as a single Aetherborn token,
 * "e" gets encoded as 4 Aetherborn token
 * "o" gets encoded as 7 Aetherborn token
 * "H" gets encoded as 11 Aetherborn token
 * 
 * In the "program" section, the symbols within a single
 * rule are separated by an Aetherborn / Faerie pair, and
 * each rule is separated by two faeries.
 * 
 * In the "tape" section, each symbol is separated by a
 * Myr token.
 * 
 * The tape starts with two Rhino tokens, which halt
 * the program.
 * 
 * It then encodes each non-halting production rule in reverse order:
 * 
 * o:
 * ff aaaaaaa af aaaaaaaaaaa af a
 *       o            H         x
 * 
 * e:
 * ff aaaa af aaaaaaaaaaa
 *    --e-    ----H------
 * 
 * x:
 * ff a af a
 *    x    x
 * 
 * They are in reverse order, because the turing head is
 * going to "bounce" back and forth between these symbols
 * and the end of the tape transcribing them.
 * 
 * The end of execution may look something like this:
 * 
 * rsggbbbbbbbbgbbbbbbbbbbbbgbggbbbbbgbbbbbbbbbbbggbbgbggbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbaaaaaaamamam
 * ^----(H, 6002)
 * 
 * After 6002 steps of the turing machine, it encountered
 * a symbol on the tape which did not have a production
 * rule, and thus halted.  Most of the tape at this point
 * is filled with computational debris, but notice the end:
 * 
 * aaaaaaamamam
 *    o    x x
 * 
 * This corresponds to an oxx being written on the tape,
 * resulting on an answer of odd.
 * 
 * Compare this to the (end of the) end state for runTuring(2):
 * 
 * aaaamamam
 *   e  x x
 * 
 * Correctly stating that 2 is even.
 * 
 * As a curiosity, the simulation will also keep track of
 * how many in-game turns would be needed to simulate this:
 *  - 4 turns per step of the turing machine if we don't change state
 *  - 3 turns per step if we DO change state
 *  - 3 turns on the turn we halt
 *  - 1 turn of setup
 * 
 * To compute if 0 is even or odd, it takes 10412 turns.
 * To compute if 1 is even or odd, it takes 23974 turns.
 * To compute if 2 is even or odd, it takes 16216 turns.
 */




/* UTM(2,18) */

var symbols = "abcdefghijklmnoprs";
var states = "12";
//                  x  e  o  H
var N = [undefined, 1, 4, 7, 11];

function A(i) {
  return "a".repeat(N[i]);
}

function _P(out) {
  let encoding = "ff";
  for(let i = out.length - 1; i >= 0; i--) {
    encoding += A(out[i]);
    if(i != 0) {
      encoding += "af";
    }
  }
  return encoding;
}
function P(i) {
  if(i == undefined) {
    return P(4) +
      P(3) +
      P(2) +
      P(1) +
      P(0);
  }
  if(i == 0) {
    return "ff";
  }
  if(i == 1) {
    return _P([1,1]);
  }
  if(i == 2) {
    return _P([4, 2]);
  }
  if(i == 3) {
    return _P([1, 4, 3]);
  }
  if(i == 4) {
    return "rr";
  } 
}
function S(num) {
  return (A(1) + "m").repeat(num) +
    A(2) + "m" + A(3) + "m";
}
function initialTape(num) {
  return P() + S(num);
}

function initialHead(num) {
  return P().length - 1;
}

function initialState() {
  return 'q1';
}

var utm218 = {
  q1: {
    a: { w: 's', d: 'L', s: 'q1' },
    b: { w: 'e', d: 'R', s: 'q1' },
    c: { w: 's', d: 'L', s: 'q1' },
    d: { w: 'a', d: 'R', s: 'q1' },
    e: { w: 'd', d: 'L', s: 'q1' },
    f: { w: 'h', d: 'R', s: 'q1' },
    g: { w: 'j', d: 'R', s: 'q1' },
    h: { w: 'f', d: 'L', s: 'q1' },
    i: { w: 'f', d: 'R', s: 'q1' },
    j: { w: 'i', d: 'L', s: 'q1' },
    k: { w: 'l', d: 'L', s: 'q2' },
    l: { w: 'i', d: 'L', s: 'q2' },
    m: { w: 'b', d: 'L', s: 'q2' },
    n: { w: 'o', d: 'R', s: 'q1' },
    o: { w: 'p', d: 'L', s: 'q1' },
    p: { w: 'r', d: 'R', s: 'q2' },
    r: { w: 'H', d: 'H', s: 'H' },
    s: { w: 'c', d: 'R', s: 'q1' },
  },
  q2: {
    a: { w: 'c', d: 'R', s: 'q2' },
    b: { w: 'c', d: 'R', s: 'q2' },
    c: { w: 'b', d: 'L', s: 'q2' },
    d: { w: 'e', d: 'R', s: 'q2' },
    e: { w: 'a', d: 'L', s: 'q2' },
    f: { w: 'k', d: 'R', s: 'q1' },
    g: { w: 'h', d: 'R', s: 'q2' },
    h: { w: 'g', d: 'L', s: 'q2' },
    i: { w: 'j', d: 'R', s: 'q2' },
    j: { w: 'g', d: 'L', s: 'q2' },
    k: { w: 'f', d: 'R', s: 'q1' },
    l: { w: 'j', d: 'R', s: 'q2' },
    m: { w: 'o', d: 'R', s: 'q2' },
    n: { w: 'o', d: 'R', s: 'q2' },
    o: { w: 'n', d: 'L', s: 'q2' },
    p: { w: 's', d: 'R', s: 'q2' },
    r: { w: 's', d: 'L', s: 'q1' },
    s: { w: 'm', d: 'L', s: 'q2' },
  }
}

function stepTuring(machine) {
  var read = machine.tape[machine.head];
  var inst = utm218[machine.state][read];
  var next = {
    steps: machine.steps + 1,
    turns: machine.turns + (machine.state == inst.s ? 4 : 3),
    state: inst.s,
    tape: machine.tape.slice(),
    head: machine.head,
  };

  if(inst.w == 'H') {
    return next;
  }

  next.tape = 
    next.tape.slice(0,machine.head) +
    inst.w +
    next.tape.slice(machine.head+1);
  var head = machine.head;
  switch(inst.d) {
    case 'L': {
      if(head == 0) {
        next.tape = 'c' + next.tape;
        head++;
      }
      head--;
    } break;
    case 'R': {
      if(head == next.tape.length - 1) {
        next.tape += 'c';
      }
      head++;
    } break;
  }
  next.head = head;

  return next;
}

function runTuring(num, steps) {
  var machine = {
    steps: 0,
    turns: 1,
    tape: initialTape(num),
    head: initialHead(num),
    state: initialState(),
  }
  console.log(machine.tape);
  console.log(' '.repeat(machine.head) + '^----(' + machine.state + ')');
  while(
    machine.state != 'H' &&
    (!steps || machine.steps < steps)) {
    machine = stepTuring(machine);
    
    console.log(machine.tape);
    console.log(' '.repeat(machine.head) + '^----(' + machine.state + ', ' + machine.steps + ')')
  }
  console.log(machine.tape);
  console.log(' '.repeat(machine.head) + '^----(' + machine.state + ', ' + machine.steps + ')')
  console.log('Turns: ', machine.turns);
}

'''