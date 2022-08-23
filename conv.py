import json
import requests


def unmarshal(data):
    result = [{}]
    for i in data.strip().split('\n'):
        pos = i.find('{')
        command = i[:pos]
        try:
            message = json.loads(i[pos:])
        except Exception:
            message = {}
            continue
        message['command'] = command
        result.append(message)

    return result[1:] if len(result) > 1 else result


def marshal(data):
    return data.pop('command') + json.dumps(data, separators=(',', ':')).replace("{}", '') + '\n'


def getservers():
    data = requests.get('http://static.rstgames.com/durak/servers.json', headers={
        'User-Agent': 'FoolAndroid/1.9.8 Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/QP1A.190711.020)'
    }).json()
    return [(data['user'][server]['host'], data['user'][server]['port']) for server in data['user'] if server != "u0"]
