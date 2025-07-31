import datetime
import re
from collections import Counter

import more_itertools
import sys


def _load_wordlist(wordlist_filter : lambda x : bool):
    # wordlist from https://gist.github.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4
    with open('wordlist-german.txt') as f:
        return list(filter(wordlist_filter,
                           map(lambda w: w.casefold().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue'),
                               f.read().splitlines())))


class WordList:
    def __init__(self, wordlist_filter : lambda x : bool):
        self.wordlist = _load_wordlist(wordlist_filter)
        self.wordset = set(self.wordlist)
        print(f"Loaded {len(self.wordlist)} words")


def _word_is_possible(word, char_count):
    word_count = Counter(word)
    return all(char_count[c] <= word_count[c] for c in word_count)


def _exact_char_match(word, char_count):
    return Counter(word) == char_count


class MeaningfulPermutations(WordList):

    def __init__(self, args : str):
        self._characters = args
        l = len(self._characters)
        self._is_pattern = '.' in self._characters
        char_count = Counter(self._characters)
        
        if self._is_pattern:
            # Keep permissive filtering for pattern mode
            super().__init__(lambda w : len(w) == l and _word_is_possible(w, char_count))
        else:
            # Use exact character frequency matching for non-pattern mode
            super().__init__(lambda w : len(w) == l and _exact_char_match(w, char_count))

    def result(self):
        found_words = set()
        
        if self._is_pattern:
            # Generate all permutations and use each as a regex pattern
            for sequence in self._generate_permutations():
                pattern = ''.join(sequence)
                compiled_pattern = re.compile(pattern)
                for word in self.wordlist:
                    if compiled_pattern.fullmatch(word):
                        found_words.add(word)
        else:
            # Original non-pattern logic
            for sequence in self._generate_permutations():
                candidate = ''.join(sequence)
                if candidate in self.wordset:
                    found_words.add(candidate)
        
        return list(found_words)


    def _generate_permutations(self):
        return more_itertools.distinct_permutations(self._characters)


class PatternMatcher(WordList):
    def __init__(self, args : str):
        self._pattern = args
        l = len(self._pattern)
        
        # Pre-compile regex for better performance
        self._regex = re.compile(self._pattern)
        
        # Simplified filtering: only filter by length for simple patterns
        # Complex filtering overhead outweighs benefits for most cases
        super().__init__(lambda w : len(w) == l)

    def result(self):
        words = []
        for word in self.wordlist:
            if self._regex.fullmatch(word):
                words.append(word)
        return words


def usage():
    print("Usage: python3 main.py algorithm arguments")
    print("")
    print("Algorithms:")
    print("     matcher")
    print("         Usage: python3 main.py matcher <pattern>")
    print("                <pattern> is a fixed length pattern that should match, e.g. 'e..l' which would lead to the result")
    print("                      ['earl', 'ebcl', 'edel', 'egal', 'egel', 'ekel', 'emil', 'engl', 'esel', 'esql', 'evtl', 'exil']")
    print("")
    print("     permutations")
    print("         Usage: python3 main.py permutations <characters>")
    print("                <characters> is a list of characters (without spaces) that should be in the result,")
    print("                e.g. 'lhme' which would lead to the result")
    print("                      ['helm', 'lehm', 'mehl']")
    exit(1)

if __name__ == '__main__':
    print(f"++++ started at {datetime.datetime.now()}")
    if len(sys.argv) != 3:
        usage()
    algorithm = sys.argv[1]
    if algorithm == 'matcher':
        matcher = PatternMatcher(sys.argv[2])
        print(matcher.result())
    elif algorithm == 'permutations':
        permutations = MeaningfulPermutations(sys.argv[2])
        print(permutations.result())
    else:
        print(f"Invalid algorithm: {algorithm}")
        print("Use 'matcher' or 'permutations'")
    print(f"++++ finished at {datetime.datetime.now()}")
