import nltk
import requests
import FB_Auth_Token
import json
from pprint import pprint
import time
import Tinder as tinder

HOST_URL = 'https://api.gotinder.com/'
HEADERS = {
    'Origin': 'https://tinder.com',
    'app-version': '1020317',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) ' + 
        'AppleWebKit/537.36 (KHTML, like Gecko) ' + 
        'Chrome/69.0.3497.100 Safari/537.36',
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
ERROR = -1


def login(session):
    response = tinder.login(session)
    if response[STATUS_CODE] is not 200:
        print('Authentication error:', response[STATUS_CODE])
    else:
        HEADERS.update({"X-Auth-Token": response[JSON]['token']})


def get_recommendations(session):
    response = tinder.get_recs_v2(session)
    if response[STATUS_CODE] is not 200:
        print('Error retreiving recommendations:', response[STATUS_CODE])
        return ERROR
    else:
        return response[JSON]


def collect_profile_info(response):
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


def load_bios():
    data = None
    with open('GirlsTinderProfiles.json', 'r') as infile:
        data = json.load(infile)
    return data


def save_bios(data):
    with open('GirlsTinderProfiles.json', 'w') as outfile:
        json.dump(data, outfile)


def like_profiles(profiles, session):
    response = None
    for profile in profiles:
        response = tinder.like(session, profile['id'])
        if response[STATUS_CODE] is not 200:
            print('Error liking the profiles:', response[STATUS_CODE])
            return ERROR
        time.sleep(60)
    return response[JSON]['likes_remaining']


def main():
    this_session = requests.session()

    login(this_session)

    recommendations = get_recommendations(this_session)
    if recommendations is ERROR:
        return ERROR

    new_profiles = collect_profile_info(recommendations)
    ### Load the previously collected data to add to it
    old_profiles = load_bios()
    old_profiles += new_profiles
    save_bios(old_profiles)
        
    ### Run the program for 5 days
    day = 1
    while day < 6:
        likes_remaining = 100 
        while likes_remaining > 0:
            likes_remaining = like_profiles(new_profiles, this_session)
            if likes_remaining is ERROR:
                return ERROR
            
            recommendations = get_recommendations(this_session)
            if recommendations is ERROR:
                return ERROR
            
            new_profiles = collect_profile_info(recommendations)
            old_profiles += new_profiles
            save_bios(old_profiles)
        day += 1
        ### Sleep for 12 hours; When more likes are available again
        print('No more likes. Sleeping...')
        time.sleep(60*60*12)
    print('Program ended')


def pass_on_profiles(profiles, session):
    for profile in profiles:
        tinder.dislike(session, profile['id'])


main()
