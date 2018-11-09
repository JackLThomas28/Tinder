import requests
import Constants
import json
from pprint import pprint
from Helpers import fileIO
import time
import Tinder

ProfilesFile = 'GirlsTinderProfiles.json'


def login(session):
    response = Tinder.login(session)
    if response[Constants.STATUS_CODE] is not 200:
        print('Authentication error:', response[Constants.STATUS_CODE])
    else:
        Constants.HEADERS.update({"X-Auth-Token": response[Constants.JSON]['token']})


def get_recommendations(session):
    response = Tinder.get_recs_v2(session)
    if response[Constants.STATUS_CODE] is not 200:
        print('Error retreiving recommendations:', response[Constants.STATUS_CODE])
        return Constants.ERROR
    else:
        return response[Constants.JSON]


def collect_profile_info(response):
    try:
        response['data']['results']
    except:
        print('The response did not contain any results:', response)
        return Constants.ERROR
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


def like_profiles(profiles, session):
    response = None
    for profile in profiles:
        response = Tinder.like(session, profile['id'])
        if response[Constants.STATUS_CODE] is not 200:
            print('Error liking profiles:', response[Constants.STATUS_CODE])
            return Constants.ERROR
        print('Sleeping between likes...')
        time.sleep(10)
    return response[Constants.JSON]['likes_remaining']


def refresh_auth_token(session):
    login(session)


def main():
    this_session = requests.session()
    login(this_session)

    recommendations = get_recommendations(this_session)
    if recommendations is Constants.ERROR:
        return Constants.ERROR

    new_profiles = collect_profile_info(recommendations)
    if new_profiles is Constants.ERROR:
        return Constants.ERROR
    ### Load the previously collected data to add to it
    old_profiles = fileIO.load_json_file(ProfilesFile)
    old_profiles += new_profiles
    fileIO.save_json_file(ProfilesFile, old_profiles)
        
    ### Run the program for 5 days
    day = 1
    while day < 6:
        if day % 2 == 0:
            refresh_auth_token(this_session)
        likes_remaining = 100

        while likes_remaining > 0:
            likes_remaining = like_profiles(new_profiles, this_session)
            if likes_remaining is Constants.ERROR:
                return Constants.ERROR
            
            recommendations = get_recommendations(this_session)
            if recommendations is Constants.ERROR:
                return Constants.ERROR
            
            new_profiles = collect_profile_info(recommendations)
            ### No one new is around. Wait 12 hours for new recommendations
            if new_profiles is Constants.ERROR:
                old_profiles += new_profiles
                fileIO.save_json_file(ProfilesFile, old_profiles)
                print('No one new is around')
                break

            old_profiles += new_profiles
            fileIO.save_json_file(ProfilesFile, old_profiles)
        ### Sleep for 12 hours; When more likes are available again
        print('No more likes. Day %d complete. Sleeping...' % day)
        day += 1
        time.sleep(60*60*12)
    print('Program ended')


def pass_on_profiles(profiles, session):
    for profile in profiles:
        Tinder.dislike(session, profile['id'])


main()
