import praw
import youtube_dl


r = praw.Reddit(user_agent='LTTscraper')
submissions = r.get_subreddit('listentothis').get_top_from_week(limit=10)

save_path = "C:\\Users\\Sri\\Desktop\\listentothis.txt"
dl_path = "C:\\Users\\Sri\\Desktop\\listentothisdls"

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '256',
    }],
}
for s in submissions:

    if "youtube" in s.url:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:  #import downloader and save as ydl variable
            ydl.download([s.url]) #download audio from URL of each submission

