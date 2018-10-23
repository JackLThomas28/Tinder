import nltk
import requests
import FB_Auth_Token
import MyCredentials as credentials
import json
from pprint import pprint
import time

HOST_URL = 'https://api.gotinder.com/'
HEADERS = {
    'Origin': 'https://tinder.com',
    'app-version': '1020317',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept': 'application/json',
    'platform': 'web',
    'DNT': '1',
    'x-supported-image-formats': 'webp,jpeg',
    'Referer': 'https://tinder.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9'
}
STATUS_CODE = 0
JSON = 1
OK_200 = 200
TOO_MANY_REQUESTS_429 = 429


def main():
    this_session = requests.session()

    login_response = login(this_session)
    if login_response[STATUS_CODE] is not OK_200:
        print('error logging in:', login_response[STATUS_CODE])
    else:
        HEADERS.update({"X-Auth-Token": login_response[JSON]['token']})

    rec_response = get_recs_v2(this_session)
    if rec_response[STATUS_CODE] is not OK_200:
        print('error getting recommendations:', rec_response[STATUS_CODE])
    else:
        oldProfiles = loadBios()
        newProfiles = collectProfileInfo(rec_response[JSON])
        latest_response = likeProfiles(newProfiles, this_session)
        oldProfiles += newProfiles
        while True:
            while latest_response[JSON]['likes_remaining'] > 0 or latest_response is None:
                rec_response = get_recs_v2(this_session)
                newProfiles = collectProfileInfo(rec_response[JSON])
                latest_response = likeProfiles(newProfiles, this_session)
                oldProfiles += newProfiles
            ### Sleep for 12 hours; When more likes are available again
            saveBios(oldProfiles)
            print('sleeping...')
            time.sleep(60*60*12)


def collectProfileInfo(response):
    data = []
    for result in response['data']['results']:
        user = {}
        user['id'] = result['user']['_id']
        user['bio'] = result['user']['bio']
        user['birth_date'] = result['user']['birth_date']
        user['name'] = result['user']['name']
        user['gender'] = result['user']['gender']
        user['jobs'] = result['user']['jobs']
        user['schools'] = result['user']['schools']
        user['common_interests'] = result['facebook']['common_interests']
        user['distance_mi'] = result['distance_mi']
        data.append(user)
    return data


def passOnProfiles(profiles, session):
    for profile in profiles:
        dislike(session, profile['id'])


def likeProfiles(profiles, session):
    last_response = None
    for profile in profiles:
        response = like(session, profile['id'])
        if response[STATUS_CODE] is TOO_MANY_REQUESTS_429:
            time.sleep(60)
        if response[STATUS_CODE] is not OK_200 and response[STATUS_CODE] is not TOO_MANY_REQUESTS_429:
            pprint(response[JSON])
            return response
        if response[JSON]['likes_remaining'] == 0:
            return response
        last_response = response
    return last_response


def loadBios():
    data = None
    with open('GirlsTinderProfiles.json', 'r') as infile:
        data = json.load(infile)
    return data


def saveBios(data):
    with open('GirlsTinderProfiles.json', 'w') as outfile:
        json.dump(data, outfile)


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


main()
