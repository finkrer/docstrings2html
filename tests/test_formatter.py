import unittest

from modules.entity_parser import Class, Method
from modules.template_formatter import TemplateFormatter


class FormatterTest(unittest.TestCase):
    def setUp(self):
        self.formatter = TemplateFormatter('../')
        self.maxDiff = None

    def test_create_page(self):
        with self.subTest('normal'):
            method = Method('a', ['param1', 'param2'], 'Docstring1')
            cls = Class('A', 'object', 'Docstring2', [method])
            page = self.formatter.create_docpage('name', [cls])
            self.assertTrue(
                'a' in page
                and 'param1' in page
                and 'param2' in page
                and 'Docstring1' in page
                and 'A' in page
                and 'object' in page
                and 'Docstring2' in page
                and 'name' in page)

        with self.subTest('empty class for top-level methods'):
            cls = Class('', '', 'Docstring2', [method])
            page = self.formatter.create_docpage('name', [cls])
            self.assertTrue(
                'Docstring2' in page
                and 'a' in page
                and 'param1' in page
                and 'param2' in page
                and 'Docstring1' in page
                and 'name' in page)

    def test_create_index(self):
        page = self.formatter.create_index('base', ['path/to/file', 'another'
                                                                    '/file'
                                                                    '.html'])
        self.assertTrue(
            'base' in page
            and 'path' in page
            and 'to' in page
            and 'file' in page
            and 'another' in page
            and 'file.html' in page
        )


if __name__ == '__main__':
    unittest.main()
