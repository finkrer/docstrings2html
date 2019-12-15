from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from modules.module_parser import Class


class PackageParser:
    """Parses directories into packages and modules"""

    def __init__(self, file_reader, module_parser, ignore_list,
                 show_nonpublic):
        self.read_file = file_reader
        self.module_parser = module_parser
        self.ignore_list = ignore_list
        self.show_nonpublic = show_nonpublic

    def get_packages(self, directory):
        """Return a package containing all packages in the given directory"""
        root = Path(directory)
        return self._get_package(root, root)

    def get_loose_files(self, files, base_package):
        """Return packages and loose modules at given paths using the given
        package as the container"""
        root = Path()
        for file in files:
            path = Path(file)
            if path.is_file():
                base_package.modules.append(self._get_module(path, root))
            elif path.is_dir():
                package = self._get_package(path, path)
                base_package.packages.append(package)
        return base_package

    def _get_package(self, dir_, root):
        """Implementation of get_packages()"""
        modules = []
        packages = []
        for file in dir_.iterdir():
            if file.is_dir():
                package = self._get_package(file, root)
                packages.append(package)
            elif file.suffix == '.py' and not self._is_ignored(file):
                modules.append(self._get_module(file, root))
        docstring = ''
        if (dir_ / '__init__.py').is_file():
            init = self.read_file(dir_ / '__init__''.py')
            docstring = self.module_parser.get_docstring(init)
        package = Package(dir_.relative_to(root.parent), dir_.name, docstring,
                          modules, packages)
        return package

    def _get_module(self, path, root):
        """Return module object for the given path"""
        contents = self.read_file(path)
        return Module(path.relative_to(root.parent), path.name,
                      self.module_parser.get_classes(contents))

    def _is_ignored(self, file):
        """Check if the file should be ignored"""
        return (any(file.match(pattern) for pattern in self.ignore_list)
                or (file.name.startswith('_') and not self.show_nonpublic))


@dataclass
class Module:
    """Representation of a Python module"""
    path: Path
    name: str
    classes: List[Class]


@dataclass
class Package:
    """Representation of a Python package"""
    path: Path
    name: str
    docstring: str
    modules: List[Module]
    packages: List[Package]

    _empty = None

    def __iter__(self):
        yield self
        for package in self.packages:
            yield from package

    def is_empty(self):
        """Check if the package or its nested packages contain any modules"""
        if self._empty is None:
            self._empty = True
            if self.modules or any(not package.is_empty()
                                   for package in self.packages):
                self._empty = False
        return self._empty
