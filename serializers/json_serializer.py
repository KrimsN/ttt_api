from .iserializer import ISerializer

import json


class JSONSerializer(ISerializer):
    def __init__(self):
        self._current_object = {}
    
    def add_property(self, name, value):
        self._current_object[name] = value
    
    def update_properties(self, properties_dict):
        self._current_object.update(properties_dict)

    def to_str(self, *, pretty=False, encoding='utf-8'):
        if pretty:
            res = json.dumps(self._current_object, indent=2, ensure_ascii=False)
        else:
            res = json.dumps(self._current_object, ensure_ascii=False)
        
        return res.encode(encoding).decode(encoding)
    
    def dumpf(self, fout, *, pretty=True, encoding='utf-8'):
        if pretty:
            json.dump(self._current_object, fout, ensure_ascii=not pretty, indent=2)
        else:
            json.dump(self._current_object, fout, ensure_ascii=not pretty)
    
    def clear_cash(self):
        self._current_object = {}