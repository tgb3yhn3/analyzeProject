import random
import string
import time
import jwt

# JWT_SECRET = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for x in range(10))
JWT_SECRET = 'Y5bkLxSvCVzhDr7FVIatEJ-n93jDbJ8-1X2_Sn'


def createJWT_FHIR():
    iat = time.time()
    exp = iat + 3600
    additional_headers = {
        'kid': 'b1113043ddb299f187ab44249a8e8c94d3124f9b',
        'alg': 'RS256',
        'typ': 'JWT'}
    payload = {
        'iss': 'fhir-281@agile-device-389611.iam.gserviceaccount.com',
        'sub': 'fhir-281@agile-device-389611.iam.gserviceaccount.com',
        'aud': 'https://healthcare.googleapis.com/',
        'iat': iat,
        'exp': exp
    }
    signed_jwt = jwt.encode(payload, '-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQClk3HV0iT2rAkC\nyVZB2qDWwACTwrVIyIFoIB2ct3p6zWouTDU8yboFs1H0eChMcKYYjVfrgllyCF20\nd/jI6UuEXSeGJTHvxLb7cEqYkOGn5aA8i2WjiCSs1zzBim+3Kcl+xJ0H3Y7tVezR\nGNb+ms9nIRejspI1zRTgrJdU0cBMDZ/C5QQCoNe+k0Nl66RNyQfPx7pT2YGb6cJI\nT/Tv0uOggWxHjfBNyoJ9xsJTCBtxUxTM54hRP5BOSVVRP5nKzTA5EbjvqMKWvYYL\n3Ew4oSHPym/Y6jZmsZnMPxL+5BkccpHWt4QWdg0D2wMlHQhoMLV2X9Mx8wMVoUSJ\nH+l7xEAhAgMBAAECggEAEfi55H7XlQAZhshGcOWraz/CGEesIFsmA6Cnwiq+lC1v\nWtjZ9vAA3U1IRhgULK7V8miGDFmUvo42qIfUlK8Qy6xGRdbL76XLBCndKOfh3FTN\n0oCBXtGARJPko++0Hj3+gUBTOIc1dCCNUKlI7a/tNtkGTTXszYLl4xiMoO/W1tI/\niJH1EHdO+o5qkDiGOsEK+7TEb3ZSmr3q5lpNxUVHpLrE2ygJoC9Ysmy0Q911lzpi\nerbfpXp5x0xcbzu5tiBEGT1binOctxtVLE61Hsd5jtvgruUFlCo3Ucu81rbWMtx5\nwPtHMLAlxsC2fjU6il8hGRS1GeTt0mvLxQ6g55KBCQKBgQDT5hdx44gp7c13Zoxc\niFkzCRSTkJ5+dYsLaO9+KAHu0Z/tyThrJkpFkIx56+UGC8AMuV/AmZuYvwWAc8+y\n9hiYFo+E/6NO8uF2vsds859iedq9csiSXLWYvyxr/1/tpxJk4YLGJZmaJ/4B/1Vu\nMbvm+MwUVUBOs8wRsYZP8VOWOQKBgQDICUkBs8Pg4jVX8pM6I7ncK/55jzs1NSbH\nT0IDY7waoJNjC8E/BconWcy2n9HmRsqhgWCRD4GyWlD48dGhbF74LdQdv57FOQRT\nS+FVrB6ckDDKJWYNLD1HZQ3FYz5D4OvSDWTHzY2fHWYZNpirPHb527COjF7cjP8v\nlN4OTGK5KQKBgEMr0kzJCvX3q0VpXZ9LnbMe8sXgd02xJzWjux+rwQkarG7tdZQJ\n3Et3CgDwNXaYLPYboW3lg7yE+VKB49pgRuWXaUGI5BT3y18gFQnFpMXLyPp7M3eq\nKerU11kY6Cjm6F7QWetEKhADE3NApK082MrcHZ1odO0987e8Jc6bupqJAoGAFW+h\nSjRoZj33d3BARLe1YBm60G3/60jB2hPtQA29B6Fziealk8pcCnF+FYf051douXvy\nzDi8Lk+tY7AORd0mJDRNCc8SBZKBmyeDgznJof91qwPs9rZp7q+ulRt4fa+ptb3H\nsf2eEpIE8ei+3YLCQS5AslXqiHn3krLCRQf8gFkCgYEAoz38pS0X484N7P9uP6GV\nRuqRUWpECNPCM9SGOpVwktNLdsnQ6F9LrwDlR6D+oOM/iBG6CibFsrPpMjeTCXGW\nKaKsicYxQf7MYYy6PPUVEO++oTivd3fJj0C6AkQcCkcGg/bKBml/kyxsBDKi8beK\nx4LKYpG+KCPIlU2DV5GFaDY=\n-----END PRIVATE KEY-----\n', headers=additional_headers, algorithm='RS256')
    print('FHIR jwt token created')
    # print(signed_jwt)
    print(signed_jwt)
    return signed_jwt


def createJWT_user(username):
    iat = time.time()
    exp = iat + 3600
    additional_headers = {
        'alg': 'HS256',
        'typ': 'JWT'}
    payload = {
        'user_id': username,
        'iat': iat,
        'exp': exp
    }
    signed_jwt = jwt.encode(payload, JWT_SECRET,
                            headers=additional_headers, algorithm='HS256')
    print('user jwt token created')
    # print(signed_jwt)
    return signed_jwt


def verifyJWT_user(username='', token='') -> bool:
    '''驗證token'''
    payload = {'user_id': username}
    try:
        _payload = jwt.decode(token, JWT_SECRET, algorithms='HS256')
    except jwt.PyJWTError:
        print('token 解析失敗')
        return False
    else:
        # print(_payload)
        exp = int(_payload.pop('exp'))
        if time.time() > exp:
            print('token 已失效')
            return False
        if payload.get('user_id') != payload.get('user_id'):
            print('token 驗證失敗\n' + 'user_id = ' + payload.get('user_id') +
                  '_user_id = ' + _payload.get('user_id'))
        print('token 驗證成功：' + 'user_id = ' + _payload.get('user_id'))
        return True