from flask import Flask, render_template
import feedparser

app = Flask(__name__)

RSS_FEEDS = {'science':"https://news.google.com/news/rss/headlines/section/topic/SCIENCE?ned=us&hl=en&gl=US",
            'entertainment':"https://news.google.com/news/rss/headlines/section/topic/ENTERTAINMENT?ned=us&hl=en&gl=US",
            'fox':"http://feeds.foxnews.com/foxnews/latest",
            'tech':"https://news.google.com/news/rss/headlines/section/topic/TECHNOLOGY?ned=us&hl=en&gl=US",
            'iol':"http://www.iol.co.za/cmlink/1.640"}

@app.route("/")
@app.route("/<publication>")
def get_news(publication='science'):
    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template("home.html",articles=feed['entries'])

if __name__ == "__main__":
    app.run(port=5000, debug=True)
