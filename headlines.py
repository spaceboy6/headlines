from flask import Flask
import feedparser

app = Flask(__name__)

RSS_FEEDS = {'science':"https://news.google.com/news/rss/headlines/section/topic/SCIENCE?ned=us&hl=en&gl=US",
            'entertainment':"https://news.google.com/news/rss/headlines/section/topic/ENTERTAINMENT?ned=us&hl=en&gl=US",
            'fox':"http://feeds.foxnews.com/foxnews/latest",
            'tech':"https://news.google.com/news/rss/headlines/section/topic/TECHNOLOGY?ned=us&hl=en&gl=US",
            'iol':"http://www.iol.co.za/cmlink/1.640"}

@app.route("/")
@app.route("/<publication>")
def get_news(publication):
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_article = feed['entries'][0]
    return """<html>
        <body>
            <h1> HEADLINES </h1>
            <b>{0}</b> <br/>
            <i>{1}</i> <br/>
            <p>{2}</p> <br/>
        </body>
    </html>""".format(first_article.get("title"), 
                    first_article.get("published"),
                    first_article.get("summary"))

if __name__ == "__main__":
    app.run(port=5000, debug=True)
