import os, sys, requests, json, re
from bs4 import BeautifulSoup

# redirects things going to stdout to filename
sys.stdout = open('stdout.txt', 'w')

# take command line args, url then directory name, respectively
url = sys.argv[1]
download_dir = sys.argv[2]
# if dir DNE, make dir, else leave as is (doesn't remake directory!!!)
os.makedirs(download_dir, exist_ok=True)  # succeeds even if directory exists.

# gets url webpage content
result = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"})

# src is result content, soup is parsed src object
src = result.content
soup = BeautifulSoup(src, 'html.parser')

# script then finds script tag containing string 'TralbumData', which
# is an array of JSON that contains data, including links to mp3s
script = soup.find('script', text=re.compile('TralbumData'))
# data is everything within var TralbumData
data = re.search(r"var TralbumData =(.+?);\n", script.text, re.S).group(0)
# apparently contents within trackinfo is randomized/unordered, so to
# get this nested array, must first substring to trackinfo then 
# substring to nested array containing album data
data = data[data.index("trackinfo"):data.index("]")] + "]"
data = data[data.index("["):]

# for debugging, print data
print(data, "\n")

# if data exists, then parse data into Python-readable dict
# otherwise return error
if data:
    json_data = json.loads(data)
else:
    print("Error: no such data oof")

# for debugging, print json_data to see if captured correctly
print(type(json_data))
print(json_data, "\n")
# url of the first track in album
print(json_data[0]["file"]["mp3-128"])

print('Beginning file download with requests\n')

# iterate through array of dicts to download each mp3
for mp3 in json_data:
    mp3_url = mp3["file"]["mp3-128"]
    r = requests.get(mp3_url, "\n")
    print(r.status_code)
    mp3_title = download_dir + "/" + mp3["title"] + ".mp3"
#     procedure to download mp3 in target folder
    with open(mp3_title, 'wb') as f:
        f.write(r.content)

print("Task finished")
