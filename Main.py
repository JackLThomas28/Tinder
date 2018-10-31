import requests
import Constants
import json
from pprint import pprint
import time
import Tinder as tinder


def login(session):
    response = tinder.login(session)
    if response[Constants.STATUS_CODE] is not 200:
        print('Authentication error:', response[Constants.STATUS_CODE])
    else:
        Constants.HEADERS.update({"X-Auth-Token": response[Constants.JSON]['token']})


def get_recommendations(session):
    response = tinder.get_recs_v2(session)
    if response[Constants.STATUS_CODE] is not 200:
        print('Error retreiving recommendations:', response[Constants.STATUS_CODE])
        return Constants.ERROR
    else:
        return response[Constants.JSON]


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
        if response[Constants.STATUS_CODE] is not 200:
            print('Error liking the profiles:', response[Constants.STATUS_CODE])
            return Constants.ERROR
        time.sleep(60)
    return response[Constants.JSON]['likes_remaining']


def main():
    this_session = requests.session()

    login(this_session)

    recommendations = get_recommendations(this_session)
    if recommendations is Constants.ERROR:
        return Constants.ERROR

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
            if likes_remaining is Constants.ERROR:
                return Constants.ERROR
            
            recommendations = get_recommendations(this_session)
            if recommendations is Constants.ERROR:
                return Constants.ERROR
            
            new_profiles = collect_profile_info(recommendations)
            old_profiles += new_profiles
            save_bios(old_profiles)

            print("Sleeping in between likes")
            time.sleep(10)
        day += 1
        ### Sleep for 12 hours; When more likes are available again
        print('No more likes. Sleeping...')
        time.sleep(60*60*12)
    print('Program ended')


def pass_on_profiles(profiles, session):
    for profile in profiles:
        tinder.dislike(session, profile['id'])


main()
