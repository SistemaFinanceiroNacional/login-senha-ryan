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


class DInterface:
    pass


class D(DInterface):
    def __init__(self, num: int, a: A):
        self.a = a
        self.num = num


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


def test_set_an_item():
    di = DiContainer()
    a = A()
    di[A] = a
    assert di[A] == a


def test_construct_and_set_an_item():
    di = DiContainer()
    c = di[C]
    b = c.b
    di[B] = b
    assert c.b == di[B]


def test_set_parameters_and_construct():
    di = DiContainer()
    di.set_parameter('num', 2)
    d = di[D]
    assert d.num == 2


def test_provide_d_interface():
    di = DiContainer()
    di.provide(DInterface, D)
    di.set_parameter('num', 2)
    obj = di[DInterface]
    assert isinstance(obj, D)


def test_provide_d_interface_equals_di_object():
    di = DiContainer()
    di.provide(DInterface, D)
    di.set_parameter('num', 2)
    obj1 = di[D]
    obj2 = di[DInterface]
    assert obj1 == obj2
