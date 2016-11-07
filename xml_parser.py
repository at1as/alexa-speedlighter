from   dependencies.BeautifulSoup import BeautifulSoup
import httplib
import re
import unicodedata
import xml.etree.ElementTree as ET
import pdb

SITE_URL        = 'www.speedlighter.ca'
FILTER_CATEGORY = 'Audible'
TEXT_BLOCK      = '{http://purl.org/rss/1.0/modules/content/}encoded'
MAX_PAGES       = 10


def get_site_content(page=1):
  # Get full XML RSS Feed
  page_query = '?paged={}'.format(page) if page > 1 else '' # paged=1 issues HTTP redirect

  conn = httplib.HTTPConnection(SITE_URL, 80)
  conn.request('GET', '/feed/' + page_query)
  response = conn.getresponse()
  tree = ET.parse(response)
  conn.close()
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

def get_verbal_text_string(input_text):
  # Remove unexpected formatting before text can be verbalized
  try:    clean_text = unicodedata.normalize('NFKD', unicode(input_text))
  except: clean_text = unicodedata.normalize('NFKD', input_text)

  clean_text = remove_url_paths(clean_text)
  clean_text = replace_unpronounceable_chars(clean_text)
  clean_text = remove_unpronounceable_chars(clean_text)
  return clean_text

def remove_url_paths(input_text):
  # Strip everything except base URL : https://www.speedlighter.ca/path/to/resource => speedlighter.ca
  try:    return re.sub("(https?://|www.|https?://www.)(?P<url>[^\/^\?]+)[^\s]*", "\\g<url>", input_text)
  except: return input_text

def replace_unpronounceable_chars(input_string):
  # Remove newlines and replace a few specific unicode characters
  return input_string.replace('\n', ' ').replace(u"\u2018", "'").replace(u"\u2019", "'")

def remove_unpronounceable_chars(input_string):
  # Removes reamining unicode chacters : "hello \u2016 world" => "hello world"
  try:
    return input_string.encode('ascii','ignore')
  except:
    try:    return input_string.decode('unicode_escape').encode('ascii','ignore')
    except: return input_string


def get_page(page_num=1):
  xml_page = get_site_content(page_num)
  return get_items_from_page(xml_page)

def get_posts_matching_category(all_posts, target_category):
  # Extract articles with target_category set
  matching_posts = []

  for post in all_posts:
    for category in post.findall('category'):
      if category.text == target_category:
        matching_posts.append(post)
        continue

  return matching_posts


def get_extracted_text(articles=1):

  matches = []
  for page_number in range(0, MAX_PAGES):

    all_posts     = get_page(page_number + 1)
    audible_posts = get_posts_matching_category(all_posts, FILTER_CATEGORY)

    if len(audible_posts) == 0:
      continue
    if len(matches) >= articles:
      break

    # Get content from audible posts
    for target_post in audible_posts:

      if len(matches) >= articles:
        break


      # Extract three desired pieces of information from XML
      title_str   = target_post.find('title').text or 'Untitled Post'
      date_str    = extract_date(target_post.find('pubDate').text) or 'Unknown Date'
      content_str = target_post.find(TEXT_BLOCK).text or 'No Content'

      # Extract text from within XML tags
      s = BeautifulSoup(content_str, convertEntities=BeautifulSoup.HTML_ENTITIES)
      safe_html = ''.join(s.findAll(text=True))

      safe_html = get_verbal_text_string(safe_html)
      title_str = get_verbal_text_string(title_str)

      # return first result found
      matches.append({'content': safe_html,
                      'title':   title_str,
                      'date':    date_str})


  if len(matches) == 0:
    return [{'content': 'Sorry, there are no recent or archived posts currently available. Please try again later',
             'title':   '',
             'date':    ''}]
  else:
    return matches


