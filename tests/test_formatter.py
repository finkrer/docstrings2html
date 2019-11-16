import unittest

from modules.entity_parser import Class, Method
from modules.template_formatter import TemplateFormatter


class FormatterTest(unittest.TestCase):
    def setUp(self):
        with open('../templates/template.html', encoding='utf-8') as template:
            template = ''.join(template.readlines())
        stylesheet = '../templates/style.css'
        self.formatter = TemplateFormatter(template, stylesheet, 'test.py')
        self.maxDiff = None

    def test_create_page(self):
        with self.subTest('empty'):
            cls = Class('', '', '', [])
            page = self.formatter.create_page([cls])
            self.assertEqual(page, self.expected_page_empty)

        with self.subTest('normal'):
            method = Method('a', ['param1', 'param2'], 'Docstring')
            cls = Class('A', 'object', 'Docstring', [method])
            page = self.formatter.create_page([cls])
            self.assertEqual(page, self.expected_page_normal)

        with self.subTest('empty class for top-level methods'):
            cls = Class('', '', 'Docstring', [method])
            page = self.formatter.create_page([cls])
            self.assertEqual(page, self.expected_page_empty_class)

    expected_page_empty = """<!DOCTYPE html>
<html lang="en" class="html">
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="../templates/style.css">
    <title>test.py</title>
</head>
<body class="body">
<p class="module-name">test.py</p>
        

</body>
</html>



"""

    expected_page_normal = """<!DOCTYPE html>
<html lang="en" class="html">
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="../templates/style.css">
    <title>test.py</title>
</head>
<body class="body">
<p class="module-name">test.py</p>
        
        <div class="class">
        <p class="class-signature">
            <span class="class-name">A</span>(<span
                class="class-parameters">object</span>)
        </p>
        <pre class="class-docstring">Docstring</pre>
        
    <div class="method">
        <p class="method-signature">
            <span class="method-name">a</span>(<span
                class="method-parameters">param1, param2</span>)
        </p>
        <pre class="method-docstring">Docstring</pre>
    </div>

        </div>

</body>
</html>



"""

    expected_page_empty_class = """<!DOCTYPE html>
<html lang="en" class="html">
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="../templates/style.css">
    <title>test.py</title>
</head>
<body class="body">
<p class="module-name">test.py</p>
        
        <pre class="class-docstring">Docstring</pre>
        
    <div class="method">
        <p class="method-signature">
            <span class="method-name">a</span>(<span
                class="method-parameters">param1, param2</span>)
        </p>
        <pre class="method-docstring">Docstring</pre>
    </div>


</body>
</html>



"""


if __name__ == '__main__':
    unittest.main()
