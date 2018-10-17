import json
from bs4 import BeautifulSoup
import lxml.html
import nltk
import requests
import FB_Auth_Token

HOST_URL = 'https://api.gotinder.com/'
HEADERS = {
    'app_version': '6.9.4',
    'platform': 'ios',
    "content-type": "application/json",
    "User-agent": "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)",
    "Accept": "application/json"
}
STATUS_CODE = 0
JSON = 1
OK_200 = 200


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
        print(rec_response[JSON])
        for result in rec_response[JSON]['data']['results']:
            print(result['user']['_id'])


def login(session):
    fb_access_token = FB_Auth_Token.get_fb_access_token('JackAttack466@gmail.com', 'Jt1qtepwC56831012')
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
    response = session.get(HOST_URL + 'like/' + profile_id, headers=HEADERS)
    return response.status_code, response.json()


def dislike(session, profile_id):
    response = session.get(HOST_URL + 'pass/' + profile_id, headers=HEADERS)
    return response.status_code, response.json()


main()
