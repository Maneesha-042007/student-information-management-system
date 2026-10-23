import json
import urllib.request
import urllib.error

url = "http://127.0.0.1:5000/students"

data = {
    "name": "Test Student",
    "department": "CSE",
    "email": "namita_22102026_8683@example.com"
}

request = urllib.request.Request(
    url,
    data=json.dumps(data).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))
        print("Status:", response.status)
        print("Response:", result)

        # Save the new student's ID for PUT and DELETE
        if "id" in result:
            with open("test_student_id.txt", "w") as file:
                file.write(str(result["id"]))
            print("Student ID saved:", result["id"])

except urllib.error.HTTPError as error:
    print("Status:", error.code)
    print("Error:", error.read().decode("utf-8"))

except urllib.error.URLError as error:
    print("Connection error:", error.reason)
    print("Make sure Flask is running.")