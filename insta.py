import requests
import json
from .instapi.client import client
from .instapi import bind
import sys
import argparse
import wget
import urllib.request
import os
import base64
import requests


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

# data = extractIG('ali_gfx24', 'Siktir49614961', target_username)
# print(data)