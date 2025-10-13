import json
import ssl
import re
from urllib.request import urlopen

def getWikiTitle():
    title = input("Enter Wikipedia Article Title:\n")
    title = title.lower()
    title = re.sub(r'[^a-z0-9]+', '-', title)
    title = title.strip('-')
    return title

def sendRequest(url):
    try: 
        context = ssl._create_unverified_context()
        response = urlopen(url, context=context)
        wikiData =json.loads(response.read())
        print(wikiData)
    except:
        print("Can't find article")

def main():
    wikiTitle = getWikiTitle()
    url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles={wikiTitle}&rvprop=timestamp|user&rvlimit=20&redirects'
    sendRequest(url)
    print(url)
main()


# NOTES:
# Provide name of Wikipedia artilcle on command-line when ran
# Responds by providing up to 30 most recent changes to that article, in reverse chronological order, time of change, one space character, then user of person making changes, followed by newline character.
# After printing changes, exit with error code 0
# If fewer than 30 changes, show all changes
# If page redirects as part of search, then first line of output from app should have the form "Redirectded to <article name>"
# If no name on command-line, print message and exit with error code 1
# If no Wikipedia page for name, print message and exit with error code 2
# If network error, print message and exit with error code 3