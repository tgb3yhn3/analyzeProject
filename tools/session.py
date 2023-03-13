def getsession(session, session_id):
    if session_id in session:
        result = session[session_id]
        print('get session[' + session_id + '] succeeded')
    else:
        result = None
        print('get session[' + session_id + '] unsucceeded')

    return result
