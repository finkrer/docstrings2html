#!/usr/bin/env python3
"""Docstring to HTML converter"""

import argparse
import sys
from pathlib import Path

from modules.entity_parser import Parser
from modules.template_formatter import TemplateFormatter

sys.argv = [
    '',
    '-e',
    r'C:\Users\finkrer\PycharmProjects\docstrings2html\Test Files\pocketfft.py',
    'output.html'
]


def main():
    arguments = _parse_arguments()
    with open(arguments.template, encoding='utf-8') as template:
        template = ''.join(template.readlines())
    with open(arguments.input_path, encoding='utf-8') as input_file:
        lines = input_file.readlines()
        template_formatter = TemplateFormatter(template, arguments.stylesheet, Path(arguments.input_path).name)
        parser = Parser(arguments.nonpublic, arguments.empty)
    classes = parser.get_classes(lines)
    page = template_formatter.create_page(classes)
    with open(arguments.output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(page)


def _parse_arguments():
    argparser = argparse.ArgumentParser(description='Convert a Python file into an HTML documentation page')
    argparser.add_argument('input_path', help='Path to input file')
    argparser.add_argument('output_path', help='Path to output file')
    argparser.add_argument('stylesheet', help='Optional path to custom stylesheet', nargs='?', default='./templates'
                                                                                                       '/style.css')
    argparser.add_argument('template', help='Optional path to custom template', nargs='?', default='./templates'
                                                                                                   '/template.html')
    argparser.add_argument('--nonpublic', '-n', help='Include non-public methods and classes', action='store_true')
    argparser.add_argument('--empty', '-e', help='Include methods with no docstring', action='store_true')
    return argparser.parse_args()


if __name__ == '__main__':
    main()
