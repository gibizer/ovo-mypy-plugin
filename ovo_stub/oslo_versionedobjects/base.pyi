import typing as ty

def __getattr__(name: str) -> ty.Any: ...  # incomplete

# This skeleton is needed to indicate that o.vos needs to be type checked and
# that they don't have any field by default.
class VersionedObject: ...
