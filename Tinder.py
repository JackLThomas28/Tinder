def login(session):
    creds = credentials.getMyCredentials()
    fb_access_token = FB_Auth_Token.get_fb_access_token(creds[0], creds[1])
    fb_access_id = FB_Auth_Token.get_fb_id(fb_access_token)
    data = {'facebook_token': fb_access_token, 'facebook_id': fb_access_id}
    response = session.post(HOST_URL + 'auth', data=data)
    return response.status_code, response.json()


def get_profile(session):
    response = session.get(HOST_URL + 'profile', headers=HEADERS)
    return response.status_code, response.json()


def get_user_profile(session, profile_id):
    response = session.get(HOST_URL + 'user/' + profile_id, headers=HEADERS)
    return response.status_code, response.json()


def get_recommedations(session):
    response = session.get(HOST_URL + 'user/recs', headers=HEADERS)
    return response.status_code, response.json()


def get_recs_v2(session):
    response = session.get(HOST_URL + '/v2/recs/core?locale=en-US', headers=HEADERS)
    return response.status_code, response.json()


def like(session, profile_id):
    response = session.get(HOST_URL + 'like/' + profile_id + '?locale=en-US&s_number=628218027', headers=HEADERS)
    print(profile_id)
    if response.status_code == 429:
        return response.status_code, None
    return response.status_code, response.json()


def dislike(session, profile_id):
    response = session.get(HOST_URL + 'pass/' + profile_id + '?locale=en-US&s_number=628218027' , headers=HEADERS)
    return response.status_code, response.json()
