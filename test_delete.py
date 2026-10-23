import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

student_id = 9
url = f"http://127.0.0.1:5000/students/{student_id}"

request = Request(url, method="DELETE")

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