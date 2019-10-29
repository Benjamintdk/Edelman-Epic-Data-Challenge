import json
import os
import time
from datetime import datetime
import csv
import urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

with open("articles.json", 'r') as f:
    datastore = json.load(f)
with open("articles_revamped.json", 'r') as f:
    publish_key = json.load(f)
# contents, fb_data (total_engagement_count, likes, comments, share)
# has_video, headline, keywords
# image_link, tw_data, velocity
# max_velocity, sentiment, publication_timestamp, source
# iffy authors, topics, li_data
# $$$ contents, headline, keywords, sentiment
# $$$
# fb_data
length = len(datastore)

def tfidBruteForce(item):
    correspond = []
    cv = CountVectorizer()
    tfidf_transformer = TfidfTransformer(smooth_idf = True, use_idf = True)
    for i in range(0, len(data_key['Keywords'])):
        # Bind the key with data
        key_data_pair = [data_key['Keywords'][i], item]

        # Initialise count vectoriser
        word_count_vector = cv.fit_transform(key_data_pair)

        # Perform TFIDF transform
        tfidf_transformer.fit(word_count_vector)
        df_idf = pd.DataFrame(tfidf_transformer.idf_, index = cv.get_feature_names(), columns=["idf_weights"])
        min_local  = min(df_idf['idf_weights'])
        if min_local == minSimilarity:
            correspond.append(i)
            break
    return correspond

def checkTopicsHasUnited():
    talkingVar = 0
    check = 0
    for i in range(1, length):
        for j in range(0, len(datastore[i]['topics'])):
            if datastore[i]['topics'][j]['id'] == 443:
                check += 1
                if "united airlines" in datastore[i]['contents'].lower():
                    talkingVar += 1
                else:
                    print(datastore[i]['contents'] + "\n" + "-------------------------")

def checkContentGotUnited():
    unitedCount = 0
    for i in range(0, length):
        loweredContents = datastore[i]['contents'].lower()
        if "united airlines" in loweredContents:
            datastore[i]['contents'] = 1
            unitedCount += 1
        else:
            datastore[i]['contents'] = 0
    print(unitedCount / length)

def printAuthor():
    for i in range(0, length):
        loweredContents = datastore[i]['link']
        print(loweredContents)

def checkHeadlineGotUnited():
    for i in range(0, length):
        if "united" in datastore[i]['headline'].lower():
            datastore[i]['headline'] = 1
        else:
            datastore[i]['headline'] = 0


def secondsToText(secs):
    days = secs//86400
    hours = (secs - days*86400)//3600
    minutes = (secs - days*86400 - hours*3600)//60
    seconds = secs - days*86400 - hours*3600 - minutes*60
    result = ("{} days, ".format(days) if days else "") + \
    ("{} hours, ".format(hours) if hours else "") + \
    ("{} minutes, ".format(minutes) if minutes else "") + \
    ("{} seconds, ".format(seconds) if seconds else "")
    return result

def secondsToDays(secs):
    days = secs//86400
    return days

def calculateTimeDifference(i):
    epochTime = datastore[i]['publication_timestamp'] / 1000
    timeVar = time.time() - epochTime
    return timeVar

def processImage():
    count = 0
    for i in range(0, length):
        try:
            image_url = datastore[i]['entities']['media'][0]['media_url']
            urllib.request.urlretrieve(image_url, '0000000' + str(i) + '.jpg')
            print("\n", "-----------------------")
            count += 1
        except Exception:
            continue
    print(count)

def hasImage():
    has = []
    for i in range(0, length):
        try:
            image_url = datastore[i]['image_link']
            request = urllib.urlopen(image_url, timeout=500)
            with open("images/" + str(i) + ".jpg", 'wb') as f:
                try:
                    f.write(request.read())
                except:
                    print("error")
            print(image_url, "\n", "-----------------------")
            has.append(1)
        except Exception:
            has.append(0)
            continue
    return has

data_temp = []
for i in range(0, len(datastore)):
    data_temp.append([datastore[i]['fb_data']['total_engagement_count'],
                      datastore[i]['max_velocity'],
                      datastore[i]['velocity'],
                      secondsToDays(calculateTimeDifference(i))])

checkContentGotUnited()
checkHeadlineGotUnited()
printAuthor()

scaler2 = StandardScaler()
transformed = scaler2.fit_transform(data_temp)
hasImageArray = hasImage()

data_out = [['engagement', 'max_velocity', 'velocity', 'time_difference', 'likes', 'sentiment', 'has_image']]
for i in range(0, length):
    if datastore[i]['contents'] == 1 and datastore[i]['headline'] == 1:
        data_out.append([transformed[i][0], transformed[i][1],
                         transformed[i][2], transformed[i][3],
                         datastore[i]['fb_data']['likes'], datastore[i]['sentiment'],
                         hasImageArray[i]])


myFile = open('out.csv', 'w')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(data_out)

# with open('out.csv', mode='w') as file:
#     writer = csv.writer(file, quoting=csv.QUOTE_ALL)
#     writer.writerow(data_out)
# followers_count, likes_count, max_retweet_value
# social_referrals
# iffy statuses_count, twitter_handle
# Segments (Criteria)
# 1) Catalysts (influence)
# 2) Originators (influence)
# 3) Young (age)
# 4) Old (age)
# 5) Middle Aged (age)
# 6) News (content) -> articles; First-hand reporting;
# 7) Politics (content)
# 8) Airline Reviewers (content)
# 9) Travel Vloggers (content)
# 10) Users that mention United Airlines
# Criteria - Frequency of social media usage
#          - Timestamp
# H
"""
TWEET = {'created_at': 'Thu Oct 18 13:15:17 +0000 2018', 'id': 1052910994303926274, 'id_str': '1052910994303926274', 'text': 'United Airlines: Still no plan to allow free carry-on bag for basic economy tickets https://t.co/POXu9njjNW https://t.co/VSH4m6BT5j', 'truncated': False,
 'entities': {'hashtags': [], 'symbols': [], 'user_mentions': [],
 'urls': [{'url': 'https://t.co/POXu9njjNW', 'expanded_url': 'https://on.11alive.com/2OzDiB5', 'display_url': 'on.11alive.com/2OzDiB5', 'indices': [84, 107]}],
 'media': [{'id': 1052910993045708802, 'id_str': '1052910993045708802', 'indices': [108, 131], 'media_url': 'http://pbs.twimg.com/media/Dpyw-DiX4AI-Tz3.jpg', 'media_url_https': 'https://pbs.twimg.com/media/Dpyw-DiX4AI-Tz3.jpg', 'url': 'https://t.co/VSH4m6BT5j', 'display_url': 'pic.twitter.com/VSH4m6BT5j', 'expanded_url': 'https://twitter.com/11AliveNews/status/1052910994303926274/photo/1', 'type': 'photo', 'sizes': {'large': {'w': 1024, 'h': 576, 'resize': 'fit'}, 'thumb': {'w': 150, 'h': 150, 'resize': 'crop'}, 'medium': {'w': 1024, 'h': 576, 'resize': 'fit'}, 'small': {'w': 680, 'h': 383, 'resize': 'fit'}}}]}, 'extended_entities': {'media': [{'id': 1052910993045708802, 'id_str': '1052910993045708802', 'indices': [108, 131], 'media_url': 'http://pbs.twimg.com/media/Dpyw-DiX4AI-Tz3.jpg', 'media_url_https': 'https://pbs.twimg.com/media/Dpyw-DiX4AI-Tz3.jpg', 'url': 'https://t.co/VSH4m6BT5j', 'display_url': 'pic.twitter.com/VSH4m6BT5j', 'expanded_url': 'https://twitter.com/11AliveNews/status/1052910994303926274/photo/1', 'type': 'photo', 'sizes': {'large': {'w': 1024, 'h': 576, 'resize': 'fit'}, 'thumb': {'w': 150, 'h': 150, 'resize': 'crop'}, 'medium': {'w': 1024, 'h': 576, 'resize': 'fit'}, 'small': {'w': 680, 'h': 383, 'resize': 'fit'}}}]}, 'source': '<a href="https://trueanthem.com/" rel="nofollow">True Anthem</a>',
 'in_reply_to_status_id': None, 'in_reply_to_status_id_str': None, 'in_reply_to_user_id': None, 'in_reply_to_user_id_str': None, 'in_reply_to_screen_name': None,
 'user': {'id': 14268564, 'id_str': '14268564', 'name': '11Alive News', 'screen_name': '11AliveNews', 'location': 'Atlanta', 'description': "Welcome to 11Alive: Where Atlanta Speaks. Here, you'll find the top stories and news from 11Alive in Atlanta.", 'url': 'https://t.co/HvuBQjyHot', 'entities': {'url': {'urls': [{'url': 'https://t.co/HvuBQjyHot', 'expanded_url': 'http://www.11Alive.com/', 'display_url': '11Alive.com', 'indices': [0, 23]}]}, 'description': {'urls': []}}, 'protected': False, 'followers_count': 392568, 'friends_count': 2761, 'listed_count': 2258, 'created_at': 'Mon Mar 31 19:05:00 +0000 2008', 'favourites_count': 4187, 'utc_offset': None, 'time_zone': None, 'geo_enabled': True, 'verified': True, 'statuses_count': 386369, 'lang': None, 'contributors_enabled': False, 'is_translator': False, 'is_translation_enabled': False, 'profile_background_color': '131516', 'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme14/bg.gif', 'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme14/bg.gif', 'profile_background_tile': True, 'profile_image_url': 'http://pbs.twimg.com/profile_images/1088178367277481985/k_XYX1i8_normal.jpg', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1088178367277481985/k_XYX1i8_normal.jpg', 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/14268564/1554384824', 'profile_link_color': '009999', 'profile_sidebar_border_color': 'EEEEEE', 'profile_sidebar_fill_color': 'EFEFEF', 'profile_text_color': '333333', 'profile_use_background_image': True, 'has_extended_profile': False, 'default_profile': False, 'default_profile_image': False, 'following': False, 'follow_request_sent': False, 'notifications': False, 'translator_type': 'none'}, 'geo': None, 'coordinates': None, 'place': None, 'contributors': None, 'is_quote_status': False, 'retweet_count': 1, 'favorite_count': 2, 'favorited': False, 'retweeted': False, 'possibly_sensitive': False, 'lang': 'en'}

 ARTICLE = {'article_id': '757aab00-d16e-11e6-ab89-c11942898bd6', 'authors': ['Tom Boggioni'], 'contents': 'A man who went on a racist and gay-bashing rant on a United Airlines flight was arrested after he told a flight attendant that it would be “cool” if he caused the plane to be diverted. According to the New Zealand Herald, the San Francisco-bound flight that originated in Sydney,...\n     ', 'excerpt': 'A man who went on a racist and gay-bashing rant on a United Airlines flight was arrested after he told a flight attendant that it would be “cool” if he caused the plane to be diverted. According to the New Zealand Herald, the San Francisco-bound flight that originated in Sydney, Australi...', '
 fb_data': {'total_engagement_count': 6059, 'likes': 0, 'comments': 0, 'shares': 0},
 'has_video': True, 'headline': '‘You want to hear me f*cking yelling?’: US-bound flight diverted after passenger goes on racist rant',
 'image_link': 'http://www.rawstory.com/wp-content/uploads/2017/01/united_passenger_screengrab-800x430.jpg',
 'keywords': '', 'li_data': {'li_count': 0}, 'link': 'http://www.rawstory.com/2017/01/you-want-to-hear-me-fcking-yelling-us-bound-flight-diverted-after-passenger-goes-on-racist-rant/',
 'max_velocity': 54.54139583470914, 'pi_data': {'pi_count': 7}, 'publication_timestamp': 1483418302896, 'sentiment': -1.0,
 'source': {'publisher': 'rawstory.com', 'link': 'http://rawstory.com', 'country': 'United States', 'country_code': 'us'},
 'topics': [{'id': 19, 'name': 'Opinion'}, {'id': 23, 'name': 'Left'}], 'tw_data': {'tw_count': 150}, 'velocity': 0.17479487659384604}
"""
