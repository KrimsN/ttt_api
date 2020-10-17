from serializers.iserializer import ISerializer

class IParser():
    def __init__(self):
        raise NotImplementedError(f'{self.__class__.__name__} does not implemented')

    def parse(self):
        pass
    
    def clear_cash(self):
        pass

    def serialize(self, serialaizer: ISerializer) -> str:
        pass

    def serialize_dump(self, serialaizer: ISerializer, fout) -> str:
        pass