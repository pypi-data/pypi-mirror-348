import sys
import os

from staq.helper import splitWithEscapes

def test_split():

   tp1 = 'hello {world: "hello world"}'
   tp2 = 'cmd: call printf(\"Hello: %d %d\", 1, 2)'

   split1 = splitWithEscapes(tp1, ":")
   split2 = splitWithEscapes(tp2, ":")

   assert split1 == [tp1]
   assert split2 == ['cmd', 'call printf(\"Hello: %d %d\", 1, 2)']

if __name__ == "__main__":
    test_split()