import datetime
import re

import more_itertools
import sys


def _load_wordlist(wordlist_filter : lambda x : bool):
    # wordlist from https://gist.github.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4
    with open('wordlist-german.txt') as f:
        return list(map(lambda w: w.casefold(),
            filter(wordlist_filter, f.read().splitlines())))


class WordList:
    def __init__(self, wordlist_filter : lambda x : bool):
        self.wordlist = _load_wordlist(wordlist_filter)
        print(f"Loaded {len(self.wordlist)} words")


class MeaningfulPermutations(WordList):

    def __init__(self, args : list):
        self._characters = args
        l = len(self._characters)
        super().__init__(lambda w : len(w) == l)

    def result(self):
        words = []
        for sequence in self._generate_permutations():
            word = ''.join(sequence)
            if word in self.wordlist:
                words.append(word)
        return words

    def _generate_permutations(self):
        return more_itertools.distinct_permutations(self._characters)


class PatternMatcher(WordList):
    def __init__(self, args : list):
        self._pattern = args[0]
        l = len(self._pattern)
        super().__init__(lambda w : len(w) == l)

    def result(self):
        words = []
        for word in self.wordlist:
            if re.fullmatch(self._pattern, word):
                words.append(word)
        return words


if __name__ == '__main__':
    print(f"++++ started at {datetime.datetime.now()}")
    algorithm = sys.argv[1]
    if algorithm == 'matcher':
        matcher = PatternMatcher(sys.argv[2:])
        print(matcher.result())
    elif algorithm == 'permutations':
        permutations = MeaningfulPermutations(sys.argv[2:])
        print(permutations.result())
    else:
        print(f"Invalid algorithm: {algorithm}")
        print("Use 'matcher' or 'permutations'")
    print(f"++++ finished at {datetime.datetime.now()}")
