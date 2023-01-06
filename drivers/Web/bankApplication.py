from Web import httpResponse

counter = 0

def root(request):
    global counter
    counter += 1
    response = httpResponse.httpResponse({}, f"Times clicked: {counter}", 200)
    return response