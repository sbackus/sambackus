
import sys
from collections import deque

class LoopError(Exception):
    pass

class SambackusParser(object):
    def __init__(self):
        self.BEGIN = ('sambackus!', 'sambackus?')
        self.END = ('sambackus?', 'sambackus!')
        self.primitives = {('sambackus.', 'sambackus.'): 'inc',
                           ('sambackus!', 'sambackus!'): 'dec',
                           ('sambackus.', 'sambackus?'): 'right',
                           ('sambackus?', 'sambackus.'): 'left',
                           ('sambackus!', 'sambackus.'): 'write',
                           ('sambackus.', 'sambackus!'): 'read'}
                           
    def parse(self, input_text):
        items = input_text.lower().split()
        for i in range(0, len(items), 2):
            x = (items[i], items[i+1])
            if x in self.primitives or x in (self.BEGIN, self.END):
                yield x

class BrainfuckParser(object):
    def __init__(self):
        self.BEGIN = '['
        self.END = ']'
        self.primitives = {'+': 'inc',
                           '-': 'dec',
                           '>': 'right',
                           '<': 'left',
                           '.': 'write',
                           ',': 'read'}
                           
    def parse(self, input_text):
        for x in input_text:
            if x in self.primitives or x in (self.BEGIN, self.END):
                yield x

# TODO: Reimplement with index stack indicating open loops.
# then proceed as in the brainfuck specification.
class Interpreter(object):
    MAX_NESTED_LOOPS = 1000

    def __init__(self, sambackus_mode=True):
        self.bf_parser = BrainfuckParser()
        self.sambackus_parser = SambackusParser()
        self.set_parser(sambackus_mode and self.sambackus_parser or self.bf_parser)

    def reset(self):
        self.cells = deque([0])
        self.index = 0
        self.input_buffer = []
        self.output_buffer = []
        self.open_loops = 0
        self.loop = []

    def inc(self):
        self.cells[self.index] += 1

    def dec(self):
        self.cells[self.index] -= 1

    def right(self):
        self.index += 1
        if self.index >= len(self.cells):
            self.cells.append(0)

    def left(self):
        if self.index == 0:
            self.cells.appendleft(0)
        else:
            self.index -= 1

    def write(self):
        self.output_buffer.append(self.cells[self.index])
            
    def read(self):
        try:
            self.cells[self.index] = int(raw_input("Your input: "))
        except (TypeError, ValueError):
            print "Invalid input! Continuing ..."

    def as_ascii(self):
        return "".join([chr(c) for c in self.output_buffer])

    def set_parser(self, parser):
        self.parser = parser
        self.reset()

    def interpret_raw_text(self, text):
        self.input_buffer.extend(self.parser.parse(text))
        try:
            self.interpret_items(self.input_buffer)
            self.input_buffer = []
        except IndexError:
            print " ... (incomplete)"
        except LoopError:
            print "LoopError ... exiting"
            sys.exit(1)

    def interpret_items(self, items):
        for item in items:
            if self.open_loops:
                self.interpret_inside_loop(item)
            else:
                self.interpret_directly(item)

    def interpret_inside_loop(self, item):
        """
        When inside a loop, we don't want to interpret anything yet,
        but rather 'record' the complete loop. When the number of 
        open loops has become zero (i.e. the initial opening loop
        has been closed), the recorded loop is interpreted as long
        as the current cell is nonzero.
        """

        if item == self.parser.END:
            self.open_loops -= 1
            if self.open_loops == 0:
                while self.cells[self.index]:
                    self.interpret_items(self.loop)
                return
        elif item == self.parser.BEGIN:
            if self.open_loops < self.MAX_NESTED_LOOPS:
                self.open_loops += 1
            else:
                raise LoopError("Nesting maximum (%s) exceeded" 
                                % self.MAX_NESTED_LOOPS)
        self.loop.append(item)

    def interpret_directly(self, item):
        if item == self.parser.END:
            raise ValueError("End without begin")
        elif item == self.parser.BEGIN:
            self.open_loops = 1
            self.loop = []
        elif item in self.parser.primitives:
            method = self.parser.primitives[item]
            getattr(self, method)()
        else:
            print "Unknown token '%s' - ignored" % (item, )

    def interpret_file(self, fname):
        file = open(fname, 'r')
        self.interpret_raw_text(file.read())
        
    def interactive_mode(self):
        print "Sambackus! and Brainfuck interpreter V0.9 - written by Sam Backus in 2014, based on Johannes Charra's ook interpreter"
        print "Type '?' to display the status of the interpreter. "
        print "Type 'b' to enter brainfuck mode. Empty input quits."
        while True:
            inp = raw_input("sb> ").strip()
            if inp == "?":
                print self
            elif inp == "b":
                print "Entering brainfuck mode. Type 'o' to return to Sambackus!"
                self.set_parser(self.bf_parser)
            elif inp == "o":
                print "Entering Sambackus! mode. Type 'b' to return to brainfuck."
                self.set_parser(self.sambackus_parser)
            elif inp == "":
                print self
                break
            else:
                self.interpret_raw_text(inp)

    def __repr__(self):
        rep = "\n".join(["Cells\t\t: %s", 
                         "Input\t\t: %s",
                         "Raw output\t: %s",
                         "ASCII output\t: %s"])

        return rep % (list(self.cells),
                      self.input_buffer,
                      " ".join([str(i) for i in self.output_buffer]), 
                      self.as_ascii())

def print_usage():
    print "\nUsage:\n"
    print "Interpret Sambackus! file: python sambackus.py -o <FILENAME>"        
    print "Interpret brainfuck file: python sambackus.py -b <FILENAME>"
    print "Interactive mode: python sambackus.py -i\n"


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_usage()
    elif len(sys.argv) == 2 and sys.argv[1] == "-i":
        sambackus = Interpreter()
        sambackus.interactive_mode()
    elif len(sys.argv) == 3:
        if sys.argv[1] == "-b":
            sambackus = Interpreter(sambackus_mode=False)
            sambackus.interpret_file(sys.argv[2])
            print sambackus
        elif sys.argv[1] == "-o":
            sambackus = Interpreter(sambackus_mode=True)
            sambackus.interpret_file(sys.argv[2])
            print sambackus
        else:
            print_usage()
    else:
        print_usage()
