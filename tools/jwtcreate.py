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
        'kid': '2254fdf6d63e3d503dbc3de4628f7c07c63206d1',
        'alg': 'RS256',
        'typ': 'JWT'}
    payload = {
        'iss': 'fhir-351@nfsepsisanalysis.iam.gserviceaccount.com',
        'sub': 'fhir-351@nfsepsisanalysis.iam.gserviceaccount.com',
        'aud': 'https://healthcare.googleapis.com/',
        'iat': iat,
        'exp': exp
    }
    signed_jwt = jwt.encode(payload, '-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCnl7/EOPguzXi2\nVvfrgZHE3KcJhqeiua2rdpfWTnfOgtWRL15nTsxOhu6QgbT9iMOsZ8K5TJwLuqh9\nGC6r0jYJt8RUOQUD//JerMOLOlkk0qVp9J2nW507/Hmvc5cZL0Uqqv3al84ntk6V\nTjIwltVm7FFqV13FmANvHY9dHbmBrsmH87blPSv2F6cnHNDUyDp1JeTOitY7qQA3\n3GQ/C7Iy0TUf0CqnguN/nJ3bfZJsdxGCeHUjG3rc6YJDLFkA2JYWK2NsC6aV+L/8\nnLPc4kqIRpCpXFe28xgw3sRfvnrKNQaL8l3IdCLG7U5WuxCVtoQIDn0hq3YiPudL\nxwRBLaMRAgMBAAECggEAClmxYr1/+mf/Nget/RH9/jIAcPKrhL3B74599yLWfF8R\nMIvD4U55CLqFnlAcbPIW351y5b3I/2JySHOHYl4zryr1yZvR5vrWLamu0/jxC3ik\n9aPBXtYmIk/H9iGF6ezE8UspLWhlt4cnWEpBiEWwfVBIAPDPXkYypBinw4Dz9YHL\n3ij+4mJ81HH/6f7FHhSbh2+vIPKOj/SUOjmq3vdkFwoPCjB+DDPyUveVdMaNlHKp\nGm08PwGSpqcfzG/if9fAVbV1AHLOzuhY9Jh/g0TJ8qo8YqxdM2vatpGgxrirvhrZ\nybFE1F0SJuvmim76Aea5UOjRG96oIGPsEVJ792IkAQKBgQDX4why3ijUfHRdtJFr\nCBckuBSUkkWxeHe+3HBuYX9UuAGbsS30MpX3Wuyl6dMhq2hoNBze/uCzBchqFXeW\n7KYHJevQPHMLrlikpiC7TV9kuRWjCqxz9HqB3KZGcrqQ3ccaxMKERZ5C0jS878n4\nyBirE6dEFlQlbRHKsiGYYXRDkQKBgQDGu4oEiIbG7IpP/nibCHKeo1ftPhey2bM4\nY125K2w7K+4cqHDtQ/CGol5p9YX8kNis165ugDR6ODsHkmMDTkaY1uYQfO4R3MS0\nd5D+jWev3GYFwUzRdnE96W9WqGTACQsqI4bY3sYoD2ifrNzDHuB3aptm62pKSPRJ\nBGAdK0SngQKBgBKCea/3kkKdpRB/sdQebnWMft86J1WPAZ1QoycjntoxqJmjuE/u\nomMB3bZf9OU3IA2HIk6QRc2zmjpWOtmq0pVcT/qbpDWFLj53q+jDOoGVSOCgwqZy\neKp3s53oqkxPZ4nJAvB6U5ZhFXp5iLSW216Xoci5rV9EGblqSm0ZNfGxAoGAUjXs\nn3l2/72Ebhkf/UpeWB/MVNk15ofGaxI4CEzdRhEjPHm11YEgdCGhGwY1ekjVSZMj\nlpS0oMa4LKazDQAJllp36+Qye/Mu8FTyB0up1AdBsSnIxHHR4MG7jEa2/vX+x1zR\nANAPeyz8o+lXneQdCWlxhf7nBnntjHMh648lpIECgYBi73HkGRTFFW+bkm3pbo9V\nBL0L2jmp2Y5yZQSnSO3qVgBqBl6ra7X8/rK7dWTDKciK1DdKOzkUQ1I8IuBSr+65\nVnNtiTljYDetsT2HZwdCyY8M7fXh7UxCZnZ8YBoP/DcadSyNQubpES7AGq6LOfKg\nPn7E9bzjj2hqDaUiAyv37Q==\n-----END PRIVATE KEY-----\n', headers=additional_headers, algorithm='RS256')
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