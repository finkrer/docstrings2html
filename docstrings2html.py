#!/usr/bin/env python3
"""Docstring to HTML converter"""

import argparse
import sys
from pathlib import Path


def _exit(message, error_code):
    print(message, file=sys.stderr)
    sys.exit(error_code)


if sys.version_info < (3, 7):
    _exit('Use python >= 3.7', 1)

try:
    from modules.module_parser import ModuleParser, Class
    from modules.template_formatter import TemplateFormatter
    from modules.package_parser import PackageParser, Package
except Exception as e:
    _exit(f'Program modules not found: "{e}"', 1)

TEMPLATES = ['./templates/base.html',
             './templates/index.html',
             './templates/docpage.html',
             './templates/module_index.html',
             './templates/navbar.html']


def main():
    """Application entry point"""
    arguments = _parse_arguments()
    output = Path(arguments.output)
    parser = ModuleParser(arguments.nonpublic, arguments.empty)
    template_formatter = try_get_template_formatter()
    package_parser = PackageParser(try_read, parser, arguments.ignore,
                                   arguments.nonpublic)

    if (len(arguments.input_files) == 1
            and Path(arguments.input_files[0]).is_dir()):
        packages = package_parser.get_packages(arguments.input_files[0])
    else:
        packages = Package(Path('./'), '', '', [], [])
        package_parser.get_loose_files(arguments.input_files, packages)

    output.mkdir(parents=True, exist_ok=True)
    for package in packages:
        for module in package.modules:
            write_docpage(output, module, template_formatter)
        if arguments.index and not package.is_empty():
            write_index(output, package, template_formatter)


def write_index(base_output_dir, package, formatter):
    """Create index.html and write it to disk"""
    base_path = base_output_dir.resolve()
    page = formatter.create_index(base_path, package)
    filename = 'index.html'
    output_dir = base_output_dir.joinpath(package.path)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir.joinpath(filename)
    try_write(output_path, page)


def write_docpage(base_output_dir, module, formatter):
    """Create docpage and write it to disk"""
    base_path = base_output_dir.resolve()
    page = formatter.create_docpage(base_path, module)
    output_dir = base_output_dir.joinpath(module.path.parent)
    output_path = base_output_dir.joinpath(module.path) \
        .with_suffix(module.path.suffix + '.html')
    output_dir.mkdir(parents=True, exist_ok=True)
    try_write(output_path, page)


def try_get_template_formatter():
    try:
        template_formatter = TemplateFormatter('./')
        if not all(Path(template).is_file() for template in TEMPLATES):
            raise FileNotFoundError('Template files not found in /templates, '
                                    f'should have {", ".join(TEMPLATES)}')
    except Exception as e:
        _exit(f'Error while accessing templates:\n{e}',
              1)
    return template_formatter


def try_read(filename, error_code=1):
    """Try to read file and exit with message on failure"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            result = file.readlines()
    except Exception as e:
        message = f'Error while accessing input file {filename}:\n'
        _exit(message + str(e), error_code)
    return result


def try_write(filename, data, error_code=1):
    """Try to write file and exit with message on failure"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(data)
    except Exception as e:
        message = f'Error while accessing output file {filename}:\n'
        _exit(message + str(e), error_code)


def _parse_arguments():
    """Parse arguments"""
    argparser = argparse.ArgumentParser(
        description='Create HTML documentation pages from Python module files')
    argparser.add_argument('input_files', help='Path to input files or '
                                               'directories', nargs='+')
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
