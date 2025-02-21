import re
import sys
from dataclasses import dataclass
from typing import List


class ModuleParser:
    """Parser for classes, methods and their docstrings"""

    def __init__(self, show_nonpublic, show_empty):
        self.show_nonpublic = show_nonpublic
        self.show_empty = show_empty

    def _split_lines(self, lines, separator_marker):
        """Split lines into groups by lines containing the separator string"""
        result = []
        current_group = []
        for line in lines:
            if re.match(rf'[^\S\n]*{separator_marker}\w+(\(.*\))?:', line):
                if current_group:
                    result.append(current_group)
                current_group = []
            current_group.append(line)
        if current_group:
            result.append(current_group)
        return result

    def _get_group_title(self, group_lines, title_marker):
        """Return the title of a group"""
        if not group_lines:
            return ''
        title_line = group_lines[0].rstrip()
        index = group_lines[0].find(title_marker)
        if index == -1:
            return ''
        return title_line[index + len(title_marker):-1]

    def _split_title(self, title):
        """Split title into name and parameters"""
        if not title:
            return '', ''
        if re.search(r'\(.*\)', title):
            return re.match(r'(\w+)\((.*)\)', title).groups()
        else:
            return title, ''

    def _split_parameters(self, parameters):
        """Split parameter string into parameters"""
        if not parameters:
            return []
        return [parameter.strip() for parameter in parameters.split(', ')]

    def get_methods(self, lines):
        """Extract method objects from lines"""
        result = []
        methods = self._split_lines(lines, Method.TITLE_MARKER)
        for m in methods:
            signature = self._get_group_title(m, Method.TITLE_MARKER)
            name, parameters = self._split_title(signature)
            parameters = self._split_parameters(parameters)
            docstring = self.get_docstring(m)
            method = Method(name, parameters, docstring)
            if (method.name
                    and (method.is_public() or self.show_nonpublic)
                    and (method.docstring or self.show_empty)):
                result.append(method)
        return result

    def get_classes(self, lines):
        """Extract class objects from lines"""
        result = []
        classes = self._split_lines(lines, Class.TITLE_MARKER)
        for c in classes:
            signature = self._get_group_title(c, Class.TITLE_MARKER)
            name, parent = self._split_title(signature)
            docstring = self.get_docstring(c)
            methods = self.get_methods(c)
            class_ = Class(name, parent, docstring, methods)
            if class_.is_public() or self.show_nonpublic:
                result.append(class_)
        return result

    def get_docstring(self, entity_lines):
        """Get entity's docstring from lines containing its text"""
        entity = ''.join(entity_lines)
        result = re.search(r'(?sm)\"\"\"(.*?)\"\"\"', entity)
        if result is None:
            return ''
        return self._trim(result.groups()[0])

    def _trim(self, docstring):
        """Trim docstring

        Taken from PEP-257
        """
        if not docstring:
            return ''
        # Convert tabs to spaces (following the normal Python rules)
        # and split into a list of lines:
        lines = docstring.expandtabs().splitlines()
        # Determine minimum indentation (first line doesn't count):
        indent = sys.maxsize
        for line in lines[1:]:
            stripped = line.lstrip()
            if stripped:
                indent = min(indent, len(line) - len(stripped))
        # Remove indentation (first line is special):
        trimmed = [lines[0].strip()]
        if indent < sys.maxsize:
            for line in lines[1:]:
                trimmed.append(line[indent:].rstrip())
        # Strip off trailing and leading blank lines:
        while trimmed and not trimmed[-1]:
            trimmed.pop()
        while trimmed and not trimmed[0]:
            trimmed.pop(0)
        # Return a single string:
        return '\n'.join(trimmed)


@dataclass
class Entity:
    """Base class for classes and methods"""
    name: str
    parameters: list
    docstring: str

    def is_public(self):
        """Check if entity is public"""
        return not self.name.startswith('_')


@dataclass
class Method(Entity):
    """Representation of a method"""
    TITLE_MARKER = 'def '


@dataclass
class Class(Entity):
    """Representation of a class"""
    TITLE_MARKER = 'class '
    methods: List[Method]
