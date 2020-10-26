from typing import List, Any

def __getattr__(name: str) -> Any: ...  # incomplete

class AutoTypedField:
    ...

class IntegerField(AutoTypedField):
    MYPY_TYPE: int

class StringField(AutoTypedField):
    MYPY_TYPE: str

class FloatField(AutoTypedField):
    MYPY_TYPE: float

class ListOfIntegersField(AutoTypedField):
    MYPY_TYPE: List[int]

