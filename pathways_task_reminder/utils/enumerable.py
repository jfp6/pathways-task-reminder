from typing import Callable, Iterable


def partition_while(
    predicate: Callable[[any], bool],
    iterable: Iterable[any],
    behavior: str = "left",
) -> tuple[list[any], list[any]]:
    """Partitions into two lists while predicate is true.

    Args:
        predicate: A Callable that returns something evaluating to True or not.
        iterable: The thing to iterate over.
        behavior
            left: On failure to match, include with the left group (trues)
            right: On failure to match, include with the right group (falses)
            remove: Don't include the matching item at all.
    """
    _allowed_behaviors = ["left", "right", "remove"]
    if behavior not in _allowed_behaviors:
        raise ValueError(f"behavior must be one of {_allowed_behaviors}")
    iterator = iter(iterable)
    true_part = []
    false_part = []
    for item in iterator:
        if predicate(item):
            true_part.append(item)
        else:
            if behavior == "left":
                true_part.append(item)
            elif behavior == "right":
                false_part.append(item)

            false_part.extend(iterator)
            break
    return true_part, false_part


def compact(lst):
    """Remove Nones from the list."""
    return [x for x in lst if x is not None]
