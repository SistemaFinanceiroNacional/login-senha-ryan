from drivers.Web import httpResponse

counter = 0

def root(request):
    if request.getResource() == "/":
        global counter
        counter += 1
        response = httpResponse.httpResponse({}, f"Times clicked: {counter}", 200)
        return response

    else:
        return httpResponse.httpResponse({}, "", 404)