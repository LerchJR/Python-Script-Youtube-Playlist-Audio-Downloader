# Python-Script-Youtube-Playlist-Audio-Downloader
This script was written by ChatGPT to download a playlist from youtube. You can select a cookie file to get past age restricted videos &amp; select where the mp3 files are downloaded to.
This does require FFmpeg & yt-dlp to function properly.
In main folder (for example C:\yt-dlp) include yt-dlp and its necessary files, the .py script, and your cookies file if needed. Run the .py and input the playlist link, click download, and choose path where files will be installed.
This script will show progress and different colors for each file, and will also include album cover & name.
If you want to edit the wait time between each download, you can look at line 35 ( "--sleep-interval", "25",  # wait 25 seconds between downloads, can change if needed), change the interval to anywhere between 10-30 seconds to not get flagged by youtube. 

Green = Download started/destination

Orange = Already downloaded/skipped

Red = Errors/failures

Black = Regular info
