import requests
url = "http://127.0.0.1:7861/nlp/v1/fetchurl"
payload = {
    "prompt": "puppy dog",
}
print(url)
resp =  requests.post(url=url,json=payload)
r=resp.json()
print(r)