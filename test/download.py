import requests

resp = requests.get(
    "https://images.unsplash.com/photo-1596107034181-9f168717f1ee?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60",
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'})

with open("a.jpeg", 'rw') as f:
    f.write(resp.content)
