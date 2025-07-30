import sys
import typing

from ._template import Conversion, Interpolation, Template

__all__ = ["bind", "binder", "f", "evaluate", "convert", "converter", "normalize", "normalize_str"]


def converter[T](conversion: Conversion) -> typing.Callable[[T], T | str]:
    """
    Convert a value to a string using the specified conversion.
    """
    if conversion == "a":
        return repr
    elif conversion == "r":
        return repr
    elif conversion == "s":
        return str
    else:
        raise ValueError(f"Invalid conversion: {conversion}")


def convert[T](
    value: T,
    conversion: Conversion | None,
) -> T | str:
    """
    Convert a value to a string using the specified conversion.
    """
    return converter(conversion)(value) if conversion else value


def normalize_str(interpolation: Interpolation) -> str:
    converted = convert(interpolation.value, interpolation.conversion)
    return format(converted, interpolation.format_spec)


def normalize(interpolation: Interpolation) -> str | object:
    """
    Normalize an Interpolation object to a string.
    """
    if interpolation.conversion is None:
        return interpolation.value
    else:
        return normalize_str(interpolation)


if sys.version_info >= (3, 14):
    def interpolated(value: Interpolation | str) -> typing.TypeIs[Interpolation]:
        return isinstance(value, Interpolation)
else:
    def interpolated(value: Interpolation | str) -> typing.TypeIs[Interpolation]:
        return not isinstance(value, str)


@typing.overload
def bind(
    template: Template,
    binder: typing.Callable[[Interpolation], str],
    *,
    joiner: typing.Callable[[typing.Iterable[str]], str] = ...,
) -> str: ...
@typing.overload
def bind[U](
    template: Template,
    binder: typing.Callable[[Interpolation], str],
    *,
    joiner: typing.Callable[[typing.Iterable[str]], U],
) -> U: ...
@typing.overload
def bind[T, U](
    template: Template,
    binder: typing.Callable[[Interpolation], T],
    *,
    joiner: typing.Callable[[typing.Iterable[T | str]], U],
) -> U: ...
def bind(template: Template, binder, *, joiner="".join) -> typing.Any:
    return joiner(_bind_iterable(template, binder))


@typing.overload
def binder(
    binder: typing.Callable[[Interpolation], str],
    joiner: typing.Callable[[typing.Iterable[str]], str] = ...,
) -> str: ...
@typing.overload
def binder[U](
    binder: typing.Callable[[Interpolation], str],
    joiner: typing.Callable[[typing.Iterable[str]], U],
) -> U: ...
@typing.overload
def binder[T, U](
    binder: typing.Callable[[Interpolation], T],
    joiner: typing.Callable[[typing.Iterable[T | str]], U],
) -> U: ...
def binder(binder, joiner="".join) -> typing.Any:
    return lambda template: bind(template, binder, joiner=joiner)


def f(template: Template | str) -> str:
    return template if isinstance(template, str) else bind(template, normalize_str)


evaluate = f


def _bind_iterable(template: Template, binder) -> typing.Iterator[Interpolation | str]:
    for item in template:
        if interpolated(item):
            yield binder(item)
        else:
            yield item
