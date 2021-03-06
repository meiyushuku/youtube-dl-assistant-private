import os
import re
import json

import common

import requests # pip install requests2
import gspread # pip install gspread
from oauth2client.service_account import ServiceAccountCredentials # pip install oauth2client

def _insertgs_init(config, confidentials):
    global USER, DATABASE_API_URL, sheet1, sheet2
    if "user" in str(config):
        if "sheetKeyFile" in str(confidentials):
            if "sheetId" in str(confidentials):
                if confidentials["insertGs"]["sheetKeyFile"] != "":
                    if confidentials["insertGs"]["sheetId"] != "":
                        USER = config["general"]["user"]
                        SHEET_KEY_FILE = confidentials["insertGs"]["sheetKeyFile"]
                        SHEET_ID = confidentials["insertGs"]["sheetId"]
                        SCOPE = "https://spreadsheets.google.com/feeds"
                        DATABASE_API_URL = confidentials["insertGs"]["databeseApiUrl"]
                        if os.path.isfile(SHEET_KEY_FILE):
                            cert = ServiceAccountCredentials.from_json_keyfile_name(SHEET_KEY_FILE, SCOPE)
                            client = gspread.authorize(cert)
                            sheet1 = client.open_by_key(SHEET_ID).get_worksheet(0) # channelInfo
                            sheet2 = client.open_by_key(SHEET_ID).get_worksheet(1) # videoInfo
                            return True
                        else:
                            print('"%s" not found.' % os.path.split(SHEET_KEY_FILE)[1])
                            input()
                    else:
                        print("Sheet ID must be supplied.")
                        input()
                else:
                    print("Sheet key file must be supplied.")
                    input()
            else:
                print('Object "sheetId" not found in "confidentials.json."')
                input()
        else:
            print('Object "sheetKeyFile" not found in "confidentials.json."')
            input()
    else:
        print('Object "user" not found in "config.json."')
        input()

def video_exists(video_id):
    video_info_url = DATABASE_API_URL + "?method=getVideoInfoByVideoId&site=YT&videoId=" + video_id
    response = requests.get(video_info_url)
    if json.loads(response.text):
        video_exists = 1 # 1
    else:
        video_exists = 0 # 0
    return video_exists

'''
def video_exists(video_id):
    try:
        if sheet2.find(video_id):
            video_exists = 1
    except:
        video_exists = 0
    return video_exists

def channel_exists(channel_id):
    try:
        if sheet1.find(channel_id):
            channel_exists = 1
    except:
        channel_exists = 0
    return channel_exists
'''

def insert_video_info(video_info_list, file_name): # Catch video_info_list from fileproc.
    insert_list = list()
    insert_list.append("YT") # site
    insert_list.append(video_info_list[1]) # channelId
    insert_list.append(video_info_list[2]) # publishedAt
    insert_list.append(video_info_list[3]) # videoId
    insert_list.append(video_info_list[4]) # title
    insert_list.append(json.dumps(video_info_list[5], ensure_ascii = False)) # description
    insert_list.append("") # customDescription
    insert_list.append(video_info_list[6]) # duration
    insert_list.append(USER) # user
    insert_list.append(common.now(2)) # lastUpdate
    insert_list.append(re.sub("[.]", "", os.path.splitext(file_name)[1])) # extension
    sheet2.append_row(insert_list, table_range = "A:A")

#def insert_channel():