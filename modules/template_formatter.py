from mako.lookup import TemplateLookup


class TemplateFormatter:
    """Formats a list of classes using provided template and stylesheet"""

    def __init__(self, template_directory):
        self.lookup = TemplateLookup(directories=[template_directory])

    def create_docpage(self, name, classes):
        """Create an HTML page from a list of classes"""
        template = self.lookup.get_template('/templates/docpage.html')
        return template.render_unicode(classes=classes, module_name=name)

    def create_index(self, base_path, files):
        """Create an index page with links to provided files"""
        template = self.lookup.get_template('/templates/index.html')
        return template.render_unicode(base_path=base_path, files=files)
