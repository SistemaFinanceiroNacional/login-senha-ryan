import httpResponse

counter = 0

def root(request):
    global counter
    counter += 1
    response = httpResponse.httpResponse({b'Connection': b'close'}, f"Times clicked: {counter}".encode("utf-8"), 200)
    return response