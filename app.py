from flask import Flask, render_template
import requests
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_meme():
    # Uncomment this line and comment out the other url line if you want to use a specific meme subreddit
    sr = "/wholesomememes"
    url = "https://meme-api.herokuapp.com/gimme" + sr
    # url = "https://meme-api.herokuapp.com/gimme"
    try:
        response = json.loads(requests.get(url).text)
        meme_large = response["preview"][-2]
        subreddit = response["subreddit"]
        return meme_large, subreddit
    except Exception as e:
        return None, None

@app.route("/")
def index():
    meme_pic, subreddit = get_meme()
    if meme_pic and subreddit:
        return render_template("meme_index.html", meme_pic=meme_pic, subreddit=subreddit)
    else:
        return "Failed to retrieve meme. Please try again later.", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
