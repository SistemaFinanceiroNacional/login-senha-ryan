from infrastructure.dicontainer import DiContainer


class A:
    pass


class B:
    def __init__(self, a: A):
        self.a = a


class C:
    def __init__(self, a: A, b: B):
        self.a = a
        self.b = b


def test_no_dependency_class():
    di = DiContainer()
    a = di[A]
    assert isinstance(a, A)


def test_simple_dependency_class():
    di = DiContainer()
    b = di[B]
    assert isinstance(b, B)


def test_simple_dependency_class_attribute():
    di = DiContainer()
    b = di[B]
    assert isinstance(b.a, A)


def test_multiple_dependencies_class():
    di = DiContainer()
    c = di[C]
    assert c.a == c.b.a


def test_set_item_1():
    di = DiContainer()
    a = A()
    di[A] = a
    assert di[A] == a


def test_construct_and_set():
    di = DiContainer()
    c = di[C]
    b = c.b
    di[B] = b
    assert c.b == di[B]
