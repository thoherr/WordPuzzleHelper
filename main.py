import datetime
import more_itertools
import sys


class WhatMakesSense:
    def __init__(self, characters):
        self.characters = list(map(lambda c : c[0], characters))
        self.wordlist = self._load_wordlist()

    def meaningful_words(self):
        for sequence in self._generate_permutations():
            word = ''.join(sequence)
            if word in self.wordlist:
                print(word)

    def _generate_permutations(self):
        return more_itertools.distinct_permutations(self.characters)

    def _load_wordlist(self):
        l = len(self.characters)
        # wordlist from https://gist.github.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4
        with open('wordlist-german.txt') as f:
            return list(map(lambda w: w.casefold(),
                filter(lambda w : len(w) == l,  f.read().splitlines())))

if __name__ == '__main__':
    whatMakesSense = WhatMakesSense(sys.argv[1:])
    print(f"++++ started at {datetime.datetime.now()}")
    whatMakesSense.meaningful_words()
    print(f"++++ finished at {datetime.datetime.now()}")
