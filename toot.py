import os
from pathlib import Path
from mastodon import Mastodon
import feedparser
from bs4 import BeautifulSoup
import textwrap
import pickle

dir_name = os.path.dirname(__file__)
access_token = Path(dir_name+'/access_token.txt').read_text().strip()
mastodon = Mastodon(
    access_token = access_token,
    api_base_url = 'https://kiddush.social/'
)

d1 = feedparser.parse('https://18forty.org/articles/feed/')
d2 = feedparser.parse('https://ireadthisovershabbos.substack.com/feed/')
d3 = feedparser.parse('https://www.spreaker.com/show/4344730/episodes/feed')
d4 = feedparser.parse('https://readingjewishhistoryintheparsha.substack.com/feed')
posted_file = dir_name+'/posted.pickle'

for d in [d1,d2,d3,d4]:
    num_entries = min(len(d.entries),10)
    for x in range(num_entries-1,-1,-1):
        entry = d.entries[x]
        link = entry.link
        if os.path.isfile(posted_file): 
            with open(posted_file, 'rb') as f:
                posted_list = pickle.load(f)
        else:
            posted_list = []
        if link not in posted_list:
            if 'Shabbos' or 'Jewish History' in d.feed.title:
                desc = BeautifulSoup(entry.description,'lxml').p.text
                toot = entry.author+':\n\"'+entry.title+'\"\n\n'+desc+'\n\n'+entry.link.split('#')[0]
            elif 'Podcast' in d.feed.title:
                toot = d.feed.title+':\n'+entry.title+'\n\n'+entry.link.split('#')[0]
            elif 'Articles' in d.feed.title:
                toot = '18Forty Article:\n\"'+entry.title+'\"\n\n'+entry.link.split('#')[0]
            if len(toot)>500:
                new_desc_len = len(desc)-(len(toot)-500)
                desc = textwrap.shorten(desc, width =new_desc_len, placeholder='...')
                toot = '\"'+entry.title+'\"'+' by '+entry.author+'\n\n'+desc+'\n\n'+entry.link
            mastodon.status_post(toot, visibility='public')
            posted_list.append(link)
            with open(posted_file, 'wb') as f:
                pickle.dump(posted_list, f)
