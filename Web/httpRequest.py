def cache(func_f):
    cachedValues = {}

    def wrapper(*args, **kwargs):
        key = str((args, kwargs))
        if key in cachedValues:
            return cachedValues[key]
        else:
            cachedValues[key] = func_f(*args, **kwargs)
            return cachedValues[key]
    return wrapper


class httpRequest:
    def __init__(self, socket):
        self.socket = socket

    @cache
    def head(self):
        header = {}
        FirstLine = 0
        FirstLineWithCarriageReturn = 1
        NameOfHeader = 2
        NameOfHeaderWithCarriageReturn = 3
        ValueOfHeaderWithSpace = 4
        ValueOfHeader = 5
        ValueOfHeaderWithCarriageReturn = 6
        NewNameOfHeader = 7
        MaybeFinalState = 9
        FinalState = 10
        state = FirstLine

        headerName = b''
        headerValue = b''

        while state != FinalState:
            nextByte = self.socket.recv(1)

            if nextByte == b'':
                raise 42

            if nextByte == b'\r' and state == FirstLine:
                state = FirstLineWithCarriageReturn

            elif nextByte == b'\n' and state == FirstLineWithCarriageReturn:
                state = NameOfHeader

            elif nextByte == b'\r' and state == NameOfHeader:
                state = FinalState

            elif nextByte != b':' and state == NameOfHeader:
                headerName += nextByte

            elif nextByte == b':' and state == NameOfHeader:
                state = ValueOfHeaderWithSpace

            elif nextByte == b'\r' and state == NameOfHeader:
                state = NameOfHeaderWithCarriageReturn

            elif nextByte == b'\n' and state == NameOfHeaderWithCarriageReturn:
                state = FinalState

            elif nextByte == b' ' and state == ValueOfHeaderWithSpace:
                state = ValueOfHeader

            elif nextByte != b'\r' and state == ValueOfHeader:
                headerValue += nextByte

            elif nextByte == b'\r' and state == ValueOfHeader:
                state = ValueOfHeaderWithCarriageReturn

            elif nextByte == b'\n' and state == ValueOfHeaderWithCarriageReturn:
                state = NewNameOfHeader
                header[headerName] = headerValue
                headerName = b''
                headerValue = b''

            elif nextByte == b'\r' and state == NewNameOfHeader:
                state = MaybeFinalState

            elif nextByte == b'\n' and state == MaybeFinalState:
                state = FinalState

            elif nextByte != b':' and state == NewNameOfHeader:
                headerName += nextByte
                state = NameOfHeader

        return header

