import unittest
from pathlib import Path

from modules.module_parser import Class, Method
from modules.package_parser import Package, Module
from modules.template_formatter import TemplateFormatter


class FormatterTest(unittest.TestCase):
    def setUp(self):
        self.formatter = TemplateFormatter('./')
        self.maxDiff = None

    def assert_strings_in_page(self, page, *strings):
        for string in strings:
            self.assertIn(string, page)

    def test_create_page(self):
        with self.subTest('normal'):
            method = Method('a', ['param1', 'param2'], 'Docstring1')
            cls = Class('A', ['object'], 'Docstring2', [method])
            module = Module(Path(), 'module1', [cls])
            page = self.formatter.create_docpage(Path(), module)
            self.assert_strings_in_page(page, 'a',
                                        'param1',
                                        'param2',
                                        'Docstring1',
                                        'A',
                                        'object',
                                        'Docstring2',
                                        'module1')

        with self.subTest('empty class for top-level methods'):
            cls = Class('', [''], 'Docstring2', [method])
            module = Module(Path(), 'module1', [cls])
            page = self.formatter.create_docpage(Path(), module)
            self.assert_strings_in_page(page, 'Docstring2',
                                        'a',
                                        'param1',
                                        'param2',
                                        'Docstring1',
                                        'module1')

    def test_create_index(self):
        package = Package(Path('path1'), 'package1', 'docstring1', [], [])
        module1 = Module(Path('path2'), 'module1', [])
        module2 = Module(Path('path3'), 'module2', [])
        package.modules.extend([module1, module2])
        page = self.formatter.create_index(Path(), package)
        self.assert_strings_in_page(page, 'path1',
                                    'docstring1',
                                    'path2',
                                    'module1',
                                    'path3',
                                    'module2')


if __name__ == '__main__':
    unittest.main()
