from typing import Any
import os.path, pickle

class _Old:
    def __init__(self, filename: str) -> None:
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                tmp = pickle.load(f)
            self.__dict__.update(tmp)

class PersistentVals:
    def __init__(self, filename: str) -> None:
        object.__setattr__(self, "_PersistentVals__filename", filename)
        object.__setattr__(self, "_old", _Old(filename))

    def print(self) -> None:
        for i,v in self.__dict__.items():
            if i != '_PersistentVals__filename':
                print(i, '=', v)
    
    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.__dict__.keys():
            object.__setattr__(self, name, value)
        else:
            if name in self._old.__dict__.keys():
                if type(value) is type(self._old.__dict__[name]):
                    object.__setattr__(self, name, self._old.__dict__[name])
                else:
                    object.__setattr__(self, name, value)
            else:
                object.__setattr__(self, name, value)

    def __del__(self) -> None:
        if hasattr(self, '_old'):
            del self._old
        with open(self.__filename, "wb") as f:
            del self.__filename
            pickle.dump(self.__dict__,f)

class NotPersistentVals:
    def __init__(self, filename: str) -> None:
        pass

    def print(self):
        for i,v in self.__dict__.items():
            print(i,'=',v)