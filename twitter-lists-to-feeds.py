from cache_to_disk import cache_to_disk
from cache_to_disk import delete_disk_caches_for_function
from dotenv import load_dotenv
from feedsearch import search
from slugify import slugify
from twitter import *
import feedparser
import os
import sys

load_dotenv()

################################################################

consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token_key = os.environ.get('ACCESS_TOKEN_KEY')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

api = Twitter(
    auth=OAuth(consumer_key=consumer_key,
               consumer_secret=consumer_secret,
               token=access_token_key,
               token_secret=access_token_secret))

################################################################


screen_name = os.environ.get('SCREEN_NAME')


################################################################

clear_cache = (os.environ.get('CLEAR_CACHE')== 'True')
functions_to_clear = ['grab_lists', 'grab_members',
                      'get_feed_metadata', 'search_feeds', 'make_opml_file']

if clear_cache:
    print("Clearing cache")
    for f in functions_to_clear:
        delete_disk_caches_for_function(f)
    print("Done clearing cache")
    sys.exit(0)

################################################################





################################################################

OPML_START = '<?xml version="1.0" encoding="UTF-8"?><opml version="1.1"><head><title>%(title)s</title></head><body><outline text="%(title)s" title="%(title)s">'

OPML_END = """</outline></body></opml>"""

OPML_OUTLINE_FEED = '<outline text="%(title)s" title="%(title)s" type="rss" version="RSS" htmlUrl="%(html_url)s" xmlUrl="%(xml_url)s" />'

################################################################


@cache_to_disk(3)
def grab_lists(screen_name):
    lists = api.lists.list(screen_name=screen_name)
    for l in lists:
        print(l['name'], l['id'])
    return lists


@cache_to_disk(3)
def grab_members(screen_name, list_id):
    print("Getting members")
    more_pages = True
    cursor = ''
    members = []
    i = 0
    while more_pages:
        i = i + 1
        print("Page", i)
        members_req = api.lists.members(owner_screen_name=screen_name, list_id=list_id,
                                        count=100, cursor=cursor, user_fields=('screen_name', 'url'))
        members = members + members_req['users']
        del members_req['users']
        cursor = members_req['next_cursor_str']

        if (cursor == '0'):
            print("No more pages")
            more_pages = False
    return members


@cache_to_disk(3)
def search_feeds(url):
    try:
        search_feeds = search(url, as_urls=True)
    except:
        print("Error searching for feeds. Skipping")
        return []
    return search_feeds


@cache_to_disk(3)
def get_feed_metadata(feed_url, url):
    try:
        d = feedparser.parse(feed_url)

        if d['feed']['title']:
            title = d['feed']['title']
        else:
            title = slugify(feed_url)

        feed = {
            "url": url,
            "title": title,
            "feed_url": feed_url
        }
        return feed
    except:
        print("Error getting feed metadata. Skipping")
        return {
            "url": url,
            "feed_url": feed_url,
            "title": slugify(feed_url)
        }
        
@cache_to_disk(3)
def make_opml_file(opml_name, feeds):
    opml_file = ""
    opml_file = opml_file + (OPML_START % {'title': opml_name})

    print("Found %d feeds" % len(feeds))
    for f in feeds:
        opml_file = opml_file + \
            (OPML_OUTLINE_FEED %
            {'title': f['title'], 'html_url': f['url'], 'xml_url': f['feed_url']})


    opml_file = opml_file + (OPML_END)
    return opml_file


################################################################

user_lists = api.lists.list(screen_name=screen_name)

for l in user_lists:
    print(l['name'], l['id'])
    screen_name = l['user']['screen_name']

    opml_name = l['name']
    try: 
        members = grab_members(screen_name, l['id'])
        
    except:
        members = None
        print("gathering members list failed")


    if members: 

        print("Found %d members" % len(members))
        feeds = []

        print("Searching for feeds")
        for m in members:
            url = m['url']

            print("\t", "@"+m['screen_name'], url)
            if url:

                found_feeds = search_feeds(url)
                print("\t\tFound %d feeds" % len(found_feeds))
                for f in found_feeds:
                    feed = get_feed_metadata(f, url)
                    if ('title' not in feed): 
                        feed['title'] = slugify(feed['feed_url'])
                    print("\t\t", feed['title'])
                    feeds.append(feed)

        if len(feeds) == 0:
            print("No feeds found")
        else:

        
            opml_contents = make_opml_file(opml_name, feeds)

            print("Writing OPML file")
            fname = slugify(screen_name + " " + opml_name) + '.opml'
            filehandle = open(fname, 'w')
            filehandle.write(opml_contents)
            filehandle.close()

