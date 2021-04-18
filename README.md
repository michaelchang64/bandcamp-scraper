# More Legit and Certainly Not Janky Bandcamp Web Scraper

This bad boy can download so many mp3's from Bandcamp!!!

## Disclaimer

Please don't arrest me or report me for piracy, I only did this for educational purposes.

Also, if you `insPecT thE ElEmenTS` carefully enough, you'll see that Bandcamp has a [lax policy](https://bandcamp.com/zendesk/help/audio_basics#steal).

Hope you enjoy this! DO SUPPORT GROWING ARTISTS BY BUYING THEIR MUSIC!!!!!!!

## Set-up
1. `git clone` this repo to a known directory on your local system
2. Create your virtual environment within repo (we'll call ours `venv`): `python -m venv venv`
3. Install all necessary dependencies: `pip install -r requirements.txt`
4. Now, you should be set up to run the scrape!
    * Make sure the first argument after `python bandcamp_scrape.py` is the bandcamp album url
    * You can specify a local file path and it will create a folder if it doesn't already exist
        * If you write to a folder that already exists, it will delete everything in it and overwrite, so beware!
    * See template and example below:
```
python bandcamp_scrape.py "artist_name.bandcamp.com/album/album_name" "./some_file_path"
```

## Example

```
python bandcamp_scrape.py "https://music.midwestcollective.us/album/odyssey" "./odyssey"
```