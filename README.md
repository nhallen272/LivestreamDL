Live Webcam Downloader
Author: Nathan Allen
        5/21/2020
Description: Periodically downloads video from the livestream of 
             vbbound.com/live-webcam-of-virginia-beach-boardwalk
             Program will download sets of short videos from the livestream every t hours, storing them in labeled directories.

Requirements: Python 3
              Libraries: m3u8, requests --must be installed with commands: python -m pip install m3u8
                                                                           python -m pip install requests

Usage: First, open chrome/browser, navigate to https://www.vbbound.com/live-webcam-of-virginia-beach-boardwalk and play the stream.
       Run python script in the interpreter.
       It will prompt for the hourly delay to download the videos and a max number of videos. 
       (If delay = 1, 1 video set is downloaded per hour. If max number = 1, 1 set of videos are downloaded)

       If a 404 error is returned, the .m3u8 url may need to be updated.
       In chrome, this is found by opening and playing livestream in chrome,
       go to -> Developer Tools -> Network -> record network log.
       In the XHR tab, there will be a chunklist_wsomenumber.m3u8 request. Click on it and copy it's Request URL which
       will look something like: https://58bdb48e25cf1.streamlock.net:19350/live/vcva002.stream/chunklist_w88396777.m3u8
       Set the m3u8_url variable (near the top of the code) equal to the new url.