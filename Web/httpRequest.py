
class httpRequest:
    def __init__(self, socket):
        self.socket = socket

    def head(self):
        header = {}
        FirstLine = 0
        FirstLineWithCarriageReturn = 1
        NameOfHeader = 2
        NameOfHeaderWithCarriageReturn = 3
        ValueOfHeaderWithSpace = 4
        ValueOfHeader = 5
        ValueOfHeaderWithCarriageReturn = 6
        FinalState = 7
        state = FirstLine

        while state != FinalState:
            nextByte = self.socket.recv(1)
            headerName = b''
            headerValue = b''

            if nextByte == b'\r' and state == FirstLine:
                state = FirstLineWithCarriageReturn

            elif nextByte == b'\n' and state == FirstLineWithCarriageReturn:
                state = NameOfHeader

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
                state = FinalState


        return header
