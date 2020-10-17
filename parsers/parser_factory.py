from .iparser import IParser

from .ttt_parser import TTTParsser



from enum import Enum, auto

class ParserTypes(Enum):
    TTT = auto()

class ParserFactory():
    _parsers = {

            ParserTypes.TTT: TTTParsser
        }

    def __init__(self):
        pass

    def createParser(self, _type: ParserTypes) -> IParser:
        parser = None

        if _type in ParserTypes:
            return self._parsers[_type]()
        else:
            raise ValueError(_type)

        return parser