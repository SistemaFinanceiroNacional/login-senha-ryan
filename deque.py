class deque:
    def __init__(self):
        self.list = []

    def isEmpty(self):
        return len(self.list) == 0

    def appendLast(self, elementToInsert):
        self.list.append(elementToInsert)

    def appendFirst(self, elementToInsert):
        self.list.insert(0, elementToInsert)

    def popLast(self):
        self.list.pop()

    def popFirst(self):
        self.list.remove(self.list[0])

    def peekLast(self):
        return self.list[-1]

    def peekFirst(self):
        return self.list[0]

    def upwards(self):
        return upwards(self.list)

    def downwards(self):
        return downwards(self.list)


class upwards:
    def __init__(self, list):
        self.list = list
        self.indice = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.indice == len(self.list):
            raise StopIteration()

        elen = self.list[self.indice]
        self.indice += 1
        return elen

class downwards:
    def __init__(self, list):
        self.list = list
        self.indice = len(self.list)-1

    def __iter__(self):
        return self

    def __next__(self):
        if self.indice == -1:
            raise StopIteration()

        elen = self.list[self.indice]
        self.indice -= 1
        return elen

if __name__ == "__main__":
    d = deque()
    d.appendLast(1)
    d.appendLast(2)
    d.appendLast(3)
    d.appendLast(4)
    d.appendLast(5)
    dequeIterable = d.downwards()
    for i in dequeIterable:
        print(i)
