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
        'kid': 'd776ecbe045ac7a6e721fb0ac59fccda9548382a',
        'alg': 'RS256',
        'typ': 'JWT'}
    payload = {
        'iss': 'healthcareapifhir@crack-will-380312.iam.gserviceaccount.com',
        'sub': 'healthcareapifhir@crack-will-380312.iam.gserviceaccount.com',
        'aud': 'https://healthcare.googleapis.com/',
        'iat': iat,
        'exp': exp
    }
    signed_jwt = jwt.encode(payload, '-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCprhLxuoVqVxM+\n8jJiwAKLNk5vNFneFXFbomYipKyGbu0AH74MiJLEnmplyD2F0rtzYjGpz4poXarQ\naGcpsRMC2UgOPDQu+srTJRhG0D7pIATa9f6tWaP/R5DsbqWp5E1qEFIVFrJabxYW\n0ZwWDEdfZPoFQOWpbs1Z2GztvRr9tENsytzkdh9CuhmfNW0KgeK4jYJXB8OWSOMb\n9XAPP/wwH2ejidtG3qv/hbWA3t0EPlVihz4EiokdZf3Lco4BfsxmMNJRb3tJC08C\nlmBAvd7SGLm8dQNqLZ/OSMfVp4SF1ysQ0dR/Lx6/UfH+JZ6/gPzOFpclKNqv9WKk\nuSAsE+/nAgMBAAECggEAAl4Bpr+j0gvnd9tSP+sOqLHTba9oT78syf6zClE2cDPi\nNZGXOnuVMlEUU0FVvaILgHB5YbWBdJsljC5zvmCQW1vLMND73qD3goWA5F4dbySn\nPLAGURud1Msel5jg0csGMGpDQV9ZVQZGDk8DaYXnbRmiX5rp0bW383VvDqemkpTl\nPoa3cTSAKNnz3jATfx1v7y9kErjqGuYgYcppJT/5Q/kOv/eoBAcvJDfQfQmQ/pZe\n4XCGi9/QZExQmfISqx0l9bi6tc1lQl8F9VM3PYtzyAKxZgBFSug/7cX14pNSucfB\nLo8Wi2JKwGlHtBxIlCf7jscWK/jR5Mq0FY4E1cYqfQKBgQDam9jU4+EISQVUncjo\n9830LOaqSLyWALzc3owaF/a0YcQJlJr3VZ9xS5x1oQkcNcMcrH82tkhq+WXexQa7\nBzxQU8O7L71QyD+fkAzJ8ub4bC7noAr4M0zk+LXzXZEHSYTuxHqMDZqY+0a78I6O\nYQaRtmszlXpfNC4sLe5AXb+JbQKBgQDGs8wTDPOO+vs578Da/ZhkXkFT384VPmQd\nCSu98DMhTVK39lp46d1TCvl8D5rkdmvgpzYax6d5U6y5j7xIj+1YotDp3SsLrrw/\nL6aDw9KKynimMO7Z+PYAeQHIYRwys7Jscvv/FIBwPHHzHLTnTONcxEBRtkUCZuzC\ng8bP1nL+IwKBgAhECEjUbPfROwBeDvCwHftzjy01HtxVHs8DIy0BZvSfFbh/A/UC\nKcsw3rOb6SpF5iC5bP32mnpg/7cSoBSGS4OGB0qWnYPmbnFsEu+33X/bJ1LevEty\nNSAbP1X6Xbd20i3tA+0zvnq2VZBZoipEBOmRijAjIMNkx7In8nBAmzNpAoGBAIRu\nSsIbrKyLzCq2B0QtJocmZsXe8PwppBHSDew+jeVRIqNnNq9FtvPk6Zhs0iAYaRfG\negHpNU5gnUrjaGq4OkkL4s8rT8guglpeiM1jEwzbmwOws1BlZJe2DqEdT+ze5Tjw\nfdFpOZ0UPCH67PsHvLUUO4X6RA4wyPVvXG8jD2sfAoGAH4oz9JaScfUjAaf0FHVR\nxpA8MXUlYa3qw8/JwWtvzaUWAx6rVRjKYc9y/SL58su7XXcZiO+jwn6SeAr3/kHC\ncsaYonxT3mW8BjpEzzin48EmY4FQMHThYJt9ND2G6Qno7v9n7+ngWmxAZxIqNRoh\nzenQIRU8F1o+hb2tnp4I4dc=\n-----END PRIVATE KEY-----\n', headers=additional_headers, algorithm='RS256')
    print('FHIR jwt token created')
    # print(signed_jwt)
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