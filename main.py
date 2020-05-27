# Program to download playlists of livecam video every T seconds.
# Author: Nathan Allen
# Date: 5/21/2020
import requests
import time
import m3u8
import datetime
from os import getcwd, listdir, chdir, mkdir, remove
from os.path import isfile, join
from moviepy.editor import VideoFileClip, concatenate_videoclips
import numpy as np

# URL set to VA beach boardwalk cam.
URL = "https://www.vbbound.com/live-webcam-of-virginia-beach-boardwalk"

# .m3u8 URL is obtained by playing a live stream in chrome, then open Developer Tools -> Network -> record network log and find
# the most recent chunklist_somenumber.m3u8 request, copy the Request URL, paste it here.
m3u8_URL = "https://58bdb48e25cf1.streamlock.net:19350/live/vcva002.stream/chunklist_w201002825.m3u8"

# Headers sent with the request to appear as a browser.
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
    return delay_secs, max_sets

# Gets the playlist of .ts videos from given m3u8 URL
def Get_ts_Playlist(m3u8_URL):
    m3u8_obj = m3u8.load(m3u8_URL)
    playlist=[el['uri'] for el in m3u8_obj.data['segments']]
    return playlist

# downloads the videos and saves them in a .avi format
def download_video(url, filename, path, headers):
    r1 = requests.get(url, stream=True, headers=headers)
    num=0
    if(r1.status_code == 200):
        chdir(path)
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

def ConcatenateClips(directories):
    for folder in directories.keys():
        # cd into each folder containing the short clips
        chdir(folder)
        # make objects from the clips
        clips = [VideoFileClip(filename) for filename in directories[folder]]
        
        # timestamp
        t = clips[1].filename[9:26]
        ffname = "beachcam full {}.mp4".format(t)

        # concatenate videos
        print("Merging clips from {}".format(t))
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(ffname, codec='libx264', audio=False) #codecs: 'rawvideo' (.avi very large file) or 'libx264' (.mp4) ~5Mb
        final_clip.close()
        # close and delete small clips
        [clip.close() for clip in clips]
        [remove(file) for file in directories[folder]]
        #for filename in directories[folder]:
        #    remove(filename)

        # make dir for img sequences and save frames as .jpg's 
        jpg_folder = "jpg sequence"
        mkdir(jpg_folder)
        
        # new video object
        final_clip = VideoFileClip(ffname)   
        dur = final_clip.duration
        print(dur)
        
        # capture a jpg for each second of the final clip.
        i = 0
        while i < dur:
            final_clip.save_frame("{0}/frame{1}.jpeg".format(jpg_folder, i), i, withmask=True)
            i += 1

        final_clip.close()
        


def main():
    # may need to open either selenium or a browser to the livecam url here, click to play livestream, and capture the requests
    # it sends. 
    delay, MAX_SETS = GetParams(URL)
    path = getcwd()
    total_vid_sets = 0
    directories = {}

    while(total_vid_sets < MAX_SETS):
        # Function creates a list of .ts video URLs that can be downloaded with requests.
        playlist = Get_ts_Playlist(m3u8_URL)
        
        # create a new folder for each set downloaded
        timestamp = datetime.datetime.now().strftime("2020-%m-%d %H%M%S")
        curr_path = path + "\\beachcam " + timestamp
        mkdir(curr_path)

        # new list of filenames for clips on each iteration
        clip_filenames = []
        vid_count= 0 # number each video
        # loop through each download url in the playlist.
        for vid_url in playlist: 
            download_url = "https://58bdb48e25cf1.streamlock.net:19350/live/vcva002.stream/" + vid_url
            fname = "beachcam " + timestamp + "clip#{}.avi".format(vid_count) 
            clip_filenames.append(fname)
            # download each video with requests library
            download_video(download_url, fname, curr_path, HEADERS)
            vid_count += 1
        
        # add folder path and filenames to dict:  {foldername : [filename, filename, filename...]}
        directories.update({curr_path : clip_filenames})
        
        total_vid_sets += 1
    
        # Sleep for user-defined hours/secs if it has not captured all the sets speci
        if total_vid_sets < MAX_SETS:
            print("Sleeping for {} hours.".format(delay/3600))
            time.sleep(delay)
  
    # Join the clips together in one video and create a jpg sequence.
    ConcatenateClips(directories)   


if __name__ == "__main__":
    main()
    