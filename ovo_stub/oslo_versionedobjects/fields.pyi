import typing as ty


def __getattr__(name: str) -> ty.Any: ...  # incomplete


class AutoTypedField:
    ...


class IntegerField(AutoTypedField):
    MYPY_TYPE: int


class StringField(AutoTypedField):
    MYPY_TYPE: str


class FloatField(AutoTypedField):
    MYPY_TYPE: float


class ListOfIntegersField(AutoTypedField):
    MYPY_TYPE: ty.List[int]

