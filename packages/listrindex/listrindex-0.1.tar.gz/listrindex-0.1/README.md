# listrindex

A lightweight Python utility that allows you to find the **last index** of an element in a list — something the built-in `list.index()` method does not support.

---

## 📌 Description

In Python, `list.index(x)` returns the **first index** of `x` in a list.  
The `listrindex` class provides the method `rindex(list, object)` that returns the **last index** where the object appears.

This is especially useful when working with large datasets or when you want to find the last occurrence of repeated elements.

---

## ✅ Features

- Returns the **last index** of a given value in a list.
- Works with integers, strings, or any data type.
- Raises `ValueError` if the element is not found, just like `list.index()`.

---

## 🧪 Usage

```python
from listrindex import listrindex

mylist = [5, 3, 7, 3, 9, 3]
value = 3

r = listrindex()
print(r.rindex(mylist, value))  # Output: 5 (last index of 3)
