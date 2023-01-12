import uuid
import urllib.parse

params = {
    "response_type": 'code',
    "client_id": "0a9306c3f71745a29297ebf24323992a",
    "scope": "user-top-read",
    "redirect_uri": "http://localhost:8888/callback",
    "state": str(uuid.uuid4())
}

url_test = urllib.parse.urlencode(params)
print(url_test)