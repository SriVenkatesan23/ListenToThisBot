import praw
import os.path

r = praw.Reddit(user_agent='LTTscraper')
submissions = r.get_subreddit('listentothis').get_top_from_week(limit=15)

save_path = "C:\\Users\\Sri\\Desktop\\listentothis.txt"
file = open(save_path, "r+")

for s in submissions:

    file.write(str(s))
    file.write("\n")
    file.write(s.url)
    file.write("\n")
    file.write("\n")


file.close()
