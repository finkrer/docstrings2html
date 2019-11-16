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
    """Application entry point"""
    arguments = _parse_arguments()
    output = Path(arguments.output)
    parser = Parser(arguments.nonpublic, arguments.empty)
    try:
        template_formatter = TemplateFormatter('./')
    except Exception as e:
        _exit(f'Error while rendering template {arguments.template}:\n{e}',
              1)

    if arguments.directory:
        files = []
        for directory in arguments.input_files:
            dir_path = Path(directory)
            dir_files = dir_path.rglob('*.py')
            dir_files = [(file, file.relative_to(dir_path)) for file in
                         dir_files]
            files.extend(dir_files)
    else:
        files = [(file, file) for file in arguments.input_files]

    for file in files:
        write_docpage(file[0], output.joinpath(file[1]), parser,
                      template_formatter)

    if arguments.index:
        output_paths = [str(file[1]) + '.html' for file in files]
        output_paths.sort()
        base_path = output.resolve()
        page = template_formatter.create_index(base_path, output_paths)
        index_path = output.joinpath('index.html')
        try_write(index_path, page, f'Error while accessing output file '
                                    f'{index_path}:\n')


def try_read(filename, message, error_code=1):
    """Try to read file and exit with message on failure"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            result = file.readlines()
    except Exception as e:
        _exit(message + str(e), error_code)
    return result


def try_write(filename, data, message, error_code=1):
    """Try to write file and exit with message on failure"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(data)
    except Exception as e:
        _exit(message + str(e), error_code)


def write_docpage(input_path, output_path, parser, formatter):
    """Create docpage and write it to disk"""
    path = Path(input_path)
    lines = try_read(input_path, f'Error while accessing input file '
                                 f'{input_path}:\n')
    classes = parser.get_classes(lines)
    page = formatter.create_docpage(path.name, classes)
    output_dir = Path(output_path).parent
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    file_path = f'{output_path}.html'
    try_write(file_path, page, f'Error while accessing output file '
                               f'{file_path}:\n')


def _parse_arguments():
    """Parse arguments"""
    argparser = argparse.ArgumentParser(
        description='Convert a Python file into an HTML documentation page')
    argparser.add_argument('input_files', help='Path to input files',
                           nargs='+')
    argparser.add_argument('--output', help='Path to output directory',
                           nargs='?', default='./')
    argparser.add_argument('--directory', '-d',
                           help='Treat input files as directories',
                           action='store_true')
    argparser.add_argument('--index', '-i',
                           help='Create an index.html file with links to all '
                                'output files',
                           action='store_true')
    argparser.add_argument('--nonpublic', '-n',
                           help='Include non-public methods and classes',
                           action='store_true')
    argparser.add_argument('--empty', '-e',
                           help='Include methods with no docstring',
                           action='store_true')
    return argparser.parse_args()


if __name__ == '__main__':
    main()
