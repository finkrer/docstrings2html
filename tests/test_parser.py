import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from modules.entity_parser import Parser


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = Parser(False, False)
        self.separator = 'def '

    def test_split_lines(self):
        with self.subTest('empty'):
            result = self.parser._split_lines([], self.separator)
            self.assertEqual(result, [])

        with self.subTest('normal'):
            result = self.parser._split_lines([
                'line 1',
                'def line2():',
                'line 3'
            ], self.separator)
            self.assertEqual(result, [['line 1'], ['def line2():', 'line 3']])

        with self.subTest('separator at the start'):
            result = self.parser._split_lines([
                'def line1():',
                'line 2'
            ], self.separator)
            self.assertEqual(result, [['def line1():', 'line 2']])

    def test_get_group_title(self):
        with self.subTest('empty'):
            result = self.parser._get_group_title([], self.separator)
            self.assertEqual(result, '')

        with self.subTest('normal'):
            result = self.parser._get_group_title(['def line1():', 'line 2'], self.separator)
            self.assertEqual(result, 'line1()')

        with self.subTest('no title'):
            result = self.parser._get_group_title(['line1', 'line 2'], self.separator)
            self.assertEqual(result, '')

    def test_split_title(self):
        with self.subTest('empty'):
            result = self.parser._split_title('')
            self.assertEqual(result, ('', ''))

        with self.subTest('normal'):
            result = self.parser._split_title('name(param1, param2)')
            self.assertEqual(result, ('name', 'param1, param2'))

        with self.subTest('no parameters'):
            result = self.parser._split_title('name()')
            self.assertEqual(result, ('name', ''))

        with self.subTest('name only'):
            result = self.parser._split_title('name')
            self.assertEqual(result, ('name', ''))

    def test_split_parameters(self):
        with self.subTest('empty'):
            result = self.parser._split_parameters('')
            self.assertEqual(result, [])

        with self.subTest('normal'):
            result = self.parser._split_parameters('param1, param2')
            self.assertEqual(result, ['param1', 'param2'])

    def test_get_docstring(self):
        with self.subTest('empty'):
            result = self.parser._get_docstring([])
            self.assertEqual(result, '')

        with self.subTest('on one line'):
            result = self.parser._get_docstring(['  """line1"""'])
            self.assertEqual(result, 'line1')

        with self.subTest('multiline'):
            result = self.parser._get_docstring(['"""line1\n', 'line2\n', '"""\n'])
            self.assertEqual(result, 'line1\nline2')

        with self.subTest('two docstrings'):
            result = self.parser._get_docstring(['"""line1"""\n', '"""line2"""\n'])
            self.assertEqual(result, 'line1')

    def test_get_methods(self):
        with self.subTest('empty'):
            result = self.parser.get_methods([])
            self.assertEqual(result, [])

        with self.subTest('normal'):
            result = self.parser.get_methods(['line1', 'def line2(param1, param2): ', '"""line3"""', 'line4'])
            self.assertEqual(result[0].name, 'line2')
            self.assertEqual(result[0].parameters, ['param1', 'param2'])
            self.assertEqual(result[0].docstring, 'line3')

        with self.subTest('no docstring'):
            parser_e = Parser(False, True)
            lines = ['line1', 'def line2(param1, param2): ', 'line3']
            result = self.parser.get_methods(lines)
            result_e = parser_e.get_methods(lines)
            self.assertEqual(result, [])
            self.assertEqual(result_e[0].name, 'line2')
            self.assertEqual(result_e[0].parameters, ['param1', 'param2'])
            self.assertEqual(result_e[0].docstring, '')

        with self.subTest('non-public'):
            parser_n = Parser(True, False)
            lines = ['line1', 'def _line2(param1, param2): ', '"""line3"""', 'line4']
            result = self.parser.get_methods(lines)
            result_n = parser_n.get_methods(lines)
            self.assertEqual(result, [])
            self.assertEqual(result_n[0].name, '_line2')
            self.assertEqual(result_n[0].parameters, ['param1', 'param2'])
            self.assertEqual(result_n[0].docstring, 'line3')

    def test_get_classes(self):
        with self.subTest('empty'):
            result = self.parser.get_classes([])
            self.assertEqual(result, [])

        with self.subTest('normal'):
            result = self.parser.get_classes(['class A(object): \n', '"""line"""\n', 'def b(): \n', '"""line"""\n'])
            self.assertEqual(result[0].name, 'A')
            self.assertEqual(result[0].parameters, 'object')
            self.assertEqual(result[0].docstring, 'line')
            self.assertEqual(result[0].methods[0].name, 'b')

        with self.subTest('non-public'):
            parser_n = Parser(True, False)
            lines = ['class _A(object): \n', '"""line"""\n', 'def b(): \n', '"""line"""\n']
            result = self.parser.get_classes(lines)
            result_n = parser_n.get_classes(lines)
            self.assertEqual(result, [])
            self.assertEqual(result_n[0].name, '_A')
            self.assertEqual(result_n[0].parameters, 'object')
            self.assertEqual(result_n[0].docstring, 'line')

        with self.subTest('empty class for top-level methods'):
            result = self.parser.get_classes(['def b(): \n', '"""line"""\n'])
            self.assertEqual(result[0].name, '')
            self.assertEqual(result[0].parameters, '')
            self.assertEqual(result[0].methods[0].name, 'b')


if __name__ == '__main__':
    unittest.main()
