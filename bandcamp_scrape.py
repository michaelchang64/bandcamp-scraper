import os, sys, requests, json, re
from bs4 import BeautifulSoup

# redirects things going to stdout to filename
sys.stdout = open('stdout.txt', 'w')
url = sys.argv[1]
download_dir = sys.argv[2]

os.makedirs(download_dir, exist_ok=True)  # succeeds even if directory exists.

result = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"})

src = result.content
soup = BeautifulSoup(src, 'html.parser')
script = soup.find('script', text=re.compile('TralbumData'))
data = re.search(r"var TralbumData =(.+?);\n", script.text, re.S).group(0)

data = data[data.index("trackinfo"):data.index("]")] + "]"
data = data[data.index("["):]
# data = data.replace("trackinfo", "\"trackinfo\"")

print(data, "\n")

if data:
#     print(data)
#     data = json.dumps(data)
    json_data = json.loads(data)
else:
    print("Error: no such data oof")

# print(type(json_data))
print(json_data, "\n")
# print(json_data[0]["file"]["mp3-128"])

print('Beginning file download with requests\n')

for mp3 in json_data:
    mp3_url = mp3["file"]["mp3-128"]
    r = requests.get(mp3_url, "\n")
    print(r.status_code)
    mp3_title = download_dir + "/" + mp3["title"] + ".mp3"

    with open(mp3_title, 'wb') as f:
        f.write(r.content)

print("Task finished")
