#!/usr/bin/env python3
"""Docstring to HTML converter"""

import argparse
import fnmatch
import sys
from pathlib import Path


def _exit(message, error_code):
    print(message, file=sys.stderr)
    sys.exit(error_code)


if sys.version_info < (3, 7):
    _exit('Use python >= 3.7', 1)

try:
    from modules.entity_parser import Parser
    from modules.template_formatter import TemplateFormatter
except Exception as e:
    _exit(f'Program modules not found: "{e}"', 1)

TEMPLATES = ['./templates/base.html',
             './templates/index.html',
             './templates/docpage.html']


def main():
    """Application entry point"""
    arguments = _parse_arguments()
    output = Path(arguments.output)
    parser = Parser(arguments.nonpublic, arguments.empty)
    try:
        template_formatter = TemplateFormatter('./')
        if not all(Path(template).is_file() for template in TEMPLATES):
            raise FileNotFoundError('Template files not found in /templates, '
                                    f'should have {", ".join(TEMPLATES)}')
    except Exception as e:
        _exit(f'Error while accessing templates:\n{e}',
              1)

    files = []
    for file in arguments.input_files:
        path = Path(file)
        if path.is_dir():
            files.extend(get_files_from_directory(path))
        else:
            files.append((path, path))

    files = [file for file in files if
             not is_ignored(file[0].name, arguments.ignore,
                            arguments.nonpublic)]

    for file in files:
        write_docpage(file[0], output.joinpath(file[1]), parser,
                      template_formatter)

    if arguments.index:
        write_index(output, files, template_formatter)


def is_ignored(file, ignore_list, show_nonpublic):
    return (is_in_ignore_list(file, ignore_list)
            or (file.startswith('_') and not show_nonpublic))


def is_in_ignore_list(path, ignore_list):
    return any(fnmatch.fnmatch(path, mask) for mask in ignore_list)


def get_files_from_directory(directory):
    """Find all Python files and their output paths in the given directory"""
    dir_path = Path(directory)
    dir_files = dir_path.rglob('*.py')
    return [(file, file.relative_to(dir_path)) for file in
            dir_files]


def write_index(output_dir, files, template_formatter):
    """Create index.html and write it to disk"""
    output_paths = [str(file[1]) + '.html' for file in files]
    output_paths.sort()
    base_path = output_dir.resolve()
    page = template_formatter.create_index(base_path, output_paths)
    index_path = output_dir.joinpath('index.html')
    try_write(index_path, page, f'Error while accessing output file '
                                f'{index_path}:\n')


def write_docpage(input_path, output_path, parser, formatter):
    """Create docpage and write it to disk"""
    path = Path(input_path)
    lines = try_read(input_path, f'Error while accessing input file'
                                 f'{input_path}:\n')
    classes = parser.get_classes(lines)
    page = formatter.create_docpage(path.name, classes)
    output_dir = Path(output_path).parent
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    file_path = f'{output_path}.html'
    try_write(file_path, page, f'Error while accessing output file'
                               f'{file_path}:\n')


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


def _parse_arguments():
    """Parse arguments"""
    argparser = argparse.ArgumentParser(
        description='Create HTML documentation pages from Python module files')
    argparser.add_argument('input_files', help='Path to input files',
                           nargs='+')
    argparser.add_argument('--output', help='Path to output directory',
                           nargs='?', default='documentation')
    argparser.add_argument('--ignore', help='Files to ignore, can use masks',
                           nargs='*', default=['*_test.py', 'test_*.py'])
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
