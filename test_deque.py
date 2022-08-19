import deque

def test_deque_using_isEmpty1():
    assert deque.deque().isEmpty()

def test_deque_using_isEmpty_2():
    d = deque.deque()
    d.appendLast("strElement")
    assert not d.isEmpty()

def test_deque_using_append_1():
    d = deque.deque()
    d.appendLast(1)
    assert not d.isEmpty()

def test_deque_using_append_2():
    d = deque.deque()
    d.appendLast(1)
    d.appendLast(2)
    d.appendLast(3)
    assert d.list == [1, 2, 3]

def test_deque_using_popLast_1():
    d = deque.deque()
    d.appendLast(1)
    d.popLast()
    assert d.isEmpty()

def test_deque_using_popLast_2():
    d = deque.deque()
    d.appendLast(1)
    d.appendLast(2)
    d.appendLast(3)
    d.popLast()
    assert d.list == [1, 2]

def test_deque_using_peekLast_1():
    d = deque.deque()
    d.appendLast(1)
    d.appendLast("2")
    assert d.peekLast() == "2"

def test_deque_using_peekLast_2():
    d = deque.deque()
    d.appendLast(1)
    d.appendLast("2")
    d.appendLast(4)
    d.appendLast(("tupleTest",))
    assert d.peekLast() == ("tupleTest",)

def test_deque_using_peekLast_when_deque_has_one_value():
    d = deque.deque()
    d.appendLast(1)
    assert d.peekLast() == 1

def test_deque_using_peekFirst_1():
    d = deque.deque()
    d.appendLast(1)
    d.appendLast("2")
    d.appendLast(3)
    assert d.peekFirst() == 1

def test_deque_using_peekFirst_2():
    d = deque.deque()
    d.appendLast("firstElement")
    d.appendLast("2")
    d.appendLast(3)
    assert d.peekFirst() == "firstElement"

def test_deque_using_appendFirst_1():
    d = deque.deque()
    d.appendLast("firstElement")
    d.appendLast("2")
    d.appendFirst(1)
    assert d.list[0] == 1

def test_deque_using_appendFirst_2():
    d = deque.deque()
    d.appendLast("firstElement")
    d.appendLast("2")
    d.appendFirst(1)
    d.appendFirst(4)
    d.appendFirst("random_str")
    assert d.list[0] == "random_str"

def test_deque_using_popFirst_1():
    d = deque.deque()
    d.appendLast(1)
    d.appendLast(2)
    d.appendLast(3)
    d.appendLast(4)
    d.popFirst()
    assert d.peekFirst() == 2

def test_deque_using_popFirst_2():
    d = deque.deque()
    d.appendFirst(1)
    d.appendFirst(2)
    d.appendFirst(3)
    d.appendFirst(4)
    d.popFirst()
    assert d.peekFirst() == 3

def test_deque_using_upwards():
    d = deque.deque()
    d.appendFirst(1)
    d.appendFirst(2)
    d.appendFirst(3)
    d.appendFirst(4)
    upwardsIterable = d.upwards()
    listTest = [4, 3, 2, 1]
    assert listTest == list(upwardsIterable)

def test_deque_using_downwards():
    d = deque.deque()
    d.appendFirst(1)
    d.appendFirst(2)
    d.appendFirst(3)
    d.appendFirst(4)
    upwardsIterable = d.downwards()
    listTest = [1, 2, 3, 4]
    assert listTest == list(upwardsIterable)