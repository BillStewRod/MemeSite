from flask import Flask, render_template
import praw

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Reddit API credentials
REDDIT_CLIENT_ID = 'your_client_id'
REDDIT_CLIENT_SECRET = 'your_client_secret'
REDDIT_USER_AGENT = 'your_user_agent'

# Initialize Reddit instance
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     user_agent=REDDIT_USER_AGENT)

def get_meme():
    try:
        subreddit = reddit.subreddit('wholesomememes')
        meme = subreddit.random()
        meme_url = meme.url
        meme_subreddit = meme.subreddit.display_name
        return meme_url, meme_subreddit
    except Exception as e:
        print(f"Error fetching meme: {e}")
        return None, None

@app.route("/")
def index():
    meme_pic, subreddit = get_meme()
    if meme_pic and subreddit:
        return render_template("meme_index.html", meme_pic=meme_pic, subreddit=subreddit)
    else:
        return "Failed to retrieve meme. Please try again later.", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)