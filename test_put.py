import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

url = "http://127.0.0.1:5000/students/8"

data = {
    "name": "Namita Updated",
    "department": "CSE AI&ML",
    "email": "namita_22102026_7462@example.com"
}

request = Request(
    url,
    data=json.dumps(data).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="PUT"
)

try:
    with urlopen(request) as response:
        print("Status:", response.status)
        result = json.loads(response.read().decode("utf-8"))
        print(json.dumps(result, indent=4))

except HTTPError as error:
    print("Status:", error.code)
    print(error.read().decode("utf-8"))

except URLError as error:
    print("Connection error:", error.reason)