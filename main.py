# Program to download playlists of livecam video every T seconds.
# Author: Nathan Allen
# Date: 5/21/2020
import os
import requests
import time
import m3u8
import datetime

# URL set to VA beach boardwalk cam.
URL = "https://www.vbbound.com/live-webcam-of-virginia-beach-boardwalk"

# .m3u8 URL is obtained by playing livestream in chrome -> Developer Tools -> Network -> record network log -> then look
# for the most recent chunklist_somenumber.m3u8 request and copy the Request URL, paste it here.
m3u8_URL = "https://58bdb48e25cf1.streamlock.net:19350/live/vcva002.stream/chunklist_w201002825.m3u8"

# Headers sent with the request to look appear as a browser.
HEADERS = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Accept": "*/*",
    "Origin": "https://www.vbbound.com",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors", 
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://www.vbbound.com/live-webcam-of-virginia-beach-boardwalk",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9"}

# Get delay time and max video sets to download.
def GetParams(URL):
    print("Open chrome and navigate to:%s ", URL)
    hourly_freq = int(input("Enter hourly frequency (1=dowload a video set every hour): "))
    delay_secs = hourly_freq * 3600
    max_sets = int(input("Enter the maximum number of video sets to download (i.e. 10=download up to 10 sets of videos every):"))
    # add opening to the webpage functionality: webbrowser.open(URL, new=1, autoraise=True)

    return delay_secs, max_sets

# Gets the playlist of .ts videos from given m3u8 URL
def get_ts_playlists(m3u8_URL):
    m3u8_obj = m3u8.load(m3u8_URL)
    playlist=[el['uri'] for el in m3u8_obj.data['segments']]
    return playlist

# downloads the videos and saves them in a .avi format
def download_video(url, filename, path, headers):
    r1 = requests.get(url, stream=True, headers=headers)
    num=0
    if(r1.status_code == 200):
        os.chdir(path)
        with open(filename,'wb') as f:
            print ("Downloading video...")
            for chunk in r1.iter_content(chunk_size=1024):
                num += 1
                f.write(chunk)
                if num>5000:
                    print('end')
                    f.close()
                    break
    else:
        print("Received unexpected status code {}".format(r1.status_code))

def main():
    # may need to open either selenium or a browser to the livecam url here, click to play livestream, and capture the requests
    # it sends. 
    delay, MAX_SETS = GetParams(URL)
    path =  os.getcwd()
    vid_set_count = 0

    while(vid_set_count < MAX_SETS):
        # Function creates a list of .ts video URLs that can be downloaded with requests.
        playlist = get_ts_playlists(m3u8_URL)
        
        # create a new folder for each set downloaded
        curr_path = path + "\\beachcam " + datetime.datetime.now().strftime("2020-%m-%d %H%M%S")
        os.mkdir(curr_path)
        
        # loop through each download url in the playlist.
        for vid_url in playlist:
            vid_url = "https://58bdb48e25cf1.streamlock.net:19350/live/vcva002.stream/" + vid_url
            fname = "beachcam " + datetime.datetime.now().strftime("2020-%m-%d %H%M%S") + ".avi" 
            # download each video with requests library
            download_video(vid_url, fname, curr_path, HEADERS)
        vid_set_count += 1 

        # Sleep for user-defined hours/secs
        print("Sleeping for {} hours.".format(delay/3600))
        time.sleep(delay)   

if __name__ == "__main__":
    main()



