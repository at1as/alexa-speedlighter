from   BeautifulSoup import BeautifulSoup
from   lxml import etree
import pdb
import re
import unicodedata


FEED_URL        = 'http://www.speedlighter.ca/feed/'
FILTER_CATEGORY = 'Digital Darkroom'
TEXT_BLOCK      = '{http://purl.org/rss/1.0/modules/content/}encoded'
MAX_PAGES       = 10
audible_posts   = []


def get_site_content(page=1):
  # Get full XML RSS Feed
  tree = etree.parse(FEED_URL + '?paged={}'.format(page))
  return tree.getroot()

def get_items_from_page(page):
  # Each post is in an <item> block
  return page.getchildren()[0].findall('item')


def extract_date(date_time_str):
  # Fri, 04 Nov 2016 19:53:18 +0000 => Fri, 04 Nov 2016
  try:
    return  ' '.join(date_time_str.split(' ')[0:4])
  except:
    return date_time_str


def get_page(page_num=1):
  xml_page = get_site_content(page_num)
  return get_items_from_page(xml_page)

def get_posts_matching_category(all_posts, target_category):
  # Extract articles with FILTER_CATEGORY tag
  matching_posts = []

  for post in all_posts:
    for category in post.findall('category'):
      if category.text == target_category:
        matching_posts.append(post)
        continue

  return matching_posts



for page_number in range(0, MAX_PAGES):

  all_posts     = get_page(page_number)
  audible_posts = get_posts_matching_category(all_posts, FILTER_CATEGORY)

  if len(audible_posts) == 0:
    continue

  

  # Get content from audible posts
  for target_post in audible_posts:

    title_str   = target_post.find('title').text or ''
    date_str    = extract_date(target_post.find('pubDate').text)
    content_str = target_post.find(TEXT_BLOCK).text

    s = BeautifulSoup(content_str, convertEntities=BeautifulSoup.HTML_ENTITIES)
    safe_html = ''.join(s.findAll(text=True))

    safe_html = unicodedata.normalize('NFKD', safe_html)

    print '{} published on {}'.format(unicode(title_str), unicode(date_str))
    print safe_html

  break

  print 'Sorry, there are no recent or archived posts currently available'



