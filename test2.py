import requests


url = 'http://172.31.2.36'

resp = requests.get(url)
resp.encoding='utf-8'

text = resp.text#.encode('utf-8')

print(text)