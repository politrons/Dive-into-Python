from __future__ import annotations

from pyf_collection import PyFCollection

if __name__ == "__main__":
    """map"""
    list = (PyFCollection(["Hello", "world"])
            .map(lambda s: s.upper())
            .to_list())
    print(list)

    """flatMap"""
    list = (PyFCollection(["Hello", "functional", "world", "python"])
            .flat_map(lambda s: PyFCollection([f"-{s}-", f"${s}$"]))
            .to_list())
    print(list)

    """filter"""
    list = (PyFCollection(["Hello", "functional", "world", "python"])
            .filter(lambda s: s != "python")
            .map(lambda s: s.upper())
            .to_list())
    print(list)

    """find"""
    exit = (PyFCollection(["Hello", "functional", "world", "python"])
            .exist(lambda s: s == "python"))
    print(exit)

    """exist"""
    list = (PyFCollection(["Hello", "functional", "world", "python"])
            .find(lambda s: s == "functional"))
    print(list)

    """fold"""
    list = (PyFCollection([1, 2, 3, 4, 5])
            .fold(0, lambda acc, n: acc + n)
            .to_list())
    print(list)

    """take"""
    list = (PyFCollection([1, 2, 3, 4, 5])
            .take(3)
            .to_list())
    print(list)

    """drop"""
    list = (PyFCollection([1, 2, 3, 4, 5])
            .drop(3)
            .to_list())
    print(list)

    """distinct"""
    list = (PyFCollection([1, 2, 3, 4, 5])
            .distinct(3)
            .to_list())
    print(list)

    """slice"""
    list = (PyFCollection([1, 2, 3, 4, 5])
            .slice(2,4)
            .to_list())
    print(list)

