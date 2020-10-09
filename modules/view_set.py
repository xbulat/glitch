import os

from collections import OrderedDict
from string import Template


class ViewSet:
    def __init__(self, **kwargs):
        self.template_file = kwargs.get('template_file')
        self.data = kwargs.get('data')
        self.output_file = kwargs.get('output_file', None)
        self.flat_data = OrderedDict()

    @property
    def template(self):
        with open(
                os.path.dirname(os.path.abspath(__file__ + "/../")) + '/templates/' + self.template_file, 'r') as template:
            return Template(template.read())

    def render(self):
        return self.template.substitute(**self.flatten())

    def flatten(self):
        def recurse(element, parent_key='', sep='_'):
            if isinstance(element, list):
                for i in range(len(element)):
                    recurse(element[i], parent_key + sep + str(i) if parent_key else str(i))
            elif isinstance(element, dict):
                for k, v in element.items():
                    recurse(v, parent_key + sep + k if parent_key else k)
            else:
                self.flat_data[parent_key] = element

        recurse(self.data)

        return self.flat_data

    def write(self):
        with open(self.output_file, 'w') as output_file:
            output_file.write(self.render())
