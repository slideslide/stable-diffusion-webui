import requests
url = "http://127.0.0.1:7861"
payload = {
    "text": "puppy dog",
}
resp =  requests.post(url=f"{url}/nlp/v1/match",json=payload)
r=resp.json()
print(r)