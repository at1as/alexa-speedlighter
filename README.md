# Speedlighter

Alexa skill for reading entries from my Father's [Photography Blog](http://www.speedlighter.ca/).

Parses [RSS feed](http://www.speedlighter.ca/feed/) for posts in the `Audible` category and reads them out.


### Status

Available as an Alexa [Skill in the US](https://www.amazon.com/s/ref=nb_sb_noss/163-7867705-1788348?url=search-alias%3Dalexa-skills&field-keywords=speedlighter)


### Usage

Pretty straight-forward, just ask Alexa something like:

```
Alexa ask SpeedLighter for the latest post
```

```
Alexa ask SpeedLighter for the last five entries
```

```
Alexa ask SpeedLighter what's new
```


### Updating

```
# Build zip file to upload as lambda function
$ zip -r speedlighter.zip *

# Build dependencies
#   (The only dependency not in the standard library is beautiful soup):
$ pip install BeautifulSoup -t dependencies/
```

