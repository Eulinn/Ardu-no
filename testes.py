import requests


try:
    rq = requests.get('http://192.168.0.101/?relay0=off')
except OSError as erro:
    print(erro)



print(rq.text)




