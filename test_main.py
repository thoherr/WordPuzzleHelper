import unittest
from unittest.mock import patch, mock_open
from main import MeaningfulPermutations, PatternMatcher, _load_wordlist


class TestMeaningfulPermutations(unittest.TestCase):
    
    @patch('builtins.open', mock_open(read_data='helm\nlehm\nmehl\ntest\nword\nhello\n'))
    def test_permutations_basic(self):
        perms = MeaningfulPermutations('lhme')
        result = perms.result()
        expected = ['helm', 'lehm', 'mehl']
        self.assertEqual(sorted(result), sorted(expected))
    
    @patch('builtins.open', mock_open(read_data='helm\nlehm\nmehl\ntest\nword\nhello\n'))
    def test_permutations_no_matches(self):
        perms = MeaningfulPermutations('xyz')
        result = perms.result()
        self.assertEqual(result, [])
    
    @patch('builtins.open', mock_open(read_data='abc\nbca\ncab\ntest\n'))
    def test_permutations_all_match(self):
        perms = MeaningfulPermutations('abc')
        result = perms.result()
        expected = ['abc', 'bca', 'cab']
        self.assertEqual(sorted(result), sorted(expected))
    
    @patch('builtins.open', mock_open(read_data='helm\nlehm\nmehl\ntest\nword\nhello\n'))
    def test_permutations_single_char(self):
        perms = MeaningfulPermutations('h')
        result = perms.result()
        self.assertEqual(result, [])
    
    @patch('builtins.open', mock_open(read_data='test\ntset\netts\nstet\n'))
    def test_permutations_duplicate_chars(self):
        perms = MeaningfulPermutations('test')
        result = perms.result()
        expected = ['test', 'tset', 'etts', 'stet']
        self.assertTrue(all(word in expected for word in result))
    
    @patch('builtins.open', mock_open(read_data='hello\nworld\ntest\n'))
    def test_permutations_pattern_mode(self):
        perms = MeaningfulPermutations('h.llo')
        result = perms.result()
        self.assertIn('hello', result)


class TestPatternMatcher(unittest.TestCase):
    
    @patch('builtins.open', mock_open(read_data='earl\nebcl\nedel\negal\negel\nekel\nemil\nengl\nesel\nesql\nevtl\nexil\ntest\n'))
    def test_pattern_matcher_basic(self):
        matcher = PatternMatcher('e..l')
        result = matcher.result()
        expected = ['earl', 'ebcl', 'edel', 'egal', 'egel', 'ekel', 'emil', 'engl', 'esel', 'esql', 'evtl', 'exil']
        self.assertEqual(sorted(result), sorted(expected))
    
    @patch('builtins.open', mock_open(read_data='test\nword\nhello\nworld\n'))
    def test_pattern_matcher_no_matches(self):
        matcher = PatternMatcher('xyz.')
        result = matcher.result()
        self.assertEqual(result, [])
    
    @patch('builtins.open', mock_open(read_data='test\nbest\nrest\nnest\nwest\nother\n'))
    def test_pattern_matcher_multiple_dots(self):
        matcher = PatternMatcher('..st')
        result = matcher.result()
        expected = ['test', 'best', 'rest', 'nest', 'west']
        self.assertEqual(sorted(result), sorted(expected))
    
    @patch('builtins.open', mock_open(read_data='hello\nhello\nworld\n'))
    def test_pattern_matcher_exact_match(self):
        matcher = PatternMatcher('hello')
        result = matcher.result()
        self.assertEqual(result, ['hello', 'hello'])
    
    @patch('builtins.open', mock_open(read_data='test\ntest1\ntest12\n'))
    def test_pattern_matcher_length_filtering(self):
        matcher = PatternMatcher('test')
        result = matcher.result()
        self.assertEqual(result, ['test'])
    
    @patch('builtins.open', mock_open(read_data='abc\naxc\nabc\n'))
    def test_pattern_matcher_dot_wildcard(self):
        matcher = PatternMatcher('a.c')
        result = matcher.result()
        expected = ['abc', 'axc', 'abc']
        self.assertEqual(result, expected)


class TestLoadWordlist(unittest.TestCase):
    
    @patch('builtins.open', mock_open(read_data='Hallo\nWelt\nÄpfel\nÖl\nÜber\n'))
    def test_load_wordlist_normalization(self):
        wordlist = _load_wordlist(lambda x: True)
        expected = ['hallo', 'welt', 'aepfel', 'oel', 'ueber']
        self.assertEqual(wordlist, expected)
    
    @patch('builtins.open', mock_open(read_data='test\nword\nhello\nworld\n'))
    def test_load_wordlist_filtering(self):
        wordlist = _load_wordlist(lambda x: len(x) == 4)
        expected = ['test', 'word']
        self.assertEqual(wordlist, expected)
    
    @patch('builtins.open', mock_open(read_data=''))
    def test_load_wordlist_empty(self):
        wordlist = _load_wordlist(lambda x: True)
        self.assertEqual(wordlist, [])


if __name__ == '__main__':
    unittest.main()