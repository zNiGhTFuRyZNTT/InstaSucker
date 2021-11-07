import requests
import json
from instapi.client import client
from instapi import bind
import sys
import argparse
import wget
import urllib.request
import os
import base64
import requests
import random

def get_as_base64(url):

    return base64.b64encode(requests.get(url).content)
# <- ----- Colors  ----- ->
def extractIG(username, password, target_username):
    bind(username, password)

    cookies = ''
    for cookie in client.obj.cookie_jar:
        if cookie.name == 'csrftoken':
            csrf = cookie.value
        cookies += f'{cookie.name}={cookie.value}; '
    print(cookies)

    headers = {
        'Cookie': cookies,
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Instagram 76.0.0.15.395 Android (24/7.0; 640dpi; 1440x2560; samsung; SM-G930F; herolte; samsungexynos8890; en_US; 138226743)',
        'X-IG-Capabilities': '3brTvw==',
        'X-IG-Connection-Type': 'WIFI',
        'X-IG-Connection-Speed': '3555kbps',
        'X-IG-App-ID': '567067343352427',
        'X-IG-Bandwidth-Speed-KBPS': '-1.000',
        'X-IG-Bandwidth-TotalBytes-B': '0',
        'X-IG-Bandwidth-TotalTime-MS': '0',
        'X-FB-HTTP-Engine': 'Liger',
    }


    url = f"https://www.instagram.com/{target_username}/?__a=1"
    response = requests.request("GET", url, headers=headers)
    res = response.json()

    # <- ----- Data ----- ->
    uid = res['logging_page_id'].split('_')[1]
    # target_username = res['graphql']['user']['username']
    full_name = res['graphql']['user']['full_name']
    bio = res['graphql']['user']['biography']
    followers_count = res['graphql']['user']['edge_followed_by']
    followings_count = res['graphql']['user']['edge_follow']
    profile_pic_url = res['graphql']['user']['profile_pic_url_hd']
    profile_pic_b64 = get_as_base64(profile_pic_url)
    profile_pic_b64_S = profile_pic_b64.decode('utf8').replace("'", '"')

    allInfo = {
        'user': {
            'username' : '',
            'uid' : '',
            'bio' : '',
            'followings_count' : '',
            'followers_count' : '',
            'profile_pic_url' : '',
            'profile_pic_b64': '',
            'videos' : [],

            }
    }
    allInfo['user']['username'] = target_username
    allInfo['user']['uid'] = uid
    allInfo['user']['bio'] = bio
    allInfo['user']['followings_count'] = followings_count
    allInfo['user']['followers_count'] = followers_count
    allInfo['user']['profile_pic_url'] = profile_pic_url
    allInfo['user']['profile_pic_b64'] = profile_pic_b64_S

    edges = res['graphql']['user']['edge_owner_to_timeline_media']['edges']
    for i in range(len(edges)):
        #print(i)
        
        path =  res['graphql']['user']['edge_owner_to_timeline_media']['edges'][i]['node']
        if path['is_video']:
            video_description = path['edge_media_to_caption']['edges'][0]['node']['text']
            video_url = path['video_url']
            video_display = path['display_url']
            display_b64 = get_as_base64(video_display)
            display_b64 = display_b64.decode('utf8').replace("'", '"')

            # <-------------------------------->
            # allInfo['user']['videos']
            allInfo['user']['videos'].append(
                {
                    "video_description": video_description,
                    "video_url": video_url,
                    "video_display": display_b64
                })
            # allInfo['user']['videos'].append(content)
        
    data = json.dumps(allInfo)
    # print(data.user.videos.video1.video_display)
    return data

"""
to run this file directly uncomment the lines bellow:
"""

if __name__ == '__main__':
    class cc:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    # <- -----  End ----- ->

    # <- -----  Args ----- ->
    my_parser = argparse.ArgumentParser(description='List the content of a folder')
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-u', '--username', action='store', type=str, help="user's username")
    my_parser.add_argument('-p', '--password',action='store', type=str, help="'user's username")
    my_parser.add_argument('-t', '--target',action='store', type=str, help="Target's username")
    my_parser.add_argument('-o', '--output',action='store', type=str, help="file output path (MUST BE FOLDER)")
    args = my_parser.parse_args()
    # <- -----  End ----- ->

    # <- -----  Get Login Details if no Argument were given ----- ->
    if args.output is None:
        output_path = ''
    else:
        output_path = args.output

    if args.username is None or args.password is None or args.target is None:
        print(cc.HEADER + "[!]Invalid arguments detected" + cc.ENDC)
        print(cc.HEADER + "Enter Login details:\n" + cc.ENDC)
        username = input("username >> ")
        password = input("password >> ")
        target_username = input("target username >> ")
    else:
        username = args.username #sys.argv[1]
        password = args.password #sys.argv[2]
        target_username = args.target
    # <- -----  End ----- ->

    # <- -----  Login ----- ->
    print(cc.OKGREEN + '[>] Logging in...' + cc.ENDC)
    bind(username, password)
    # <- -----  End ----- ->
    
    data = extractIG(username, password, target_username) 
    rNum = random.randint(0, 100000)

    with open(f'output{rNum}.json', 'w') as f:
        f.write(data)

