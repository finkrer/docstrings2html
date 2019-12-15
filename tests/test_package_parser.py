import unittest
from pathlib import Path

import docstrings2html
from modules.module_parser import ModuleParser
from modules.package_parser import PackageParser, Package, Module


class TempFile:
    def __init__(self, path, contents):
        self.path = path
        self.path.write_text(contents, encoding='utf-8')

    def __enter__(self):
        return self.path

    def __exit__(self, exc_type, exc_value, traceback):
        self.path.unlink()


class PackageParserTest(unittest.TestCase):
    def setUp(self):
        module_parser = ModuleParser(False, False)
        reader = docstrings2html.try_read
        self.parser = PackageParser(reader, module_parser,
                                    ['*ignore*', 'test_*.py', '*_test.py'],
                                    False)

    def test_is_ignored(self):
        with self.subTest('normal'):
            file = Path('module.py')
            result = self.parser._is_ignored(file)
            self.assertFalse(result)

        with self.subTest('private'):
            file = Path('_module.py')
            result = self.parser._is_ignored(file)
            self.assertTrue(result)

        with self.subTest('ignored'):
            file = Path('ignored_module.py')
            result = self.parser._is_ignored(file)
            self.assertTrue(result)

    def test_get_module(self):
        with TempFile(Path('test.py'),
                      '''
                      def test():
                      """doc"""
                      ''') as file:
            result = self.parser._get_module(file, Path())
        self.assertEqual(str(result.path), 'test.py')
        self.assertEqual(result.name, 'test.py')
        self.assertEqual(result.classes[0].methods[0].name, 'test')

    def test_package_is_empty(self):
        with self.subTest('empty'):
            package = Package(Path(), '', '', [], [])
            self.assertTrue(package.is_empty())

        with self.subTest('has modules'):
            package = Package(Path(), '', '', [Module(Path(), '', [])], [])
            self.assertFalse(package.is_empty())

        with self.subTest('has empty package'):
            package = Package(Path(), '', '', [], [
                Package(Path(), '', '', [], [])
            ])
            self.assertTrue(package.is_empty())

        with self.subTest('has non-empty package'):
            package = Package(Path(), '', '', [], [
                Package(Path(), '', '', [Module(Path(), '', [])], [])
            ])
            self.assertFalse(package.is_empty())

    def test_get_package(self):
        with TempFile(Path('__init__.py'),
                      '''
                      """docstring"""
                      '''):
            with TempFile(Path('test.txt'), ''):
                with TempFile(Path('test.py'), ''):
                    result = self.parser._get_package(Path(), Path())
        self.assertEqual(result.docstring, 'docstring')
        self.assertTrue(len(result.modules) == 1
                        and result.modules[0].name == 'test.py')
