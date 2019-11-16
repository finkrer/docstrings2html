from mako.template import Template


class TemplateFormatter:
    """Formats a list of classes using provided template and stylesheet"""

    def __init__(self, template, stylesheet, name):
        self.template = Template(template)
        self.stylesheet = stylesheet
        self.name = name

    def create_page(self, classes):
        """Create an HTML page from a list of classes"""
        return self.template.render_unicode(stylesheet=self.stylesheet,
                                            classes=classes,
                                            module_name=self.name)
