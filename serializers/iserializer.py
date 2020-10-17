
class ISerializer():
    def __init__(self):
        raise NotImplementedError(f'{self.__class__.__name__} does not implemented')
    
    def add_property(self, name, value) -> None:
        pass

    def update_properties(self, properties_dict) -> None :
        pass

    def to_str(self, *, pretty, encoding) -> str:
        pass

    def dumpf(self, fout, *, pretty, encoding) -> None:
        pass

    def clear_cash(self):
        pass
