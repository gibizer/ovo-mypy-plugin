import typing as ty

def __getattr__(name: str) -> ty.Any: ...  # incomplete

class UnspecifiedDefault: ...

class Field:
    def __init__(
        self,
        field_type,
        nullable=False,
        default=UnspecifiedDefault,
        read_only=False,
    ) -> None: ...

class AutoTypedField(Field):
    # The constructor param list is deduced from the Field.__init__ param list,
    # and replaced **kwargs with the real signature
    # TODO(gibi): The type of the `default` param should be
    # ty.Union[UnspecifiedDefault, type(self.MYPY_TYPE)]
    def __init__(
        self,
        nullable: bool = False,
        default: ty.Any = UnspecifiedDefault,
        read_only: bool = False,
    ) -> None: ...

class IntegerField(AutoTypedField):
    MYPY_TYPE: int

class StringField(AutoTypedField):
    MYPY_TYPE: str

class FloatField(AutoTypedField):
    MYPY_TYPE: float

class ListOfIntegersField(AutoTypedField):
    MYPY_TYPE: ty.List[int]
