import requests


try:
    rq = requests.get('http://192.168.0.101/?relay0=off')
    print(rq.text)
except OSError as erro:
    print(erro)







