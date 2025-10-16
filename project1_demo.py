import json
import ssl
import re
import sys
from urllib.request import urlopen, Request

# To run just put: python project1_demo.py "<Wikipedia article name>"
def getWikiTitle():
    try:
        title = input("Enter Wikipedia Article Title:\n")
        title = re.sub(r'[^a-zA-Z0-9,]+', '_', title)
        title = title.strip('_')
        print("title =  " + title)
    except IndexError:
        print("Please provide a Wikipedia article name on the command line")
        sys.exit(1)
    #title = title.replace(' ', '_')
    return title

def sendRequest(url):
    try: 
        request = Request(url, headers={'User-Agent': 'CS222Project/1.0'})
        context = ssl._create_unverified_context()
        response = urlopen(request, context=context)
        wikiData = json.loads(response.read())

        if 'redirects' in wikiData.get('query', {}):
            redirect_name = wikiData['query']['redirects'][0]['to']
            print(f"Redirected to {redirect_name}")
        pages = wikiData['query']['pages']
        page_id = list(pages.keys())[0]
        page = pages[page_id]
        
        if 'missing' in page:
            print("No Wikipedia page found for the provided name")
            sys.exit(2)
        revisions = page['revisions']
        for revision in revisions:
            timestamp = revision['timestamp']
            user = revision['user']
            print(f"{timestamp} {user}")
        sys.exit(0)
    except Exception as e:
        print("Network error occurred")
        sys.exit(3)

def main():
    wikiTitle = getWikiTitle()
    url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles={wikiTitle}&rvprop=timestamp|user&rvlimit=30&redirects'
    sendRequest(url)

main()


# NOTES:
# get name of Wikipedia article on command-line by input when ran
# Responds by providing up to 30 most recent changes to that article, in reverse chronological order, time of change, one space character, then user of person making changes, followed by newline character.
# After printing changes, exit with error code 0
# If fewer than 30 changes, show all changes
# If page redirects as part of search, then first line of output from app should have the form "Redirectded to <article name>"
# If no name on command-line, print message and exit with error code 1
# If no Wikipedia page for name, print message and exit with error code 2
# If network error, print message and exit with error code 3