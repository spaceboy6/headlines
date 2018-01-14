from flask import Flask, render_template, request
import feedparser
import json
import urllib2
import urllib


app = Flask(__name__)

RSS_FEEDS = {'science':"https://news.google.com/news/rss/headlines/section/topic/SCIENCE?ned=us&hl=en&gl=US",
            'entertainment':"https://news.google.com/news/rss/headlines/section/topic/ENTERTAINMENT?ned=us&hl=en&gl=US",
            'fox':"http://feeds.foxnews.com/foxnews/latest",
            'tech':"https://news.google.com/news/rss/headlines/section/topic/TECHNOLOGY?ned=us&hl=en&gl=US",
            'iol':"http://www.iol.co.za/cmlink/1.640"
            }

WEATHERURL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=07574fd3aa112027dd0c8c2eadcb079b"

DEFAULTS = {"publication":"science", 
            "city":"Santa Barbara",
            "currency_from":"USD",
            "currency_to":"USD"
            }

CURRENCYURL = "https://openexchangerates.org//api/latest.json?app_id=20446256fe8d4c8d976fac72c55b515c"

@app.route("/")
def home():
    publication = request.args.get("publication")
    if not publication:
        publication = DEFAULTS["publication"]
    articles = get_news(publication)
    city = request.args.get("city")
    if not city:
        city = DEFAULTS["city"]
    weather = get_weather(city)
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate, currencies = get_rate(currency_from, currency_to)
    return render_template("home.html",
                            articles=articles,
                            weather=weather,
                            currency_from=currency_from,
                            currency_to=currency_to,
                            rate=rate,
                            currencies=sorted(currencies))

def get_news(query):
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "science"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']

def get_weather(query):
    query = urllib.quote(query)
    url = WEATHERURL.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"],
                    "temperature": parsed["main"]["temp"],
                    "city": parsed["name"],
                    "country": parsed['sys']['country']
                    }
    return weather

def get_rate(frm, to):
    all_currency = urllib2.urlopen(CURRENCYURL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate/frm_rate, parsed.keys())

if __name__ == "__main__":
    app.run(port=5000, debug=True)
