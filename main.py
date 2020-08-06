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
  if tag.name == "h2" and ("The" in tag.text or "the" in tag.text or "and" in tag.text) and "grievances" not in tag.text:
    fables.append(list_no)
    fables.append(tag)
    fables.append(tag.find_next_sibling("p"))
    if "." in tag.find_next_sibling("p").find_next_sibling("p").text:
      fables.append(tag.find_next_sibling("p").find_next_sibling("p"))
    list_no = list_no + 1
  
# set dates
start_date = date(2020, 5, 24)
date_diff_pre = date.today() - start_date
pre_t = date_diff_pre.days
t = pre_t % 311

# tweet fable
for x in fables:
  if type(x) == int and x == t:
    fable_name = "'" + fables[fables.index(x)+1].text.strip() + "'"
    api.update_status(fable_name)
    tweet_id = api.user_timeline(screen_name = 'AesopFableBot', count = 100, include_rts = False)[0].id
    time.sleep(10)
    fable_body_total_txt = re.sub('f.gg.t','bundle',fables[fables.index(x)+2].text.replace('\r\n','').replace('      ',' '))
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
        if len(tweet) > 280:
          text_2 = []
          text_iter_2 = iter(text_2)
          for clause in re.split(r'(,)',tweet):
            text_2.append(clause)
          clean_text_2 = [f+next(text_iter_2, '') for f in text_iter_2]
          clean_text_iter_2 = iter(clean_text_2)
          tweet_2 = ''
          for q in clean_text_iter_2:
            if len(tweet_2) + len(q) <= 280:
              tweet_2 = tweet_2 + q
              api.update_status(tweet_2,tweet_id)
              tweet_id = api.user_timeline(screen_name = 'AesopFableBot', count = 100, include_rts = False)[0].id
              time.sleep(10)
              tweet_2 = ''
            tweet = z    
        else:
            if len(z) > 280:
              text_3 = []
              text_iter_3 = iter(text_3)
              for clause in re.split(r'(,)',z):
                text_3.append(clause)
              clean_text_3 = [f+next(text_iter_3, '') for f in text_iter_3]
              clean_text_iter_3 = iter(clean_text_3)
              tweet_3 = ''
              for w in clean_text_iter_3:
                if len(tweet_3) + len(w) <= 280:
                  tweet_3 = tweet_3 + w
                  api.update_status(tweet_3,tweet_id)
                  tweet_id = api.user_timeline(screen_name = 'AesopFableBot', count = 100, include_rts = False)[0].id
                  time.sleep(10)
                  tweet_3 = ''
            else:
              api.update_status(tweet,tweet_id)
              tweet_id = api.user_timeline(screen_name = 'AesopFableBot', count = 100, include_rts = False)[0].id
              time.sleep(10)
        tweet = z
        if len(z) > 280:
          tweet = ''
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
