# Speedlighter

`Status: Has been submitted for certification. Awaiting result`

Alexa skill for reading entries from my Father's [Photography Blog](http://www.speedlighter.ca/).

Parses [RSS feed](http://www.speedlighter.ca/feed/) for posts in the `Audible` category and reads them out.


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

