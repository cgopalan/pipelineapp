import json


def parse_request(request):
    """Gets coin ids from request depending on header"""
    parsed = []
    if request.headers["Content-Type"] == "text/csv":
        parsed = parse_csv(request.data)
        print(f"CSV parsed: {parsed}")
    elif request.headers["Content-Type"] == "application/json":
        parsed = parse_json(request.data)
        print(f"JSON parsed: {parsed}")
    else:
        # Header unknown
        print("Header type unknown")
    return parsed


def parse_csv(input):
    # We dont want the first line which is "coin"
    return input.split(b"\n")[1:]


def parse_json(input):
    # Return the value of the dict which is the list of ids
    return json.loads(input)["coins"]
