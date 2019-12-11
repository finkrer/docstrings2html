from mako.lookup import TemplateLookup


class TemplateFormatter:
    """Finds and renders template files"""

    def __init__(self, template_directory):
        self.lookup = TemplateLookup(directories=[template_directory],
                                     strict_undefined=True)

    def create_docpage(self, base_path, module):
        """Create an HTML documentation page from a module object"""
        template = self.lookup.get_template('/templates/docpage.html')
        return template.render_unicode(base_path=base_path, module=module)

    def create_index(self, base_path, packages):
        """Create an index page with links to provided packages and modules"""
        template = self.lookup.get_template('/templates/index.html')
        return template.render_unicode(base_path=base_path, packages=packages)
