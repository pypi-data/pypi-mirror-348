from collections.abc import (
    Iterator,
    Iterable,
    Callable,
    Mapping,
    MutableMapping,
    ItemsView,
    ValuesView,
    KeysView
)
from typing import Any, overload, Optional, TypeVar, Union

K = TypeVar("K")
V = TypeVar("V")


class IndexedDict(MutableMapping[K, V]):
    """
    A dictionary that preserves insertion order and allows index-based operations.

    In addition to all the usual dict methods (key lookup, iteration, membership,
    pop, update, etc.), you can also:

        - Access by integer index:         `d.get_from_index(i)` or `d[i]` if
            you slice.
        - Get the key at a given index:    `d.get_key_from_index(i)`.
        - Remove by index:                 `d.pop_from_index(i)` or `del d[i:j]`.
        - Insert at an arbitrary position: `d.insert(idx, key, value)`.
        - Move an existing key:            `d.move_to_index(key, new_idx)`.
        - Slice the dict in order:         `d[1:4]`, `del d[2:5]`,
            `d[0:3] = […]`.
        - Sort by key or custom function:  `d.sort()` or
            `d.sort(key=…, reverse=…)`.
        - Export back to a plain dict:     `d.to_dict()`.

    Internally, self._index holds the keys in insertion (or user-reordered)
    order and self._dict maps keys → values for O(1) lookup.
    """

    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, data: Mapping[K, V]) -> None: ...
    @overload
    def __init__(self, data: Mapping[K, V], **kwargs: V) -> None: ...
    @overload
    def __init__(self, data: Iterable[tuple[K, V]]) -> None: ...
    @overload
    def __init__(self, data: Iterable[tuple[K, V]], **kwargs: V) -> None: ...
    @overload
    def __init__(self, data: None = None, **kwargs: V) -> None: ...
    def __init__(
        self,
        data: Mapping[K, V] | Iterable[tuple[K, V]] | None = None,
        **kwargs: V,
    ) -> None:
        """
        Initialize an IndexedDict.

        Args:
            data (Mapping[K, V] | Iterable[tuple[K, V]] | None, optional): Initial data.
                Defaults to None.
            **kwargs (V): Additional key-value pairs to add to the IndexedDict.
        """
        self._index: list[K] = []
        self._dict: dict[K, V] = {}
        if data is None:
            data = {}
        self._add_data(self, data, **kwargs)

    def __setitem__(
        self, key_or_slice: Union[K, slice], value: Union[V, Iterable[V]]
    ) -> None:
        """
        Assign value(s).

        - If key_or_slice is a single key, behave like dict: insert or replace.
        - If key_or_slice is a slice, value must be an iterable of new values;
          replaces the values at those positions without changing keys.
        """
        if isinstance(key_or_slice, slice):
            keys = self._index[key_or_slice]
            if not isinstance(value, Iterable) or isinstance(
                value, (str, bytes)
            ):
                raise TypeError(
                    "Slice assignment requires a non-string iterable of values"
                )
            vals = list(value)
            if len(vals) != len(keys):
                raise ValueError("Slice assignment length mismatch")
            for k, v in zip(keys, vals):
                self._dict[k] = v
        else:
            if key_or_slice not in self._dict:
                self._index.append(key_or_slice)
            self._dict[key_or_slice] = value  # type: ignore
            # A Generic V can be an Iterable of a Generic V,
            # despite the type error

    def __getitem__(self, key_or_slice: Union[K, slice]) -> Any:
        """
        Retrieve item(s).

        - If key_or_slice is a key, return its value.
        - If key_or_slice is a slice, return a list of values in that index range.
        """
        if isinstance(key_or_slice, slice):
            return [self._dict[k] for k in self._index[key_or_slice]]
        return self._dict[key_or_slice]

    def __delitem__(self, key_or_slice: Union[K, slice]) -> None:
        """
        Delete entry(ies).

        - If key_or_slice is a key, remove that key and its value.
        - If key_or_slice is a slice, remove all keys in that index range.
        """
        if isinstance(key_or_slice, slice):
            for k in self._index[key_or_slice]:
                del self._dict[k]
            del self._index[key_or_slice]
        else:
            key = key_or_slice
            if key not in self._dict:
                raise KeyError(key)
            self._index.remove(key)
            del self._dict[key]

    def __eq__(self, other: object) -> bool:
        """Test for equality."""
        if isinstance(other, IndexedDict):
            return list(self.items()) == list(other.items())
        return self.to_dict() == dict(other) if isinstance(other, Mapping) else False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __or__(self, other: Mapping[K, V]) -> "IndexedDict[K, V]":
        new = self.copy()
        new.update(other)
        return new

    def __ior__(self, other: Mapping[K, V]) -> "IndexedDict[K, V]":
        self.update(other)
        return self

    def __len__(self) -> int:
        """Return number of entries."""
        return len(self._index)

    def __iter__(self) -> Iterator[K]:
        """Yield keys in their current order."""
        return iter(self._index)

    def __repr__(self) -> str:
        items = ", ".join(f"{k!r}: {self._dict[k]!r}" for k in self._index)
        return f"{self.__class__.__name__}({{{items}}})"

    def __str__(self) -> str:
        return str({k: self._dict[k] for k in self._index})

    def __contains__(self, key: object) -> bool:
        """Tests membership in the dict."""
        return key in self._dict

    def __bool__(self) -> bool:
        """Checks if dict is non-empty."""
        return bool(self._dict)

    def __reversed__(self) -> Iterator[K]:
        """Iterates keys in reverse order."""
        return reversed(self._index)

    def __copy__(self) -> "IndexedDict[K, V]":
        return self.copy()

    # ——— Private Methods ———
    @staticmethod
    def _add_data(
        _obj: "IndexedDict[K, V]",
        _data: Union[Mapping[K, V], Iterable[tuple[K, V]]],
        **kwargs: V,
    ) -> None:
        if isinstance(_data, Mapping):
            for k, v in _data.items():
                if k not in _obj._dict:
                    _obj._index.append(k) # type: ignore
                _obj._dict[k] = v # type: ignore
        elif isinstance(_data, Iterable):
            for k, v in _data:
                if k not in _obj._dict:
                    _obj._index.append(k)
                _obj._dict[k] = v
        elif _data is not None:
            raise TypeError(
                "_data must be a mapping or iterable of (key, value) pairs"
            )

        for k, v in kwargs.items():
            if k not in _obj._dict:
                _obj._index.append(k)  # type: ignore
            _obj._dict[k] = v  # type: ignore

    # ——— Public Methods ———
    def position(self, key: K) -> int:
        """Return the position index of a key"""
        return self._index.index(key)

    def get_from_index(self, index: int) -> V:
        """
        Return the value at a given insertion-index.
        Raises IndexError if out of range.
        """
        return self._dict[self._index[index]]

    def get_key_from_index(self, index: int) -> K:
        """
        Return the key at a given insertion-index.
        Raises IndexError if out of range.
        """
        return self._index[index]

    def pop_from_index(self, index: int) -> V:
        """
        Remove and return the value at a given index.
        Shifts subsequent items left.
        """
        key = self._index.pop(index)
        return self._dict.pop(key)

    def to_dict(self) -> dict[K, V]:
        """
        Export to a plain built-in dict, preserving current order.
        """
        return {k: self._dict[k] for k in self._index}

    # ——— List-like Methods ———
    def insert(self, index: int, key: K, value: V) -> None:
        """
        Insert a new key/value at the given index and shifts subsequent items
        to the right.

        Raises KeyError if key already present.
        """
        if key in self._dict:
            raise KeyError("insert(): key already present")

        if index < 0:
            index = max(0, len(self._index) + index)

        index = min(index, len(self._index))
        new_index_list = []
        new_dict = {}

        keys_before = self._index[:index]
        keys_after = self._index[index:]

        for k in keys_before:
            new_index_list.append(k)
            new_dict[k] = self._dict[k]

        new_index_list.append(key)
        new_dict[key] = value

        for k in keys_after:
            new_index_list.append(k)
            new_dict[k] = self._dict[k]

        self._index = new_index_list
        self._dict = new_dict

    def move_to_index(self, key: K, new_index: int) -> None:
        """
        Relocate an existing key to a new index position.
        Raises KeyError if key is not present.
        """
        if key not in self._dict:
            raise KeyError(key)

        value = self._dict[key]
        self._index.remove(key)
        del self._dict[key]
        if new_index < 0:
            new_index = len(self._index) + new_index + 1
        new_index = max(new_index, 0)
        new_index = min(new_index, len(self._index))
        new_index_list = []
        new_dict = {}

        keys_before = self._index[:new_index]
        keys_after = self._index[new_index:]

        for k in keys_before:
            new_index_list.append(k)
            new_dict[k] = self._dict[k]

        new_index_list.append(key)
        new_dict[key] = value

        for k in keys_after:
            new_index_list.append(k)
            new_dict[k] = self._dict[k]
        self._index = new_index_list
        self._dict = new_dict

    def sort(
        self,
        *,
        key: Optional[Callable[[K], Any]] = None,
        reverse: bool = False,
    ) -> None:
        """
        Sort keys in-place.

        Args:
            key: optional function mapping a key → comparison key. If None,
                sorts by key.
            reverse: if True, reverse the sort order.
        """
        self._index.sort(key=key, reverse=reverse)  # type: ignore
        self._dict = {k: self._dict[k] for k in self._index}

    # ——— Standard‐API Methods (dict‐like) ———

    def keys(self) -> KeysView[K]:
        """Return a view of keys."""
        return self._dict.keys()

    def values(self) -> ValuesView[V]:
        """Return a view of values."""
        return self._dict.values()

    def items(self) -> ItemsView[K, V]:
        """Return a view of key/value pairs."""
        return self._dict.items()

    def clear(self) -> None:
        """Remove all items."""
        self._index.clear()
        self._dict.clear()

    def copy(self) -> "IndexedDict[K, V]":
        """Return a shallow copy of the IndexedDict."""
        new = self.__class__()
        new._index = self._index.copy()
        new._dict = self._dict.copy()
        return new

    def pop(self, key: K, default: Any = ...) -> V:
        """
        Remove specified key and return its value.
        Return default if not found and default is provided.
        Raise KeyError if key not found and default not provided.
        """
        if key in self._dict:
            self._index.remove(key)
            return self._dict.pop(key)
        if default is not ...:
            return default
        raise KeyError(key)

    def popitem(self) -> tuple[K, V]:
        """
        Remove and return the last key/value pair.
        Raises KeyError if empty.
        """
        if not self._index:
            raise KeyError("popitem(): dictionary is empty")
        key = self._index.pop()
        return key, self._dict.pop(key)

    def setdefault(self, key: K, default: Optional[V] = None) -> V:
        """
        If key in dict: return its value.
        Else: insert key with default and return default.
        """
        if key not in self._dict:
            self._index.append(key)
            self._dict[key] = default  # type: ignore
        return self._dict[key]

    def update(self, *args, **kwargs: V) -> None:
        """
        Update with key/value pairs from another mapping, iterable, or kwargs.
        """
        if len(args) > 1:
            raise TypeError(
                f"update expected at most 1 argument, got {len(args)}"
            )
        elif not args:
            data = None
        else:
            data = args[0]

        if data is None and kwargs:
            for k, v in kwargs.items():
                if k not in self._dict:
                    self._index.append(k)  # type: ignore
                self._dict[k] = v  # type: ignore
        elif isinstance(data, (Mapping, Iterable)):
            self._add_data(self, data, **kwargs)
        elif data is not None:
            raise TypeError(
                "update() must be a mapping or iterable of key/value pairs"
            )

    # ——— Class Methods ———
    @classmethod
    def fromkeys(
        cls, iterable: Iterable[K], value: Optional[V] = None
    ) -> "IndexedDict[K, V]":
        """
        Create a new IndexedDict with keys from iterable and all values set
        to value.
        """
        new = cls()
        for k in iterable:
            new._index.append(k)
            new._dict[k] = value  # type: ignore
        return new

    @classmethod
    def fromitems(
        cls, data: Union[Mapping[K, V], Iterable[tuple[K, V]]]
    ) -> "IndexedDict[K, V]":
        """
        Create a new IndexedDict with key/value pairs from iterable.
        """
        new = cls()
        new._add_data(new, data)
        return new
