from .iserializer import ISerializer

from lxml.etree import Element
from lxml import etree as ET

class XMLSerializer(ISerializer):
    def __init__(self):
        self._current_element = Element('elem')

    def _add_subproperty(self, elem, name, value):
        name = str(name)
        if name[0].isdigit():
            name = f'n{name}'
        item = Element(name)
        if isinstance(value, dict):
            for key in value:
                self._add_subproperty(item, key, value[key])
        else:
            item.text = str(value)
        elem.append(item)
        

    def add_property(self, name, value):
        name = str(name)
        if name[0].isdigit():
            name = f'n{name}'
        prop = Element(name)
        if isinstance(value, dict):
            for key in value:
                self._add_subproperty(prop, key, value[key])
        else:        
            prop.text = str(value)

        self._current_element.append(prop)

    def update_properties(self, properties_dict):
        for key in properties_dict:
            self.add_property(key, properties_dict[key])
    
    def to_str(self, *, pretty=False, encoding='unicode'):
        return ET.tostring(self._current_element, pretty_print=pretty, encoding=encoding)


    def dumpf(self, fout, *, pretty=True, encoding='unicode'):
        fout.write(self.to_str(pretty=pretty, encoding=encoding))

    def clear_cash(self):
        self._current_element = {}