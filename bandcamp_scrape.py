import os
import sys
import requests
import json
import re
from bs4 import BeautifulSoup

###################
### SYSTEM INIT ###
###################

# redirects things going to stdout to filename
sys.stdout = open('stdout.txt', 'w')

# take command line args, url then directory name, respectively
url = sys.argv[1] # first command line arg, after 'python'
download_dir = sys.argv[2] # second arg, download directory

# if dir DNE, make dir, else leave as is (doesn't remake directory!!!)
os.makedirs(download_dir, exist_ok=True)  # succeeds even if directory exists.

####################
### REQUEST STEP ###
####################

# spoof header to make requester seem more human
header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"}
# gets url webpage content
bandcamp_page = requests.get(url, headers=header)
bandcamp_page_src = bandcamp_page.content

###################
### SCRAPE STEP ###
###################

# bandcamp_page_src is result content, then parsed by soup
soup = BeautifulSoup(bandcamp_page_src, 'lxml')

# find script tag containing type 'application/ld+json', which
# is an array of JSON that contains data, including links to mp3s
json_script_obj = soup.find('script', {'type': 'application/ld+json'})

# load data from json obj
json_script_obj_src = json_script_obj.contents[0]
raw_json = json.loads(json_script_obj_src)

# find pertinent list with track data
track_data = raw_json['track']['itemListElement']

#####################
### DOWNLOAD STEP ###
#####################

print('Beginning file download with requests\n')

# get number of tracks to download
num_tracks = len(track_data)
i = 0

# iterate through array of dicts to download each mp3
for mp3 in track_data:
    # get pertinent metadata from each track in list
    mp3_title = mp3['item']['name']
    mp3_url = mp3['item']['additionalProperty'][2]['value']

    # get page with raw mp3
    print('Extracting mp3 from', mp3_title, 'at', mp3_url)
    mp3_page = requests.get(mp3_url, "\n")

    # increment track number by one
    i += 1

    # conditions to check if mp3_page is accessible
    if mp3_page.ok:
        # title each mp3 based on title
        title = download_dir + "/" + mp3_title + ".mp3"

        # download mp3 into target folder
        with open(title, 'wb') as f:
            f.write(mp3_page.content)

        print('Downloaded track', i, 'of', num_tracks, '\n')
    else:
        print('mp3 track', i, 'not accessible, error code', mp3_page.status_code)
        # print('mp3 track', 'not accessible, error code', mp3_page.status_code)

print("\nAll done!")
