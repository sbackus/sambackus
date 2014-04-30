
import unittest
from bf import convertSambackusToBF

sambackus2bf = {('sambackus.', 'sambackus.'): '+',
          ('sambackus!', 'sambackus!'): '-',
          ('sambackus!', 'sambackus.'): '.',
          ('sambackus.', 'sambackus!'): ',',
          ('sambackus.', 'sambackus?'): '>',
          ('sambackus?', 'sambackus.'): '<',
          ('sambackus!', 'sambackus?'): '[',
          ('sambackus?', 'sambackus!'): ']'}

class SambackusConverterTest(unittest.TestCase):
    def test_convert(self):
        text = (" sambackus.   sambackus. sambackus. \n\nsambackus! \nsambackus! "
                " sambackus!  sambackus! sambackus."
                "\n sambackus. sambackus? sambackus? sambackus.  sambackus!sambackus?  sambackus? sambackus!")
        self.assertEqual(convertSambackusToBF(text), "+,-.><[]")

if __name__ == '__main__':
    unittest.main()
