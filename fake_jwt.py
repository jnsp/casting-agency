from jose import jwt

private_key = (
    '-----BEGIN PRIVATE KEY-----\n'
    'MIIBUwIBADANBgkqhkiG9w0BAQEFAASCAT0wggE5AgEAAkEAiRTQJ4g8GcKnRQMz'
    'tEWE2NxU2HJerjMlIhbaVfztJpMWZ70JvB1sG8JzVMc5mgaPEOQbBAHxz5EK9fOd'
    'W333YwIDAQABAkBRoRU7FUNEy8czr25woR00zi+wHJsI/OfV3unxXoYR+5GpR185'
    '4RVKSUw7aeDvLfBh2P32hqZ3fTNcniIoiexxAiEAv2wdlscUI572ChSsLno858uZ'
    '1rLnd+xKI6Ic7mWwALUCIQC3U58UEayMEekPhZKL28VM9Sx18BFguUiklwovcp9e'
    'twIgFqOr0DRVXm0jfke5oXmVkHiVBj58f8NzdUlsEIn4Se0CICZTaA1lCIKb9/JT'
    'xWhRwLSvCOV7E9b5xVMLdIio2OKPAiBqWSbsCQ3pXeBlPpfkbNNLeOt4CQYR7pJ9'
    'P792/e675A==\n'
    '-----END PRIVATE KEY-----')

public_key = (
    '-----BEGIN PUBLIC KEY-----\n'
    'MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAIkU0CeIPBnCp0UDM7RFhNjcVNhyXq4z'
    'JSIW2lX87SaTFme9CbwdbBvCc1THOZoGjxDkGwQB8c+RCvXznVt992MCAwEAAQ==\n'
    '-----END PUBLIC KEY-----')

jwks = {
    'keys': [{
        'alg': 'RS256',
        'kty': 'RSA',
        'use': 'sig',
        'n': 'iRTQJ4g8GcKnRQMztEWE2NxU2HJerjMlIhbaVfztJpMWZ70JvB1sG8' \
             'JzVMc5mgaPEOQbBAHxz5EK9fOdW333Yw',
        'e': 'AQAB',
        'kid': 'LeE4htANOADB4/QY2qD45+oukIY=',
        'x5c': public_key,
    }]
}

headers = {'kid': 'LeE4htANOADB4/QY2qD45+oukIY='}
payload = {
    'aud': 'casting-agency-api',
    'iss': 'https://jnsp-casting-agency.us.auth0.com/',
    'permissions': []
}


def get_test_token(permissions):
    payload['permissions'] = permissions
    return jwt.encode(payload, private_key, algorithm='RS256', headers=headers)
