import requests
import re
import time
from bs4 import BeautifulSoup
from array import array
from datetime import date, datetime, timedelta
import tweepy

# setup
URL = 'https://www.gutenberg.org/files/21/21-h/21-h.htm'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

# access Twitter
auth = tweepy.OAuthHandler("API_KEY", "API_KEY_SECRET")
auth.set_access_token("ACCESS_TOKEN", "ACCCESS_TOKEN_SECRET")
api = tweepy.API(auth)

# scrape Gutenberg
fables = []
list_no = 0
for tag in soup.find_all(["h2","p"]):
  if tag.name == "h2" and ("The" in tag.text or "the" in tag.text or "and" in tag.text) and ("ggot" not in tag.find_next_sibling("p").text):
    fables.append(list_no)
    fables.append(tag)
    fables.append(tag.find_next_sibling("p"))
    if "." in tag.find_next_sibling("p").find_next_sibling("p").text:
      fables.append(tag.find_next_sibling("p").find_next_sibling("p"))
    list_no = list_no + 1
  
# set dates
start_date = date(2020, 5, 26)
date_diff_pre = date.today() - start_date
pre_t = date_diff_pre.days
t = pre_t % 308

# tweet fable
for x in fables:
  if type(x) == int and x == t:
    fable_name = fables[fables.index(x)+1].text
    api.update_status(fable_name)
    tweet_id = api.user_timeline(screen_name = 'AesopFableBot', count = 100, include_rts = False)[0].id
    time.sleep(10)
    fable_body_total_txt = fables[fables.index(x)+2].text.replace('\r\n','').replace('      ',' ')
    text = []
    text_iter = iter(text)
    for sentence in re.split(r'([."].)',fable_body_total_txt):
      text.append(sentence)
    clean_text = [y+next(text_iter, '') for y in text_iter]
    clean_text_iter = iter(clean_text)
    tweet = ''
    for z in clean_text_iter:
      if len(tweet) + len(z) <= 280:
        tweet = tweet + z
      else:
        api.update_status(tweet,tweet_id)
        tweet_id = api.user_timeline(screen_name = 'AesopFableBot', count = 100, include_rts = False)[0].id
        time.sleep(10)
        tweet = z
    api.update_status(tweet,tweet_id)
    tweet_id = api.user_timeline(screen_name = 'AesopFableBot', count = 100, include_rts = False)[0].id
    time.sleep(10)
    if type(fables[fables.index(x)+3]) == int:
      break
    else:
      tweet = fables[fables.index(x)+3].text.replace('\r\n','').replace('      ',' ')
      api.update_status(tweet,tweet_id)
else:
  x = fables.index(x) + 1
