import Constants
import MyCredentials as credentials
import FB_Auth_Token

def login(session):
    creds = credentials.getMyCredentials()
    fb_access_token = FB_Auth_Token.get_fb_access_token(creds[0], creds[1])
    fb_access_id = FB_Auth_Token.get_fb_id(fb_access_token)
    data = {'facebook_token': fb_access_token, 'facebook_id': fb_access_id}
    response = session.post(Constants.HOST_URL + 'auth', data=data)
    return response.status_code, response.json()


def get_profile(session):
    response = session.get(Constants.HOST_URL + 'profile', headers=Constants.HEADERS)
    return response.status_code, response.json()


def get_user_profile(session, profile_id):
    response = session.get(Constants.HOST_URL + 'user/' + profile_id, headers=Constants.HEADERS)
    return response.status_code, response.json()


def get_recommedations(session):
    response = session.get(Constants.HOST_URL + 'user/recs', headers=Constants.HEADERS)
    return response.status_code, response.json()


def get_recs_v2(session):
    response = session.get(Constants.HOST_URL + '/v2/recs/core?locale=en-US', headers=Constants.HEADERS)
    return response.status_code, response.json()


def like(session, profile_id):
    response = session.get(Constants.HOST_URL + 'like/' + profile_id + '?locale=en-US&s_number=628218027', headers=Constants.HEADERS)
    print(profile_id)
    return response.status_code, response.json()


def dislike(session, profile_id):
    response = session.get(Constants.HOST_URL + 'pass/' + profile_id + '?locale=en-US&s_number=628218027' , headers=Constants.HEADERS)
    return response.status_code, response.json()
