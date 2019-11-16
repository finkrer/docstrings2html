#!/usr/bin/env python3
"""Docstring to HTML converter"""

import argparse
import sys
from pathlib import Path


def _exit(message, error_code):
    print(message, file=sys.stderr)
    sys.exit(error_code)


if sys.version_info < (3, 6):
    _exit('Use python >= 3.6', 1)

try:
    from modules.entity_parser import Parser
    from modules.template_formatter import TemplateFormatter
except Exception as e:
    _exit(f'Program modules not found: "{e}"', 1)


def main():
    arguments = _parse_arguments()
    try:
        with open(arguments.template, encoding='utf-8') as template:
            template = ''.join(template.readlines())
    except Exception as e:
        _exit(
            f'Error while accessing template file {arguments.template}:\n{e}',
            1)

    try:
        with open(arguments.input_path, encoding='utf-8') as input_file:
            lines = input_file.readlines()
    except Exception as e:
        _exit(f'Error while accessing input file {arguments.input_path}:\n{e}',
              1)

    parser = Parser(arguments.nonpublic, arguments.empty)
    classes = parser.get_classes(lines)

    try:
        template_formatter = TemplateFormatter(template, arguments.stylesheet,
                                               Path(arguments.input_path).name)
        page = template_formatter.create_page(classes)
    except Exception as e:
        _exit(f'Error while rendering template {arguments.template}:\n{e}', 1)

    try:
        with open(arguments.output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(page)
    except Exception as e:
        _exit(
            f'Error while accessing output file {arguments.output_path}:\n{e}',
            1)


def _parse_arguments():
    argparser = argparse.ArgumentParser(
        description='Convert a Python file into an HTML documentation page')
    argparser.add_argument('input_path', help='Path to input file')
    argparser.add_argument('output_path', help='Path to output file')
    argparser.add_argument('stylesheet',
                           help='Optional path to custom stylesheet',
                           nargs='?', default='./templates'
                                              '/style.css')
    argparser.add_argument('template', help='Optional path to custom template',
                           nargs='?', default='./templates'
                                              '/template.html')
    argparser.add_argument('--nonpublic', '-n',
                           help='Include non-public methods and classes',
                           action='store_true')
    argparser.add_argument('--empty', '-e',
                           help='Include methods with no docstring',
                           action='store_true')
    return argparser.parse_args()


if __name__ == '__main__':
    main()
