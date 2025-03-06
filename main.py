import datetime
import more_itertools
import sys


class WordList:
    def __init__(self, wordlist_filter : lambda x : bool):
        self.wordlist = self._load_wordlist(wordlist_filter)
        print(f"Loaded {len(self.wordlist)} words")

    def _load_wordlist(self, wordlist_filter : lambda x : bool):
        # wordlist from https://gist.github.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4
        with open('wordlist-german.txt') as f:
            return list(map(lambda w: w.casefold(),
                filter(wordlist_filter, f.read().splitlines())))


class WhatMakesSense(WordList):

    def __init__(self, characters : list):
        self.characters = characters
        l = len(characters)
        super().__init__(lambda w : len(w) == l)

    def meaningful_words(self):
        for sequence in self._generate_permutations():
            word = ''.join(sequence)
            if word in self.wordlist:
                print(word)

    def _generate_permutations(self):
        return more_itertools.distinct_permutations(self.characters)


if __name__ == '__main__':
    whatMakesSense = WhatMakesSense(sys.argv[1:])
    print(f"++++ started at {datetime.datetime.now()}")
    whatMakesSense.meaningful_words()
    print(f"++++ finished at {datetime.datetime.now()}")
