from drivers.Web import httpResponse

counter = 0

def root(request):
    if request.getResource() == "/":
        global counter
        counter += 1
        with open("drivers/Web/root/index.html") as index:
            indexContent = index.read()

        response = httpResponse.httpResponse({"Content-Type": "text/html"}, indexContent.replace("{counter}", str(counter)), 200)
        return response

    else:
        return httpResponse.httpResponse({}, "", 404)