from __future__ import annotations

from pyf_collection import PyFCollection

if __name__ == "__main__":
    """map"""
    resul1 = (PyFCollection(["Hello", "world"])
            .map(lambda s: s.upper())
            .to_list())
    print(resul1)

    """flatMap"""
    resul2 = (PyFCollection(["Hello", "functional", "world", "python"])
            .flat_map(lambda s: PyFCollection([f"-{s}-", f"${s}$"]))
            .to_list())
    print(resul2)

    """filter"""
    resul3 = (PyFCollection(["Hello", "functional", "world", "python"])
            .filter(lambda s: s != "python")
            .map(lambda s: s.upper())
            .to_list())
    print(resul3)

    """find"""
    exit = (PyFCollection(["Hello", "functional", "world", "python"])
            .exist(lambda s: s == "python"))
    print(exit)

    """exist"""
    resul4 = (PyFCollection(["Hello", "functional", "world", "python"])
            .find(lambda s: s == "functional"))
    print(resul4)

    """fold"""
    resul5 = (PyFCollection([1, 2, 3, 4, 5])
            .fold(0, lambda acc, n: acc + n))
    print(resul5)

    """take"""
    resul6 = (PyFCollection([1, 2, 3, 4, 5])
            .take(3)
            .to_list())
    print(resul6)

    """drop"""
    resul7 = (PyFCollection([1, 2, 3, 4, 5])
            .drop(3)
            .to_list())
    print(resul7)

    """distinct"""
    resul8 = (PyFCollection([1, 2, 3, 4, 5])
            .distinct(3)
            .to_list())
    print(resul8)

    """slice"""
    resul9 = (PyFCollection([1, 2, 3, 4, 5])
            .slice(2,4)
            .to_list())
    print(resul9)
