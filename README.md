# WordPuzzleHelper

I wrote this litte script to help me solving crossword puzzles by looking up a list of most of the german
words and matching them in differnt ways with the given constraint.

The currently implemented lookup algorithms are

## permutations

The first variant looks for permutations of a given sequence of characters in the (german) wordlist.

Therefore you have to provide a list of characters, provided as a single string argument.

The script computes all possible permutations of the list of character, compares them with the (normalized)
wordlist and collects all matches, e.g.

```shell
bash % python3 main.py permutations lhme
Loaded 2531 words
['helm', 'lehm', 'mehl']
```

## matches

The script matches the given pattern to the wordlist.

The length of the pattern is used to filter the wordlist for efficiency, therefore only simple
patterns will work (i.e. only `.` or character classes as placeholder).

The pattern has to be provided as a single argument, e.g.

```shell
bash % python3 main.py matcher e..l
Loaded 2531 words
['earl', 'ebcl', 'edel', 'egal', 'egel', 'ekel', 'emil', 'engl', 'esel', 'esql', 'evtl', 'exil']
```
