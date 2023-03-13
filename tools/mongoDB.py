def password_check(collection, username, password):
    result = collection.find_one({
        '$and': [
            {'username': username},
            {'password': password}
        ]
    })
    print('password_check succeeded')
    return result


def usertoken_check(collection, username, token_user):
    result = collection.find_one({
        '$and': [
            {'username': username},
            {'token_user': token_user}
        ]
    })
    return result


def token_update(collection, username, token_fhir, token_user):
    collection.update_one(
        {'username': username},
        {'$set': {
            'token_fhir': token_fhir,
            'token_user': token_user
        }
        }, upsert=True)
    print('token_update')


def getDBvalue(collection, username, value_name):
    result = collection.find_one({'username': username}).get(value_name)
    return result
