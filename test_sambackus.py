
import unittest
from sambackus import Interpreter, SambackusParser, BrainfuckParser

TEST_STRING_GC = """
    sambackus. sambackus. sambackus. sambackus. sambackus. sambackus. sambackus. sambackus. sambackus! sambackus.
    sambackus. sambackus. sambackus. sambackus. sambackus. sambackus. sambackus. sambackus. sambackus! sambackus.
    sambackus. sambackus? sambackus! sambackus.
    sambackus. sambackus. sambackus! sambackus.
    sambackus! sambackus.
    sambackus! sambackus.
    sambackus! sambackus! sambackus! sambackus.

    sambackus. sambackus. sambackus. sambackus. sambackus. sambackus. sambackus. sambackus.
    sambackus! sambackus?
    sambackus. sambackus? sambackus. sambackus. sambackus. sambackus? sambackus. sambackus. sambackus. sambackus. sambackus? sambackus. sambackus? sambackus. sambackus! sambackus!
    sambackus? sambackus!
    sambackus. sambackus? sambackus. sambackus? sambackus! sambackus! sambackus! sambackus.
    sambackus? sambackus. sambackus! sambackus.
    sambackus. sambackus? sambackus! sambackus! sambackus! sambackus.
    sambackus. sambackus. sambackus. sambackus. sambackus. sambackus. sambackus! sambackus.
    sambackus! sambackus! sambackus! sambackus.
    sambackus? sambackus. sambackus! sambackus.
"""

GC_OUTPUT = [4, 8, 0, 1, 1, 1, 0, 7, 4, 6, 9, 8, 4]

class SambackusParserTest(unittest.TestCase):
    def test_sambackusparser(self):
        parser = SambackusParser()
        li = list(parser.parse("sambackus. SamBackus. Sambackus! SaMBaCKus?"))
        assert li == [("sambackus.", "sambackus."), ("sambackus!", "sambackus?")], "List is %s" % li

class BrainfuckParserTest(unittest.TestCase):
    def test_bfparser(self):
        parser = BrainfuckParser()
        li = list(parser.parse("++++"))
        assert li == ["+", "+", "+", "+"], "List is %s" % li

class SambackusTest(unittest.TestCase):
    def setUp(self):
        self.sambackus = Interpreter()

    def test_incdec(self):
        self.sambackus.interpret_items([("sambackus.", "sambackus.")])
        assert list(self.sambackus.cells) == [1], "Inc failed"
        self.sambackus.interpret_items([("sambackus!", "sambackus!")])
        assert list(self.sambackus.cells) == [0], "Dec failed"

    def test_leftright(self):
        self.sambackus.interpret_items([("sambackus.", "sambackus?")])
        assert list(self.sambackus.cells) == [0, 0], "Right failed"
        assert self.sambackus.index == 1, "Index move to the right failed"
        self.sambackus.interpret_items([("sambackus?", "sambackus.")])
        assert list(self.sambackus.cells) == [0, 0], "Left failed"
        assert self.sambackus.index == 0, "Index move to the left failed"
        self.sambackus.interpret_items([("sambackus?", "sambackus.")])
        assert list(self.sambackus.cells) == [0, 0, 0], "Left failed"
        assert self.sambackus.index == 0, "Index move to the left failed"

    def test_raw_inc(self):
        self.sambackus.interpret_raw_text("sambackus. sambackus.")
        assert list(self.sambackus.cells) == [1], "Raw inc failed"

    def test_javaner(self):
        self.sambackus.interpret_raw_text(TEST_STRING_GC)
        assert self.sambackus.output_buffer == GC_OUTPUT, "Output is %s instead of %s" % (self.sambackus.output_buffer, GC_OUTPUT)

    def test_helloworld(self):
        self.sambackus.interpret_file('sambackustest.txt')
        assert self.sambackus.as_ascii() == 'Hello World!', 'Helloworld failed: %s' % self.sambackus.as_ascii()

    def test_simple_loop(self):
        self.sambackus.interpret_raw_text("sambackus. sambackus. sambackus! sambackus? sambackus! sambackus! sambackus? sambackus! sambackus! sambackus.")
        assert self.sambackus.output_buffer == [0], self.sambackus.output_buffer

    def test_nested_loop(self):
        self.sambackus.interpret_raw_text("sambackus. sambackus. sambackus! sambackus? "
                                    "sambackus. sambackus. sambackus! sambackus? "
                                    "sambackus! sambackus! sambackus? sambackus! sambackus? sambackus! sambackus! sambackus.")
        assert self.sambackus.output_buffer == [0], self.sambackus.output_buffer

    def test_squares(self):
        self.sambackus.interpret_file('squares.sambackus')
        assert "10000" in self.sambackus.as_ascii(), "Output squares: %" % self.sambackus.as_ascii()

class BFTest(unittest.TestCase):
    def setUp(self):
        self.bf = Interpreter(sambackus_mode=False)

    def test_incdec(self):
        self.bf.interpret_items(["+"])
        assert list(self.bf.cells) == [1], "Inc failed"
        self.bf.interpret_items(["-"])
        assert list(self.bf.cells) == [0], "Dec failed"

    def test_leftright(self):
        self.bf.interpret_items([">"])
        assert list(self.bf.cells) == [0, 0], "Right failed"
        assert self.bf.index == 1, "Index move to the right failed"
        self.bf.interpret_items(["<"])
        assert list(self.bf.cells) == [0, 0], "Left failed"
        assert self.bf.index == 0, "Index move to the left failed"

    def test_raw_inc(self):
        self.bf.interpret_raw_text("+")
        assert list(self.bf.cells) == [1], "Raw inc failed"

    def test_helloworld(self):
        self.bf.interpret_file('bftest.txt')
        assert self.bf.as_ascii() == "Hello World!\n", "Helloworld failed: '%s'" % self.bf.as_ascii()

    def test_simple_loop(self):
        self.bf.interpret_raw_text("+[-].")
        assert self.bf.output_buffer == [0], self.bf.output_buffer

    def test_nested_loop(self):
        self.bf.interpret_raw_text("+[+[-]].")
        assert self.bf.output_buffer == [0], self.bf.output_buffer
        
    def test_ignore_whitespace(self):
        self.bf.interpret_raw_text("   +   +   +      -  - ")
        assert list(self.bf.cells) == [1], "List is %s" % list(self.bf.cells)

if __name__ == '__main__':
    unittest.main()
