Live Webcam Downloader

Author: Nathan Allen

Description: Used for the paper: Is it safer at the beach? Spatial and temporal analyses of beachgoer behaviors during the COVID-19 pandemic.Periodically downloads video from the livestream of 
             vbbound.com/live-webcam-of-virginia-beach-boardwalk
             Program will download sets of short videos from the livestream every t hours, storing them in labeled directories.

Requirements: 
Python 3
Libraries: m3u8, requests
                                                                           

Usage: open chrome or a web browser, navigate to https://www.vbbound.com/live-webcam-of-virginia-beach-boardwalk and play the stream.
       Run python script in the interpreter.
       It will prompt for the hourly delay to download the videos and a max number of videos. 
       (If delay = 1, 1 video set is downloaded per hour. If max number = 1, 1 set of videos are downloaded)

Bugs: The script does not automatically get the .m3u8 url from the xhr request. Without a fresh URL, it may return a 404 error when attempting to download.
To fix this, a new URL must be supplied in the script. In chrome, this is found by opening and playing the livestream, then going to -> Developer Tools -> Network -> record network log.
In the XHR tab, there will be a chunklist_wsomenumber.m3u8 request. Click on it and copy it's Request URL which will look something like: https://58bdb48e25cf1.streamlock.net:19350/live/vcva002.stream/chunklist_w88396777.m3u8
Set the m3u8_url variable (near the top of the code) equal to the new url.
