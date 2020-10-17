from .iserializer import ISerializer
from .json_serializer import JSONSerializer
from .xml_serializer import XMLSerializer


from enum import Enum

class SerializerTypes(Enum):
    JSON = 'json'
    XML = 'xml'


class SerializerFactory:

    _serializers = {
        SerializerTypes.JSON: JSONSerializer,
        SerializerTypes.XML: XMLSerializer
    }

    def create(self, _type):

        if _type in SerializerTypes:
            return self._serializers[_type]()
        else:
            raise ValueError(_type)

