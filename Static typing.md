# Static typing

Python fundamentally uses a dynamically typed execution. And the typing support that the language
has does not change that.

All it offers is support at the language level to specify types as sort of additional metadata to stuff
and then leaves the static analysis or any sort of checking to third party implementations like mypy, pyright etc.

## Common examples

In no fixed order, the usual stuff that covers most of the cases.

- `Any` if you want to disable any checks for something
- ordinary built in types have the same name like `float`, `int`, `list`, `list[int]`, `tuple[float,int]`, `dict[str,int]`
- `Literal["fast","slow"]` is for literal args, a form of weaker static analysis based check to ensure args can only be
  these two. - difference over enums is that the runtime type is still `str` as opposed to an entirely new thing in `Enum`
- `type Coords = tuple[int, int]` is an example of a typealias
  - an older syntax used `Coords: typing.TypeAlias = typle[int,int]`
- types can be union like `x: int | str = 5`
- `Protocol` allows for static duck typing as an alternative to interfaces

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None:
        # this ... is valid python, it's Ellipsis, here used in place of a pass for convention as
        # this is to be implemented
        ...

class Circle:
    def draw(self) -> None:
        print("circle")

# then in say a function you can restrict allow static checking to just check if a draw(self) -> None exists
# on the passed arg
def render(obj: Drawable):
    pass
```

By why do this instead of inheritance, for example this is another way to do all this

```python
from abc import ABC, abstractmethod

class Drawable(ABC):
    @abstractmethod
    def draw(self) -> None:
        pass

class Circle(Drawable):
    def draw(self) -> None:
        print("circle")

def render(obj: Drawabe):
    pass
```

    - the difference is that one is just structural checking and is intended for more loose coupling
    - what inheritance allows is that the type is actually `Drawable` as in `isinstance(Circle(), Drawable)` is `True`
    - for just this case, there's little difference, note that inhertiance would've also allowed you to pick other
    properties and behaviors from the func, that protocol doesn't, which is the idea of "loose" coupling aka I just want
    it to satisfy this instead of inheriting all the rest too. Seems more like a trait.

- `Dict` if you ever see is from older python and is not needed / preferred. `dict[str, float]` is the modern version.
- `TypedDict`, in case you want behavior like "key a is of type x", "key b is of type y" for the static checker

```python
from typing import TypedDict

class User(TypedDict):
    name: str
    age: int

user: User = {
    "name": "Alice",
    "age": 30,
}
```

    - you would use this if you use a dict and get some item from it and want the static checker to be able to infer it.
    - in general for actual app data, prefer dataclasses; a TypedDict is more so when the semantics really are more dict
    like and you just want typing for "some" keys ( can be all )

- `Callable` to describe functions

```python
from collections.abc import Callable

def apply(
    # takes an int and returns a str
    # named args don't work nicely here, so if that level of checks needed, use a Protocol
    f: Callable[[int], str],
    x: int,
) -> str:
    return f(x)
```

- `Final` to signal that something should not be re-assigned, usually for constants ( due to lack of a const in python )
  - `MAX_USERS: typing.Final = 100`
- `Self` for type of the current class / subclass it's in. You would see this a lot in fluent apis.
- `TypeIs` is rather more advanced and niche usecase. Think of it like tagging to a bool and then narrowing type and
  letting the checker use that narrowed type for a scope

```python
from typing import TypeIs

x: str | int = "hello"

def is_string(value: object) -> TypeIs[str]:
    return isinstance(value, str)

if is_string(x):
    # x is str
    ...
else:
    # x is int
    ...
```

## Misc

- a class that produces objects of type T has type `type[T]`
- if you forget to overrode and abstract method, it's a TypeError on instantiation of the class
